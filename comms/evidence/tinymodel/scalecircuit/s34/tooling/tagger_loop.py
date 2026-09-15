"""Inner loop for the tagger: the eval-driven curriculum loop from trainkey/docs/LOOP.md section 2,
instantiated for the 0.5B LoRA tagger. NOT a self-training loop: every training label is written by
a person; the model's own outputs never enter training data, not even correctness-filtered.

    EVAL    current adapter on (a) the fixed eval slice, docs 3-39 minus few-shot, never trained on,
            and (b) the newest hand-labelled batch of train-side docs.
    BUCKET  failures on (b) by class: na_wrong, anchor, hops_dropped, hops_extra, filter, relation.
    ROUTE   dominant class -> synthetic reweighting for the next round (more nesting phrasings for
            hops_dropped, fewer OOV->attribute for hops_extra, more descriptor anchors for anchor,
            more filter phrasings for filter).
    TRAIN   accumulated real labels (all batches so far, x rep) + reweighted synthetic + 10 percent
            plain-synthetic replay; LoRA continued from the previous adapter.
    STOP    hard cap 3 rounds; or eval delta < 1 point for 2 rounds; or eval regresses > 2 points
            (kill: keep the previous adapter).
    TRIGGER a round only runs when the newest batch has >= --min-fail failures (default 10).

    <local>/model-training/.venv/Scripts/python.exe scripts/tagger_loop.py --start models/tagger_lora_0.5b \\
        --batches data/tagger_real_70-99.jsonl data/tagger_real_100-129.jsonl --out models/tagger_loop
"""
import argparse
import json
import os
import random
import subprocess
import sys

import torch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from tagger3b import parse, norm_ent  # noqa: E402
from tagger_lora import chat, ROWS, FEWSHOT, KEY  # noqa: E402

PY = sys.executable


def classify(pred, truth):
    """One failure class per example, or None if correct at the structure+anchor+filter level."""
    k, p = parse(truth), parse(pred)
    if k == "NA" or p == "NA":
        return None if k == p else "na_wrong"
    if p is None:
        return "unparseable"
    if not (norm_ent(p[1]) == norm_ent(k[1]) or norm_ent(k[1]) in norm_ent(p[1]) or norm_ent(p[1]) in norm_ent(k[1])):
        return "anchor"
    if len(p[0]) < len(k[0]):
        return "hops_dropped"
    if len(p[0]) > len(k[0]):
        return "hops_extra"
    if (p[2] is None) != (k[2] is None):
        return "filter"
    if p[0] != k[0]:
        return "relation"
    return None


@torch.no_grad()
def tag_all(adapter, pairs, base="Qwen/Qwen2.5-0.5B-Instruct"):
    from peft import PeftModel
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(base)
    model = AutoModelForCausalLM.from_pretrained(base, torch_dtype=torch.bfloat16, attn_implementation="sdpa").cuda()
    model = PeftModel.from_pretrained(model, adapter).eval()
    out = []
    for q, _ in pairs:
        ids = tok(chat(tok, q), return_tensors="pt", add_special_tokens=False)["input_ids"].cuda()
        gen = model.generate(ids, max_new_tokens=40, do_sample=False, pad_token_id=tok.pad_token_id)
        out.append(tok.decode(gen[0, ids.shape[1]:], skip_special_tokens=True).strip().split("\n")[0])
    del model
    torch.cuda.empty_cache()
    return out


def batch_profile(pairs):
    """Data-drift profile of a labelled batch: NA fraction, mean chain depth, filter fraction."""
    tags = [t for _, t in pairs]
    chains = [parse(t) for t in tags if t != "NA"]
    chains = [c for c in chains if c not in ("NA", None)]
    return {"n": len(pairs), "na_frac": round(sum(t == "NA" for t in tags) / max(1, len(pairs)), 3),
            "mean_depth": round(sum(len(c[0]) for c in chains) / max(1, len(chains)), 2),
            "filter_frac": round(sum(c[2] is not None for c in chains) / max(1, len(chains)), 3)}


def drift_flags(new, acc):
    """Flags when the new batch's label distribution departs from the accumulated one."""
    flags = []
    if acc and abs(new["na_frac"] - acc["na_frac"]) > 0.15:
        flags.append(f"na_frac {new['na_frac']} vs accumulated {acc['na_frac']}")
    if acc and abs(new["mean_depth"] - acc["mean_depth"]) > 0.5:
        flags.append(f"mean_depth {new['mean_depth']} vs accumulated {acc['mean_depth']}")
    return flags


def eval_slice(adapter, pairs):
    preds = tag_all(adapter, pairs)
    classes = [classify(pr, t) for pr, (_, t) in zip(preds, pairs)]
    # ONE stop measure (2026-09-13 checkpoint fix): structure, the same tier the band is written in.
    # anchor and relation mismatches are autopsied and routed but do not count as slice failures here.
    STRUCTURE_FAIL = {"na_wrong", "unparseable", "hops_dropped", "hops_extra", "filter"}
    ok = sum(c not in STRUCTURE_FAIL for c in classes)
    buckets = {}
    for c in classes:
        if c:
            buckets[c] = buckets.get(c, 0) + 1
    return ok, buckets, preds


ROUTE = {  # dominant failure class -> generator knobs (see tagger_data.py main() env overrides)
    "hops_dropped": {"TAGGER_DEPTH_WEIGHTS": "20,35,30,15", "TAGGER_CLAUSE_FRAC": "0.55"},   # v3: clause wrappers
    "hops_extra": {"TAGGER_OOV_FRAC": "0.05"},
    "anchor": {"TAGGER_DESC_FRAC": "0.25", "TAGGER_LEADIN_FRAC": "0.30"},                 # v3: date/number lead-ins
    "filter": {"TAGGER_FILTER_FRAC": "0.40"},
    "relation": {},
    "na_wrong": {"TAGGER_NA_FRAC": "0.20"},
    "unparseable": {},
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", required=True, help="adapter to start from (the s8 full-run adapter)")
    ap.add_argument("--batches", nargs="+", required=True, help="hand-labelled jsonl batches, one per round, in order")
    ap.add_argument("--out", default=os.path.join(ROOT, "models", "tagger_loop"))
    ap.add_argument("--min-fail", type=int, default=10)
    ap.add_argument("--max-rounds", type=int, default=3)
    ap.add_argument("--n-synth", type=int, default=12000)
    ap.add_argument("--rep", type=int, default=5)
    ap.add_argument("--seed-labels", nargs="*", default=[], help="labelled batches already used by the starting adapter; join the accumulated labels without a round")
    ap.add_argument("--flat-so-far", type=int, default=0, help="resume: number of consecutive <1pt rounds already seen")
    ap.add_argument("--first-round", type=int, default=1, help="resume: number the first batch given as this round (earlier rounds' labels go in --seed-labels, their adapter in --start); loop_log.json is appended")
    ap.add_argument("--auto", action="store_true", help="skip the R2 pause (unattended); default: stop after the autopsy until why_r<N>.md exists")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    eval_pairs = [(ROWS[i]["input"], KEY[i]) for i in range(40) if i not in FEWSHOT]
    log_path = os.path.join(args.out, "loop_log.json")
    log = json.load(open(log_path)) if args.first_round > 1 and os.path.exists(log_path) else []
    log = [e for e in log if e.get("round", 0) < args.first_round or "stop" in e and "paused" in e["stop"] and e["round"] < args.first_round]
    flat = args.flat_so_far
    adapter = args.start
    prev_eval = None
    labelled_so_far = list(args.seed_labels)
    for r, batch_path in enumerate(args.batches[: args.max_rounds - (args.first_round - 1)], start=args.first_round):
        batch = [(json.loads(l)["question"], json.loads(l)["tag"]) for l in open(batch_path, encoding="utf-8")]
        assert not any(q == e[0] for q, _ in batch for e in eval_pairs), "eval doc in a training batch"
        ev_ok, ev_b, _ = eval_slice(adapter, eval_pairs)
        b_ok, b_buckets, b_preds = eval_slice(adapter, batch)
        n_fail = len(batch) - b_ok
        # data-drift gate: the new batch's label profile against everything labelled so far
        acc_pairs = [(json.loads(l)["question"], json.loads(l)["tag"]) for p in labelled_so_far for l in open(p, encoding="utf-8")]
        prof_new, prof_acc = batch_profile(batch), (batch_profile(acc_pairs) if acc_pairs else None)
        flags = drift_flags(prof_new, prof_acc)
        entry = {"round": r, "adapter_in": adapter, "eval_ok_before": ev_ok, "batch": batch_path,
                 "batch_ok": b_ok, "batch_fail": n_fail, "buckets": b_buckets,
                 "batch_profile": prof_new, "accumulated_profile": prof_acc, "drift_flags": flags}
        if flags:
            print("DRIFT FLAG on the new batch (the round still runs; the flag travels in the ledger row): " + "; ".join(flags), flush=True)
        print(json.dumps(entry), flush=True)
        if prev_eval is not None and ev_ok < prev_eval - 2:
            entry["stop"] = "eval regressed; keeping previous adapter"; log.append(entry); break
        if n_fail < args.min_fail:
            entry["stop"] = f"only {n_fail} failures on the new batch (< {args.min_fail}); no round"; log.append(entry)
            labelled_so_far.append(batch_path)
            continue
        # R1 autopsy: every failure on the new batch, per doc, with its class; frozen per round
        autopsy = [{"question": q, "pred": pr, "truth": t, "class": classify(pr, t)}
                   for (q, t), pr in zip(batch, b_preds) if classify(pr, t)]
        autopsy_path = os.path.join(args.out, f"autopsy_r{r}.json")
        json.dump({"round": r, "batch": batch_path, "counts": b_buckets, "failures": autopsy}, open(autopsy_path, "w"), indent=1)
        entry["autopsy"] = autopsy_path
        # R2 pause: a person writes the 5-why (rung 0: is the key right? then why -> missing mechanism, doc ids)
        why_path = os.path.join(args.out, f"why_r{r}.md")
        if not args.auto and not os.path.exists(why_path):
            template = [
                f"# 5-why for round {r} (fill in, save as why_r{r}.md, re-run the loop)", "",
                f"Autopsy: {autopsy_path}", f"Classes: {json.dumps(b_buckets)}", "",
                "## Rung 0",
                "For each failing doc: is the key's structure actually right for this question? List docs where it is not; they leave the fixable class.", "",
                "## 5-why on the largest fixable class",
                "1. why ... (doc ids)", "2. why ...", "3. ...", "Root = MISSING MECHANISM: ...", "",
                "## Route",
                "class -> knob(s) for this round, or 'no training this round' if the root is not a data mechanism.", "",
            ]
            with open(why_path + ".template", "w", encoding="utf-8") as f:
                f.write("\n".join(template))
            entry["stop"] = f"paused for the R2 5-why: write {why_path} (template written) and re-run"
            print(json.dumps(entry), flush=True); log.append(entry); break
        dominant = max(b_buckets, key=b_buckets.get)
        entry["route"] = dominant
        if os.path.exists(why_path):
            entry["why"] = why_path
        env = dict(os.environ, **ROUTE.get(dominant, {}))
        synth = os.path.join(args.out, f"synth_r{r}.jsonl")
        subprocess.run([PY, os.path.join(ROOT, "scripts", "tagger_data.py"), "--n", str(args.n_synth), "--seed", str(100 + r), "--out", synth], check=True, env=env)
        replay = os.path.join(args.out, f"replay_r{r}.jsonl")          # 10 percent plain synthetic replay
        subprocess.run([PY, os.path.join(ROOT, "scripts", "tagger_data.py"), "--n", str(args.n_synth // 10), "--seed", str(200 + r), "--out", replay], check=True)
        train = os.path.join(args.out, f"train_r{r}.jsonl")
        with open(train, "w", encoding="utf-8") as f:
            for p in (synth, replay):
                f.write(open(p, encoding="utf-8").read())
        labelled_so_far.append(batch_path)
        extra = os.path.join(args.out, f"real_r{r}.jsonl")
        with open(extra, "w", encoding="utf-8") as f:
            for p in labelled_so_far:
                f.write(open(p, encoding="utf-8").read())
        out_adapter = os.path.join(args.out, f"round{r}")
        subprocess.run([PY, os.path.join(ROOT, "scripts", "tagger_lora.py"), "--train", train, "--extra", extra, "--extra-rep", str(args.rep),
                        "--out", out_adapter, "--epochs", "1", "--init-adapter", adapter], check=True)
        ev_ok_after, ev_b_after, _ = eval_slice(out_adapter, eval_pairs)
        entry.update({"adapter_out": out_adapter, "eval_ok_after": ev_ok_after, "eval_buckets_after": ev_b_after})
        print(json.dumps(entry), flush=True)
        if ev_ok_after < ev_ok - 2:
            entry["stop"] = "eval regressed after training; keeping previous adapter"; log.append(entry); break
        flat = flat + 1 if abs(ev_ok_after - ev_ok) < 1 else 0
        adapter, prev_eval = out_adapter, ev_ok_after
        log.append(entry)
        if flat >= 2:
            entry["stop"] = "converged: < 1 point change for 2 rounds"; break
    json.dump(log, open(os.path.join(args.out, "loop_log.json"), "w"), indent=1)
    print("final adapter:", adapter)


if __name__ == "__main__":
    main()
