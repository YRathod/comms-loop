"""Content filter for GENERATED training text (teacher / model-written labels): PII and harmful-content
patterns. Rows that match are dropped and counted; the counts are printed and written next to the
file so the safety case can cite them. Conservative on purpose: a false drop costs one row.

    python scripts/content_filter.py data/decomp_teacher_train.jsonl --fields question decomp
"""
import argparse
import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
PATTERNS = {
    "email": re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"),
    "phone": re.compile(r"\b(?:\+?\d{1,3}[\s-]?)?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{4}\b"),
    "ssn_like": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "card_like": re.compile(r"\b(?:\d[ -]?){13,16}\b"),
    "street_address": re.compile(r"\b\d{1,5}\s+(?:[A-Z][a-z]+\s){1,3}(?:Street|St\.|Avenue|Ave\.|Road|Rd\.|Drive|Dr\.|Lane|Boulevard|Blvd\.)\b"),
    "harm_instruction": re.compile(r"\b(how to (?:make|build|synthesi[sz]e) (?:a )?(?:bomb|explosive|nerve agent|poison)|kill (?:yourself|himself|herself))\b", re.I),
    "sexual_minor": re.compile(r"\b(child|minor|underage)\b.{0,40}\b(sex|sexual|nude|porn)\b|\b(sex|sexual|nude|porn)\b.{0,40}\b(child|minor|underage)\b", re.I),
    "slur_or_abuse": re.compile(r"\b(n[i1]gg(?:er|a)s?|f[a@]gg?ots?|k[i1]kes?|sp[i1]cs?|ch[i1]nks?|tr[a@]nn(?:y|ies))\b", re.I),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--fields", nargs="+", default=["question", "decomp"])
    ap.add_argument("--out", default=None, help="filtered output (default: overwrite in place)")
    args = ap.parse_args()
    rows = [json.loads(l) for l in open(args.path, encoding="utf-8")]
    counts = {k: 0 for k in PATTERNS}
    keep, dropped = [], []
    for r in rows:
        text = " ".join(str(r.get(f, "")) for f in args.fields)
        hits = [k for k, p in PATTERNS.items() if p.search(text)]
        if hits:
            for k in hits:
                counts[k] += 1
            dropped.append({"id": r.get("id"), "hits": hits})
        else:
            keep.append(r)
    out = args.out or args.path
    with open(out, "w", encoding="utf-8") as f:
        for r in keep:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    report = {"file": args.path, "rows_in": len(rows), "rows_kept": len(keep), "rows_dropped": len(dropped), "counts": counts, "dropped": dropped[:50]}
    json.dump(report, open(args.path + ".content_filter.json", "w"), indent=1)
    print(f"content filter: {len(rows)} in, {len(keep)} kept, {len(dropped)} dropped; counts {counts}")


if __name__ == "__main__":
    main()
