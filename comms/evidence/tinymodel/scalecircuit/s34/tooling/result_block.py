"""Mechanical result block for comms mails: every number comes from the frozen pipeline JSON, never typed.

    python scripts/result_block.py <pipeline_json> --claim f1_iterative_fallback [--slice data/hotpot_heldout_v1.jsonl] [--band 0.05] [--out block.md]

Prints (and optionally writes) a markdown block: wiring table with deltas, wins/losses, band verdict for the
claimed wiring, bootstrap 95% CI + P(delta >= band) per wiring, and a by-type split when the slice file
carries a "type" field. Paste the block into the mail unchanged (s32 rule: freeze, cat, paste).
"""
import argparse
import collections
import json
import random
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
NAMES = {"f1_sp": "single-pass baseline", "f1_chain": "chain", "f1_retrieval": "retrieval", "f1_iterative": "iterative",
         "f1_iterative_notes": "iterative + notes", "f1_superset": "superset", "f1_superset_notes": "superset + notes",
         "f1_superset_fallback": "superset + fallback", "f1_select": "select (agree / judge / sp)", "f1_iterative_fallback": "iterative + shape fallback"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json")
    ap.add_argument("--claim", required=True)
    ap.add_argument("--slice", default=None, help="jsonl with a 'type' field per doc index (for the by-type split)")
    ap.add_argument("--band", type=float, default=0.05)
    ap.add_argument("--boot", type=int, default=20000)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    d = json.load(open(args.json, encoding="utf-8")); rows = d["rows"]; n = len(rows)
    W = [k for k in NAMES if k in rows[0]]
    sp = sum(r["f1_sp"] for r in rows) / n
    band = sp + args.band
    L = [f"Source: `{args.json}` (n={n}), claimed wiring `{args.claim}`, band = single-pass + {args.band:.2f} = {band:.3f}.", "",
         "| wiring | mean F1 | delta | wins / losses | 95% CI of delta | P(delta >= band) | status |", "|---|---|---|---|---|---|---|"]
    rng = random.Random(0)
    for k in W:
        m = sum(r[k] for r in rows) / n
        if k == "f1_sp":
            L.append(f"| {NAMES[k]} | {m:.3f} | - | - | - | - | baseline |"); continue
        dl = [r[k] - r["f1_sp"] for r in rows]
        wins = sum(x > 1e-9 for x in dl); losses = sum(x < -1e-9 for x in dl)
        bs = sorted(sum(dl[rng.randrange(n)] for _ in range(n)) / n for _ in range(args.boot))
        lo, hi = bs[int(0.025 * args.boot)], bs[int(0.975 * args.boot)]
        p = sum(1 for x in bs if x >= args.band) / args.boot
        if k == args.claim:
            status = f"**CLAIMED: {'PASS' if m >= band - 1e-9 else 'FAIL'} by {abs(m - band):.3f}**"
        else:
            status = "diagnostic"
        L.append(f"| {'**' if k == args.claim else ''}{NAMES[k]}{'**' if k == args.claim else ''} | {m:.3f} | {m - sp:+.3f} | {wins} / {losses} | [{lo:+.3f}, {hi:+.3f}] | {p:.2f} | {status} |")
    oracle = sum(max(r[k] for k in W) for r in rows) / n
    L.append(f"| oracle union | {oracle:.3f} | {oracle - sp:+.3f} | | | | D2 diagnostic |")
    if args.slice:
        srows = [json.loads(l) for l in open(args.slice, encoding="utf-8")]
        if "type" in srows[0]:
            L += ["", "| type | n | single-pass | claimed | NA-tagged | docs where claimed != single-pass |", "|---|---|---|---|---|---|"]
            for t in sorted({s["type"] for s in srows}):
                rs = [r for r in rows if srows[r["doc"]]["type"] == t]
                if not rs:
                    continue
                na = sum(1 for r in rs if str(r["tag"]).upper().startswith("NA"))
                diff = sum(1 for r in rs if abs(r[args.claim] - r["f1_sp"]) > 1e-9)
                L.append(f"| {t} | {len(rs)} | {sum(r['f1_sp'] for r in rs)/len(rs):.3f} | {sum(r[args.claim] for r in rs)/len(rs):.3f} | {na} | {diff} |")
    if "select_how" in rows[0]:
        L.append(""); L.append("select_how: " + ", ".join(f"{k} {v}" for k, v in collections.Counter(r["select_how"] for r in rows).items()))
    block = "\n".join(L)
    print(block)
    if args.out:
        open(args.out, "w", encoding="utf-8").write(block + "\n")


if __name__ == "__main__":
    main()
