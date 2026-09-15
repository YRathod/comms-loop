"""LoRA fine-tune of a Qwen2.5-Instruct model as a FREE-FORM decomposer (fix 1, key #10):
question -> "NA" or "H1: ...\\nH2: ... #1 ..." (H2 may be "NA" for single-hop questions: then only H1 is used).

Training rows: jsonl with fields question, decomp (and provenance fields). The train file needs a
<file>.provenance.json CLEAN stamp (scripts/decomp_data_check.py). Evaluation on a labelled DEV file
reports: parse rate, anchor-kept rate (H1 contains a capitalised span of the question), NA agreement.

    python scripts/decomp_lora.py --train data/decomp_train.jsonl --dev data/decomp_dev.jsonl --out models/decomp_1.5b --epochs 2
"""
import argparse
import hashlib
import json
import os
import random
import re
import sys
import time

import torch
from peft import LoraConfig, PeftModel, get_peft_model
from transformers import AutoModelForCausalLM, AutoTokenizer

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
SYSTEM = ("Split the question into sub-questions. Output 'NA' if it needs no bridge entity (comparison or single fact). "
          "Otherwise output 'H1: <first sub-question naming the entity from the question with its qualifiers>' and on the next line "
          "'H2: <second sub-question with #1 where the answer to H1 goes>' (or 'H2: NA' if one sub-question is enough). Nothing else.")


def chat(tok, q, out=None):
    msgs = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": q}]
    prompt = tok.apply_chat_template(msgs, add_generation_prompt=True, tokenize=False)
    return prompt if out is None else prompt + out + tok.eos_token


def caps(q):
    return [c for c in re.findall(r"\b[A-Z][\w'\-]+(?:\s+[A-Z][\w'\-]+)*", q) if len(c) > 3]


def parse(text):
    """-> None (unparseable) | "NA" | (h1, h2 or None)"""
    t = text.strip()
    if t == "NA":
        return "NA"
    m = re.match(r"H1:\s*(.+?)\s*(?:\nH2:\s*(.+))?$", t, re.S)
    if not m:
        return None
    h1 = m.group(1).strip(); h2 = (m.group(2) or "").strip()
    if "\n" in h1:
        return None
    return h1, (None if h2 in ("", "NA") else h2)


def anchor_ok(q, p):
    return p == "NA" or (p is not None and any(c in p[0] for c in caps(q)))


@torch.no_grad()
def generate(model, tok, q, max_new=96):
    ids = tok(chat(tok, q), return_tensors="pt", add_special_tokens=False)["input_ids"].cuda()
    out = model.generate(ids, max_new_tokens=max_new, do_sample=False, pad_token_id=tok.pad_token_id)
    return tok.decode(out[0, ids.shape[1]:], skip_special_tokens=True).strip()


def eval_dev(model, tok, rows, verbose=False):
    n = len(rows); parses = anchors = na_agree = 0
    for r in rows:
        pred = generate(model, tok, r["question"])
        p, k = parse(pred), parse(r["decomp"])
        parses += p is not None
        anchors += anchor_ok(r["question"], p) and p is not None
        na_agree += ((p == "NA") == (k == "NA")) if r["decomp"] else 0     # unlabelled dev rows: parse/anchor tiers only
        if verbose:
            print(f"  {r['question'][:70]!r} -> {pred[:90]!r}", flush=True)
    s = {"n": n, "parses": parses, "anchor_kept": anchors, "na_agree": na_agree}
    print("dev:", s, flush=True)
    return s


def batches(tok, pairs, bs):
    for s in range(0, len(pairs), bs):
        chunk = pairs[s:s + bs]
        texts = [chat(tok, q, o) for q, o in chunk]; prompts = [chat(tok, q) for q, _ in chunk]
        enc = tok(texts, return_tensors="pt", padding=True, add_special_tokens=False)
        labels = enc["input_ids"].clone()
        for i, p in enumerate(prompts):
            labels[i, :len(tok(p, add_special_tokens=False)["input_ids"])] = -100
        labels[enc["attention_mask"] == 0] = -100
        yield {k: v.cuda() for k, v in enc.items()}, labels.cuda()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="Qwen/Qwen2.5-1.5B-Instruct")
    ap.add_argument("--train", required=True)
    ap.add_argument("--dev", default=None, help="labelled jsonl (question, decomp) for the dev tiers; never a held-out slice")
    ap.add_argument("--out", required=True)
    ap.add_argument("--epochs", type=float, default=2)
    ap.add_argument("--bs", type=int, default=4)
    ap.add_argument("--accum", type=int, default=4)
    ap.add_argument("--lr", type=float, default=2e-4)
    ap.add_argument("--rank", type=int, default=16)
    ap.add_argument("--rep-hand", type=int, default=5, help="repeat rows whose source starts with 'hand'")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--sanity", default="50:2.0,100:1.0,200:0.6")
    ap.add_argument("--eval-only", action="store_true")
    ap.add_argument("--eval-verbose", action="store_true")
    ap.add_argument("--allow-unstamped", action="store_true")
    args = ap.parse_args()
    torch.manual_seed(args.seed); random.seed(args.seed)
    tok = AutoTokenizer.from_pretrained(args.base); tok.padding_side = "right"
    model = AutoModelForCausalLM.from_pretrained(args.base, torch_dtype=torch.bfloat16, attn_implementation="sdpa").cuda()
    dev = [json.loads(l) for l in open(args.dev, encoding="utf-8")] if args.dev else []
    if args.eval_only:
        model = PeftModel.from_pretrained(model, args.out).eval()
        eval_dev(model, tok, dev, args.eval_verbose); return
    if not args.allow_unstamped:
        stamp = args.train + ".provenance.json"
        assert os.path.exists(stamp), f"no provenance stamp for {args.train}"
        st = json.load(open(stamp))
        assert st["verdict"] == "CLEAN" and st["sha256"] == hashlib.sha256(open(args.train, "rb").read()).hexdigest(), "stamp mismatch"
        print("provenance stamp OK", st["utc"], flush=True)
    rows = [json.loads(l) for l in open(args.train, encoding="utf-8")]
    pairs = []
    for r in rows:
        pairs += [(r["question"], r["decomp"])] * (args.rep_hand if str(r.get("source", "")).startswith("hand") else 1)
    cfg = LoraConfig(r=args.rank, lora_alpha=2 * args.rank, lora_dropout=0.05, task_type="CAUSAL_LM",
                     target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"])
    model = get_peft_model(model, cfg); model.print_trainable_parameters()
    opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=args.lr, weight_decay=0.0)
    steps_per_epoch = (len(pairs) + args.bs * args.accum - 1) // (args.bs * args.accum); total = int(steps_per_epoch * args.epochs)
    sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: min(1.0, (s + 1) / 50) * max(0.05, 1 - s / max(1, total)))
    bands = sorted((int(k), float(v)) for k, v in (kv.split(":") for kv in args.sanity.split(",") if kv))
    model.train(); t0 = time.time(); step = micro = 0; ema = None
    print(f"pairs {len(pairs)} steps {total}", flush=True)
    os.makedirs(args.out, exist_ok=True)
    while step < total:
        random.shuffle(pairs)
        for enc, labels in batches(tok, pairs, args.bs):
            out = model(**enc, labels=labels); (out.loss / args.accum).backward(); micro += 1
            if micro % args.accum:
                continue
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); opt.step(); sched.step(); opt.zero_grad(set_to_none=True); step += 1
            loss_now = out.loss.item(); ema = loss_now if ema is None else 0.9 * ema + 0.1 * loss_now
            breach = "NaN loss" if loss_now != loss_now else next((f"ema {ema:.3f} > {b_max} at step {step}" for b_step, b_max in bands if step >= b_step and ema > b_max), None)
            if breach:
                json.dump({"step": step, "breach": breach}, open(os.path.join(args.out, "drift_alert.json"), "w")); print("ALERT", breach, flush=True)
                if breach == "NaN loss":
                    return
            if step % 25 == 0:
                el = time.time() - t0
                json.dump({"step": step, "total": total, "loss": round(loss_now, 4), "ema_loss": round(ema, 4), "elapsed_s": round(el), "eta_s": round(el / step * (total - step)),
                           "sanity_ok": breach is None, "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}, open(os.path.join(args.out, "heartbeat.json"), "w"))
                print(f"step {step}/{total} loss {loss_now:.4f} ema {ema:.4f} {el:.0f}s", flush=True)
            if step >= total:
                break
    model.save_pretrained(args.out); model.eval()
    s = eval_dev(model, tok, dev, args.eval_verbose) if dev else None
    json.dump({"dev": s, "args": vars(args), "train_seconds": time.time() - t0}, open(os.path.join(args.out, "eval.json"), "w"), indent=1)
    print(f"saved {args.out} {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
