"""Tier an adapter on any hand-labelled batch (structure / anchor / relations / na_ok), the same
definitions as tagger_lora.eval_real, for DEV batches that are not the eval slice.

    <local>/model-training/.venv/Scripts/python.exe scripts/tagger_tier.py --adapter models/tagger_v4clean_0.5b --labels data/tagger_real_160-199.jsonl
"""
import argparse
import json
import sys

import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, "scripts")
from tagger3b import parse, norm_ent  # noqa: E402
from tagger_lora import chat, generate  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--adapter", required=True)
    ap.add_argument("--labels", required=True)
    ap.add_argument("--base", default="Qwen/Qwen2.5-0.5B-Instruct")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    tok = AutoTokenizer.from_pretrained(args.base)
    model = AutoModelForCausalLM.from_pretrained(args.base, torch_dtype=torch.bfloat16, attn_implementation="sdpa").cuda()
    model = PeftModel.from_pretrained(model, args.adapter).eval()
    rows = [json.loads(l) for l in open(args.labels, encoding="utf-8")]
    out = []
    for r in rows:
        pred = generate(model, tok, r["question"], "cuda")
        k, p = parse(r["tag"]), parse(pred)
        na_ok = (k == "NA") == (p == "NA")
        struct = ent = rel = False
        if k != "NA" and p not in ("NA", None):
            struct = len(p[0]) == len(k[0]) and (p[2] is None) == (k[2] is None)
            ent = norm_ent(p[1]) == norm_ent(k[1]) or norm_ent(k[1]) in norm_ent(p[1]) or norm_ent(p[1]) in norm_ent(k[1])
            rel = p[0] == k[0] and p[2] == k[2]
        elif k == "NA" and p == "NA":
            struct = ent = rel = True
        out.append({"doc": r.get("doc"), "pred": pred, "key": r["tag"], "parses": p is not None, "na_ok": na_ok, "struct": struct, "anchor": ent, "rel": rel})
        print(f"  doc {r.get('doc')} | {pred[:58]:<58s} | key {r['tag'][:48]:<48s} | struct {int(struct)} ent {int(ent)} rel {int(rel)}", flush=True)
    n = len(out)
    summary = {"n": n, "parses": sum(x["parses"] for x in out), "na_ok": sum(x["na_ok"] for x in out), "struct": sum(x["struct"] for x in out),
               "anchor": sum(x["anchor"] for x in out), "relations": sum(x["rel"] for x in out), "adapter": args.adapter, "labels": args.labels}
    print("tiers:", summary, flush=True)
    if args.out:
        json.dump({"summary": summary, "rows": out}, open(args.out, "w"), indent=1)


if __name__ == "__main__":
    main()
