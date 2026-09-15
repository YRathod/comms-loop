"""LoRA fine-tune of Qwen2.5-0.5B-Instruct as a tagger: question -> mini-language tag.

    <local>/model-training/.venv/Scripts/python.exe scripts/tagger_lora.py --train data/tagger_train.jsonl --out models/tagger_lora_0.5b --epochs 2
    <local>/model-training/.venv/Scripts/python.exe scripts/tagger_lora.py --eval-only --out models/tagger_lora_0.5b

Evaluation: synthetic held-out (exact tag match) and the 30 real HotpotQA questions against the
hand key in scripts/tagger3b.py (structure / anchor / relation tiers). The 10 few-shot docs from
tagger3b are added to training as real-style examples; the 30 scored docs never are.
"""
import argparse
import json
import os
import random
import sys
import time

import torch
from peft import LoraConfig, PeftModel, get_peft_model
from transformers import AutoModelForCausalLM, AutoTokenizer

sys.path.insert(0, "scripts")
from tagger3b import KEY, FEWSHOT, SYSTEM, parse, norm_ent  # noqa: E402

ROWS = [json.loads(l) for l in open(r"C:\dev\research\memory-challange\long-bench\data\data\hotpotqa.jsonl", encoding="utf-8")][:40]


SHORT_SYSTEM = "Convert the question into the tag language: REL of ... of ENTITY [ PROP ] ? or NA. Output only the tag."


def chat(tok, q, tag=None):
    msgs = [{"role": "system", "content": SHORT_SYSTEM}, {"role": "user", "content": q}]
    prompt = tok.apply_chat_template(msgs, add_generation_prompt=True, tokenize=False)
    return prompt if tag is None else prompt + tag + tok.eos_token


def batches(tok, pairs, bs, device):
    for s in range(0, len(pairs), bs):
        chunk = pairs[s : s + bs]
        texts = [chat(tok, q, t) for q, t in chunk]
        prompts = [chat(tok, q) for q, _ in chunk]
        enc = tok(texts, return_tensors="pt", padding=True, add_special_tokens=False)
        labels = enc["input_ids"].clone()
        for i, p in enumerate(prompts):
            n = len(tok(p, add_special_tokens=False)["input_ids"])
            labels[i, :n] = -100                      # loss only on the tag
        labels[enc["attention_mask"] == 0] = -100
        yield {k: v.to(device) for k, v in enc.items()}, labels.to(device)


@torch.no_grad()
def generate(model, tok, q, device, max_new=40):
    ids = tok(chat(tok, q), return_tensors="pt", add_special_tokens=False)["input_ids"].to(device)
    out = model.generate(ids, max_new_tokens=max_new, do_sample=False, pad_token_id=tok.pad_token_id)
    return tok.decode(out[0, ids.shape[1]:], skip_special_tokens=True).strip().split("\n")[0]


def eval_real(model, tok, device, verbose=False):
    out = []
    for i, r in enumerate(ROWS):
        if i in FEWSHOT:
            continue
        pred = generate(model, tok, r["input"], device)
        k, p = parse(KEY[i]), parse(pred)
        na_ok = (k == "NA") == (p == "NA")
        struct = ent = rel = False
        if k != "NA" and p not in ("NA", None):
            struct = len(p[0]) == len(k[0]) and (p[2] is None) == (k[2] is None)
            ent = norm_ent(p[1]) == norm_ent(k[1]) or norm_ent(k[1]) in norm_ent(p[1]) or norm_ent(p[1]) in norm_ent(k[1])
            rel = p[0] == k[0] and p[2] == k[2]
        elif k == "NA" and p == "NA":
            struct = ent = rel = True
        out.append((i, pred, KEY[i], p is not None, na_ok, struct, ent, rel))
        if verbose:
            print(f"  doc {i:2d} | {pred:<58s} | key {KEY[i]:<50s} | struct {int(struct)} ent {int(ent)} rel {int(rel)}", flush=True)
    n = len(out)
    summary = {"n": n, "parses": sum(x[3] for x in out), "na_ok": sum(x[4] for x in out), "struct": sum(x[5] for x in out),
               "anchor": sum(x[6] for x in out), "relations": sum(x[7] for x in out)}
    # miss classes only (v1.15: autopsies on the eval slice name classes, never lift strings)
    classes = {"unparseable": sum(1 for x in out if not x[3]), "na_wrong": sum(1 for x in out if not x[4]),
               "struct_miss": sum(1 for x in out if x[3] and x[4] and not x[5]), "anchor_miss": sum(1 for x in out if x[3] and x[4] and not x[6]),
               "relation_miss": sum(1 for x in out if x[3] and x[4] and x[5] and not x[7])}
    print("real 30:", summary, "| miss classes:", classes, flush=True)
    return summary, out


def eval_synth(model, tok, device, pairs):
    ok = sum(generate(model, tok, q, device) == t for q, t in pairs)
    print(f"synthetic held-out exact tag match: {ok}/{len(pairs)}", flush=True)
    return ok / len(pairs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="Qwen/Qwen2.5-0.5B-Instruct")
    ap.add_argument("--train", default="data/tagger_train.jsonl")
    ap.add_argument("--out", default="models/tagger_lora_0.5b")
    ap.add_argument("--epochs", type=float, default=2)
    ap.add_argument("--bs", type=int, default=4)
    ap.add_argument("--accum", type=int, default=4, help="gradient accumulation steps (effective batch = bs * accum)")
    ap.add_argument("--lr", type=float, default=2e-4)
    ap.add_argument("--rank", type=int, default=16)
    ap.add_argument("--limit", type=int, default=0, help="use only the first N pairs (pre-gate)")
    ap.add_argument("--extra", default=None, help="jsonl of hand-labelled REAL pairs (question, tag) mixed into training, repeated --extra-rep times")
    ap.add_argument("--extra-rep", type=int, default=5)
    ap.add_argument("--eval-only", action="store_true")
    ap.add_argument("--init-adapter", default=None, help="continue training from this LoRA adapter (loop rounds)")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--sanity", default="50:1.0,100:0.4,200:0.15",
                    help="metric-sanity bands step:max_loss (banked from pre-gates 1-3: 0.05 at step 100, 0.006 at 175); "
                         "a breach or a NaN writes drift_alert.json and prints ALERT")
    ap.add_argument("--abort-on-drift", action="store_true", help="stop the run on a sanity breach instead of alerting only")
    ap.add_argument("--allow-unstamped", action="store_true", help="train on a file without a provenance stamp (legacy files only; say so in the pre-reg)")
    ap.add_argument("--eval-verbose", action="store_true", help="print per-doc eval-slice predictions and keys (default: class counts only, v1.15: never lift strings)")
    ap.add_argument("--no-real-eval", action="store_true", help="do not score the 30 eval docs at the end (hold-out experiments that must not look at the eval slice)")
    ap.add_argument("--mini-eval-every", type=int, default=0, help="if > 0, score 40 synthetic held-out pairs every N steps into the heartbeat")
    args = ap.parse_args()
    bands = sorted((int(k), float(v)) for k, v in (kv.split(":") for kv in args.sanity.split(",") if kv))
    device = "cuda"
    torch.manual_seed(args.seed); random.seed(args.seed)
    tok = AutoTokenizer.from_pretrained(args.base)
    tok.padding_side = "right"
    model = AutoModelForCausalLM.from_pretrained(args.base, torch_dtype=torch.bfloat16, attn_implementation="sdpa").to(device)

    if not args.eval_only and not args.allow_unstamped:                     # provenance duty (v1.15): no stamp, no training
        import hashlib
        stamp = args.train + ".provenance.json"
        assert os.path.exists(stamp), f"no provenance stamp for {args.train}: run scripts/tagger_data_check.py {args.train} first"
        st = json.load(open(stamp))
        assert st.get("verdict") == "CLEAN" and st.get("sha256") == hashlib.sha256(open(args.train, "rb").read()).hexdigest(),             f"provenance stamp for {args.train} is not CLEAN or does not match the file"
        print(f"provenance stamp OK ({st['utc']})", flush=True)
    pairs = [(json.loads(l)["question"], json.loads(l)["tag"]) for l in open(args.train, encoding="utf-8")]
    if args.limit:
        pairs = pairs[: args.limit]
    held = pairs[-500:]; pairs = pairs[:-500]
    pairs += [(ROWS[i]["input"], KEY[i]) for i in FEWSHOT] * 5      # ten real-style examples, repeated
    if args.extra:
        extra = [(json.loads(l)["question"], json.loads(l)["tag"]) for l in open(args.extra, encoding="utf-8")]
        assert not any(q == ROWS[i]["input"] for q, _ in extra for i in range(40) if i not in FEWSHOT), "eval doc leaked into --extra"
        pairs += extra * args.extra_rep
        print(f"extra real pairs: {len(extra)} x {args.extra_rep}", flush=True)

    if args.eval_only:
        model = PeftModel.from_pretrained(model, args.out).eval()
        eval_synth(model, tok, device, held[:200]); eval_real(model, tok, device, verbose=args.eval_verbose)
        return

    if args.init_adapter:
        model = PeftModel.from_pretrained(model, args.init_adapter, is_trainable=True)
    else:
        cfg = LoraConfig(r=args.rank, lora_alpha=2 * args.rank, lora_dropout=0.05, task_type="CAUSAL_LM",
                         target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"])
        model = get_peft_model(model, cfg)
    model.print_trainable_parameters()
    opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=args.lr, weight_decay=0.0)
    steps_per_epoch = (len(pairs) + args.bs * args.accum - 1) // (args.bs * args.accum)
    total = int(steps_per_epoch * args.epochs)
    sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: min(1.0, (s + 1) / 50) * max(0.05, 1 - s / max(1, total)))
    model.train(); t0 = time.time(); step = 0
    print(f"pairs {len(pairs)}  steps {total}", flush=True)
    micro = 0
    while step < total:
        random.shuffle(pairs)
        for enc, labels in batches(tok, pairs, args.bs, device):
            out = model(**enc, labels=labels)
            (out.loss / args.accum).backward()
            micro += 1
            if micro % args.accum:
                continue
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step(); sched.step(); opt.zero_grad(set_to_none=True)
            step += 1
            loss_now = out.loss.item()
            ema = loss_now if step == 1 else 0.9 * ema + 0.1 * loss_now
            # metric sanity (LOOP.md 1a): NaN, or EMA loss above the banked band for this step
            breach = None
            if loss_now != loss_now:
                breach = "NaN loss"
            else:
                for b_step, b_max in bands:
                    if step >= b_step and ema > b_max:
                        breach = f"ema loss {ema:.3f} > band {b_max} at step {step} (band step {b_step})"
            if breach:
                os.makedirs(args.out, exist_ok=True)
                json.dump({"step": step, "breach": breach, "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())},
                          open(os.path.join(args.out, "drift_alert.json"), "w"))
                print(f"ALERT metric-sanity: {breach}", flush=True)
                if args.abort_on_drift or breach == "NaN loss":
                    print("aborting run on sanity breach", flush=True)
                    return
            if step % 25 == 0:
                print(f"step {step}/{total} loss {loss_now:.4f} ema {ema:.4f} {time.time() - t0:.0f}s", flush=True)
                # heartbeat for the drift tick (LOOP.md 1a): liveness, metric sanity, ETA
                os.makedirs(args.out, exist_ok=True)
                elapsed = time.time() - t0
                hb = {"step": step, "total": total, "loss": round(loss_now, 4), "ema_loss": round(ema, 4), "elapsed_s": round(elapsed),
                      "eta_s": round(elapsed / step * (total - step)), "sanity_ok": breach is None,
                      "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
                if args.mini_eval_every and step % args.mini_eval_every == 0:
                    model.eval(); hb["mini_synth_ok"] = eval_synth(model, tok, device, held[:40]); model.train()
                json.dump(hb, open(os.path.join(args.out, "heartbeat.json"), "w"))
            if step >= total:
                break
    os.makedirs(args.out, exist_ok=True)
    model.save_pretrained(args.out)
    model.eval()
    synth = eval_synth(model, tok, device, held[:200])
    summary, rows = (None, None) if args.no_real_eval else eval_real(model, tok, device, verbose=args.eval_verbose)
    json.dump({"synth_heldout": synth, "real": summary, "rows": rows, "args": vars(args), "train_seconds": time.time() - t0},
              open(os.path.join(args.out, "eval.json"), "w"), indent=1)
    print(f"saved {args.out}  train {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
