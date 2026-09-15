"""Build a fresh held-out slice from the HotpotQA distractor dev set in the LongBench format, excluding
LongBench docs 0-199 (by question text) and every id in the given files; hash it and write <out>.meta.json.

    python scripts/build_slice.py --seed 20260918 --n 400 --out data/hotpot_heldout_v5.jsonl --exclude data/hotpot_heldout_v1.jsonl ... --key "KEYS.md #11"
"""
import argparse
import collections
import hashlib
import json
import random
import sys
import time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def n(s):
    return " ".join(s.lower().split())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--n", type=int, default=400)
    ap.add_argument("--out", required=True)
    ap.add_argument("--exclude", nargs="*", default=[])
    ap.add_argument("--key", default="")
    ap.add_argument("--raw", default="data/hotpot_distractor_validation.jsonl")
    ap.add_argument("--longbench", default=r"C:\dev\research\memory-challange\long-bench\data\data\hotpotqa.jsonl")
    a = ap.parse_args()
    raw = [json.loads(l) for l in open(a.raw, encoding="utf-8")]
    forbidden_q = {n(json.loads(l)["input"]) for l in open(a.longbench, encoding="utf-8")}
    used = set()
    for f in a.exclude:
        used |= {json.loads(l)["_id"] for l in open(f, encoding="utf-8")}
    pool = [r for r in raw if n(r["question"]) not in forbidden_q and r["id"] not in used]
    rng = random.Random(a.seed)
    sel = rng.sample(pool, a.n); sel_ids = {r["id"] for r in sel}
    others = [r for r in pool if r["id"] not in sel_ids]

    def para(t, s):
        return t + "\n" + " ".join(x.strip() for x in s)
    out = []
    for r in sel:
        paras = [para(t, s) for t, s in zip(r["titles"], r["sentences"])]
        for o in rng.sample(others, 8):
            paras += [para(t, s) for t, s in zip(o["titles"], o["sentences"])]
        rng.shuffle(paras)
        out.append({"input": r["question"], "context": "\n\n".join(paras), "answers": [r["answer"]], "_id": r["id"], "type": r["type"], "level": r["level"]})
    with open(a.out, "w", encoding="utf-8") as f:
        for o in out:
            f.write(json.dumps(o, ensure_ascii=False) + "\n")
    h = hashlib.sha256(open(a.out, "rb").read()).hexdigest()
    meta = {"file": a.out, "sha256": h, "n": len(out), "seed": a.seed, "pool_after_exclusions": len(pool), "excluded_files": a.exclude,
            "overlap_with_used_ids": len(sel_ids & used), "types": dict(collections.Counter(o["type"] for o in out)),
            "built_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "key": a.key}
    json.dump(meta, open(a.out.replace(".jsonl", ".meta.json"), "w"), indent=1)
    print(json.dumps(meta))


if __name__ == "__main__":
    main()
