"""Teacher decompositions for the free-form decomposer (key #10 exception): the frozen local
Qwen2.5-3B-Instruct writes H1/H2 for HotpotQA TRAIN-split questions only. Mechanical filters: H1 must
contain a capitalised span of the question; H2 must contain "#1"; NA allowed for comparison / single-hop.

    python scripts/decomp_teacher.py --n 3000 --seed 20260914 --out data/decomp_teacher_train.jsonl
"""
import argparse
import json
import random
import re
import sys
import time

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
SYSTEM = ("You split a multi-hop question into sub-questions a search engine can answer one at a time. "
          "Output exactly two lines: 'H1: <first sub-question, naming the entity from the question with its qualifiers>' "
          "and 'H2: <second sub-question, writing #1 where the answer to H1 goes>', or 'H2: NA' if H1 already answers the question. "
          "If the question compares two named things, or needs no bridge entity, output the single line 'NA'. No other text.")
FEW = [("Which 1983 Nissan-sponsored race did race car driver Jeff Wood make his CART debut at?",
        "H1: Which race did race car driver Jeff Wood make his CART debut at?\nH2: Which 1983 Nissan-sponsored race was #1?"),
       ("Who did an actress from The Secret of NIMH play in A Patch of Blue?",
        "H1: Which actress was in the film The Secret of NIMH?\nH2: Who did #1 play in A Patch of Blue?"),
       ("Were Scott Derrickson and Ed Wood of the same nationality?", "NA")]


def caps(q):
    return re.findall(r"\b[A-Z][\w'\-]+(?:\s+[A-Z][\w'\-]+)*", q)


def valid(q, out):
    if out.strip() == "NA":
        return True
    m = re.match(r"H1:\s*(.+)\nH2:\s*(.+)$", out.strip(), re.S)
    if not m:
        return False
    h1, h2 = m.group(1).strip(), m.group(2).strip()
    return any(c in h1 for c in caps(q) if len(c) > 3) and (h2.strip() == "NA" or "#1" in h2) and "\n" not in h1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=3000)
    ap.add_argument("--seed", type=int, default=20260914)
    ap.add_argument("--train", default="data/hotpot_distractor_train.jsonl")
    ap.add_argument("--out", default="data/decomp_teacher_train.jsonl")
    ap.add_argument("--skip-ids", default=None, help="jsonl of rows whose ids must not be used (the hand-label set)")
    ap.add_argument("--teacher", default="Qwen/Qwen2.5-3B-Instruct")
    args = ap.parse_args()
    rows = [json.loads(l) for l in open(args.train, encoding="utf-8")]
    skip = {json.loads(l)["id"] for l in open(args.skip_ids, encoding="utf-8")} if args.skip_ids else set()
    rng = random.Random(args.seed)
    cand = [r for r in rows if r["id"] not in skip]
    rng.shuffle(cand)
    tok = AutoTokenizer.from_pretrained(args.teacher)
    model = AutoModelForCausalLM.from_pretrained(args.teacher, torch_dtype=torch.bfloat16, attn_implementation="sdpa").cuda().eval()
    kept, tried, t0 = 0, 0, time.time()
    with open(args.out, "w", encoding="utf-8") as f:
        for r in cand:
            if kept >= args.n:
                break
            tried += 1
            msgs = [{"role": "system", "content": SYSTEM}]
            for q, a in FEW:
                msgs += [{"role": "user", "content": q}, {"role": "assistant", "content": a}]
            msgs.append({"role": "user", "content": r["question"]})
            ids = tok(tok.apply_chat_template(msgs, add_generation_prompt=True, tokenize=False), return_tensors="pt", add_special_tokens=False)["input_ids"].cuda()
            with torch.no_grad():
                out = model.generate(ids, max_new_tokens=80, do_sample=False)
            text = tok.decode(out[0, ids.shape[1]:], skip_special_tokens=True).strip()
            if valid(r["question"], text):
                f.write(json.dumps({"id": r["id"], "question": r["question"], "decomp": text, "type": r["type"], "source": "teacher:Qwen2.5-3B-Instruct", "split": "train"}, ensure_ascii=False) + "\n")
                kept += 1
            if tried % 200 == 0:
                print(f"tried {tried} kept {kept} ({time.time()-t0:.0f}s)", flush=True)
    print(f"done: kept {kept} of {tried} tried ({time.time()-t0:.0f}s) -> {args.out}", flush=True)


if __name__ == "__main__":
    main()
