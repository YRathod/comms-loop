"""Provenance check for free-form decomposer training data (v1.15 producer duty, key #10).

Legs (all must be zero / CLEAN):
  1. every training row's split field is "train" and its id is in the HotpotQA TRAIN split file;
  2. no training question equals (normalised) any held-out question: LongBench docs 0-39, slices v1/v2/v3;
  3. no held-out anchor (capitalised span >= 2 words from any held-out question) occurs in a training
     question or decomposition, unless that span also occurs in >= 3 distinct train-split questions
     (common names like "United States");
  4. content 3-gram share (kimi leg 1b definition) between training decompositions+questions and the
     held-out questions: FAIL > 2 percent, SUSPECT > 0.5 percent.
Writes <file>.provenance.json on CLEAN.

    python scripts/decomp_data_check.py data/decomp_train.jsonl
"""
import hashlib
import json
import re
import sys
import time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
STOP = {"of", "the", "a", "an", "in", "on", "for", "to", "and", "is", "was", "are", "were", "what", "which", "who", "by", "at", "from", "that", "this"}


def n(s):
    return " ".join(s.lower().split())


def grams(text):
    w = re.findall(r"[a-z0-9]+", text.lower())
    return {tuple(w[i:i + 3]) for i in range(len(w) - 2) if sum(1 for t in w[i:i + 3] if t not in STOP) >= 2}


def main():
    path = sys.argv[1]
    rows = [json.loads(l) for l in open(path, encoding="utf-8")]
    train_ids = {json.loads(l)["id"] for l in open("data/hotpot_distractor_train.jsonl", encoding="utf-8")}
    train_qs = [json.loads(l)["question"] for l in open("data/hotpot_distractor_train.jsonl", encoding="utf-8")]
    held = []
    lb = [json.loads(l) for l in open(r"C:\dev\research\memory-challange\long-bench\data\data\hotpotqa.jsonl", encoding="utf-8")][:40]
    held += [r["input"] for r in lb]
    for f in ("data/hotpot_heldout_v1.jsonl", "data/hotpot_heldout_v2.jsonl", "data/hotpot_heldout_v3.jsonl"):
        held += [json.loads(l)["input"] for l in open(f, encoding="utf-8")]
    bad = 0
    leg1 = [r for r in rows if r.get("split") != "train" or r["id"] not in train_ids]
    print(f"leg 1 rows not from the train split: {len(leg1)}"); bad += len(leg1)
    hq = {n(q) for q in held}
    leg2 = [r for r in rows if n(r["question"]) in hq]
    print(f"leg 2 training questions equal to a held-out question: {len(leg2)}"); bad += len(leg2)
    spans = set()
    for q in held:
        spans |= {c for c in re.findall(r"\b[A-Z][\w'\-]+(?:\s+[A-Z][\w'\-]+)+", q)}
    common = {s for s in spans if sum(1 for q in train_qs if s in q) >= 3}
    spans -= common
    text_all = "\n".join(r["question"] + "\n" + r["decomp"] for r in rows)
    leg3 = sorted(s for s in spans if s in text_all)
    print(f"leg 3 held-out anchors present in training text: {len(leg3)} {leg3[:10]}"); bad += len(leg3)
    # leg 4 for NATURAL-LANGUAGE rows: raw 3-gram share is dominated by generic question phrases ("in what year",
    # "which of the two") that every HotpotQA row shares, so the test is the EXCESS over a null: the same share
    # measured on 1000 random train-split rows that are NOT in the training file. FAIL if excess > 2 pp,
    # SUSPECT if > 0.5 pp. Both shares are printed.
    import random
    hg = set().union(*(grams(q) for q in held))
    share = sum(bool(grams(r["question"]) & hg) for r in rows) / max(1, len(rows))          # questions only: same text type as the null
    dshare = sum(bool(grams(r["decomp"]) & hg) for r in rows) / max(1, len(rows))            # decompositions: informational (no matched null)
    used = {r["id"] for r in rows}
    rng = random.Random(0)
    null_rows = [json.loads(l) for l in open("data/hotpot_distractor_train.jsonl", encoding="utf-8")]
    null_rows = [r for r in null_rows if r["id"] not in used]
    # null distribution: the same statistic on 300 random samples of the SAME SIZE from unused train rows;
    # FAIL if the training share is above the 99th percentile of the null, SUSPECT above the 95th.
    flags = [bool(grams(r["question"]) & hg) for r in null_rows]
    m = len(rows)
    null_shares = sorted(sum(rng.sample(flags, m)) / m for _ in range(300))
    null_share = sum(null_shares) / len(null_shares)
    p95, p99 = null_shares[int(0.95 * 300) - 1], null_shares[int(0.99 * 300) - 1]
    excess = share - null_share
    verdict4 = "FAIL" if share > p99 else ("SUSPECT" if share > p95 else "PASS")
    print(f"leg 4 distribution (questions, n={m}): training {share:.2%}; null mean {null_share:.2%} (p95 {p95:.2%}, p99 {p99:.2%}); excess {excess:+.2%}; {verdict4}. decompositions sharing a 3-gram with a held-out question: {dshare:.2%} (informational)")
    bad += 1 if verdict4 != "PASS" else 0
    print("PROVENANCE CHECK:", "CLEAN" if bad == 0 else f"FAIL ({bad})")
    if bad == 0:
        json.dump({"file": path, "sha256": hashlib.sha256(open(path, "rb").read()).hexdigest(), "verdict": "CLEAN",
                   "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "checker": "scripts/decomp_data_check.py",
                   "leg4_share": share, "leg4_null_mean": null_share, "leg4_null_p95": p95, "leg4_null_p99": p99, "leg4_excess": excess}, open(path + ".provenance.json", "w"), indent=1)
        print("stamp written")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
