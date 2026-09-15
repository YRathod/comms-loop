"""Provenance check for the tagger generator (NO CHEATING rule 1): nothing on the source side may be
traceable to the scored eval docs. Three mechanical legs, all must be zero:

  1. pool items (names, places, orgs, codes, descriptors, modifiers, filter phrasings) found verbatim
     (lowercase substring) in any question of docs 0-39;
  2. relation / clause templates whose fixed spans of >= 3 words occur in any question of docs 0-39;
  3. eval anchors (from tagger3b.KEY) occurring as substrings of the generated training questions.

    .venv/Scripts/python scripts/tagger_data_check.py data/tagger_train_v4.jsonl
"""
import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, "scripts")
import tagger_data as G  # noqa: E402
from tagger3b import KEY, parse, norm_ent  # noqa: E402

ROWS = [json.loads(l) for l in open(r"C:\dev\research\memory-challange\long-bench\data\data\hotpotqa.jsonl", encoding="utf-8")][:40]
Q = {i: " ".join(ROWS[i]["input"].lower().split()) for i in range(0, 40)}


def n(s):
    return " ".join(s.lower().split())


STOP = {"of", "the", "a", "an", "in", "on", "for", "to", "and", "is", "was", "are", "were", "what", "which", "who", "by", "at",
        "from", "that", "this"}


def content_3grams(text):
    """identical to comms-loop/scripts/alignment_gate.py leg 1b (kimi, v1.14): 3-grams with >= 2 non-stop tokens"""
    w = re.findall(r"[a-z0-9]+", text.lower())
    return {tuple(w[i:i + 3]) for i in range(len(w) - 2) if sum(1 for t in w[i:i + 3] if t not in STOP) >= 2}


def found(item, q):
    """single words must match as whole words; multi-word items as substrings"""
    return re.search(r"" + re.escape(n(item)) + r"", q) is not None if " " not in item.strip() else n(item) in q


def main():
    bad = 0
    pools = {k: getattr(G, k) for k in ("FIRST", "LAST", "ADJ", "NOUN", "PLACES", "ORGS", "CODES", "DESCRIPTORS", "OOV_MODIFIERS") if hasattr(G, k)}
    for k, pool in pools.items():
        hits = [(w, [i for i, q in Q.items() if found(w, q)]) for w in pool]
        hits = [h for h in hits if h[1]]
        print(f"leg 1 {k}: {len(hits)} of {len(pool)} in eval questions", hits[:8])
        bad += len(hits)
    for fk, forms in G.FILTERS.items():
        for w in forms:
            docs = [i for i, q in Q.items() if found(w, q) and len(w.split()) > 1]
            if docs:
                print("leg 1 FILTERS:", w, docs); bad += 1
    tmpl = []
    sources = list(G.RELS.items()) + [(f"CLAUSE:{r}", (v, [])) for r, v in G.CLAUSE.items()]
    for rel, (nom, qf) in sources:
        for t in nom + qf:
            g = content_3grams(t.replace("{x}", " "))
            docs = [i for i, q in Q.items() if g & content_3grams(q)]
            if docs:
                tmpl.append((rel, t, docs))
    print(f"leg 2 templates sharing a content 3-gram with an eval question: {len(tmpl)}", tmpl[:10])
    bad += len(tmpl)
    if len(sys.argv) > 1:
        tq = "\n".join(json.loads(l)["question"].lower() for l in open(sys.argv[1], encoding="utf-8"))
        anch = []
        for i in range(3, 40):
            k = parse(KEY[i])
            if k not in ("NA", None):
                e = norm_ent(k[1])
                if e and e.lower() in tq:
                    anch.append((i, k[1]))
        print(f"leg 3 eval anchors in training questions: {len(anch)}", anch)
        bad += len(anch)
        # leg 4: distribution (kimi's v1.14 leg): share of training questions sharing a content 3-gram with any eval question
        eg = set().union(*(content_3grams(q) for q in Q.values()))
        tqs = [json.loads(l)["question"] for l in open(sys.argv[1], encoding="utf-8")]
        share = sum(bool(content_3grams(q) & eg) for q in tqs) / len(tqs)
        print(f"leg 4 distribution: {share:.2%} of training questions share a content 3-gram with an eval question (FAIL > 2%, SUSPECT > 0.5%)")
        bad += 1 if share > 0.005 else 0
    print("PROVENANCE CHECK:", "CLEAN" if bad == 0 else f"FAIL ({bad} hits)")
    if len(sys.argv) > 1:
        import hashlib, time, os
        stamp = sys.argv[1] + ".provenance.json"
        if bad == 0:
            json.dump({"file": sys.argv[1], "sha256": hashlib.sha256(open(sys.argv[1], "rb").read()).hexdigest(), "verdict": "CLEAN",
                       "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "checker": "scripts/tagger_data_check.py"}, open(stamp, "w"), indent=1)
            print("stamp written:", stamp)
        elif os.path.exists(stamp):
            os.remove(stamp); print("stale stamp removed:", stamp)
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
