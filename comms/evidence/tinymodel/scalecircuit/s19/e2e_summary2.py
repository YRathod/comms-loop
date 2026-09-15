import json, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
d = json.load(open(sys.argv[1], encoding="utf-8")); rows = d["rows"]; n = len(rows)
CLAIM = "f1_iterative_fallback"
W = [k for k in ("f1_sp", "f1_chain", "f1_retrieval", "f1_iterative", "f1_iterative_notes", "f1_superset", "f1_superset_notes", "f1_superset_fallback", "f1_select", CLAIM) if k in rows[0]]
sp = sum(r["f1_sp"] for r in rows) / n
band = sp + 0.05
print(f"n={n} single_pass={sp:.3f} band={band:.3f}")
for k in W[1:]:
    m = sum(r[k] for r in rows) / n
    wins = [(r["doc"], round(r[k] - r["f1_sp"], 2)) for r in rows if r[k] > r["f1_sp"] + 1e-9]
    losses = [(r["doc"], round(r[k] - r["f1_sp"], 2)) for r in rows if r[k] < r["f1_sp"] - 1e-9]
    tag = "  <== CLAIMED" if k == CLAIM else ""
    print(f"{k[3:]:<20s} {m:.3f} ({m - sp:+.3f}) wins {len(wins)} losses {len(losses)}{tag}")
    if k == CLAIM:
        print("   wins:", wins); print("   losses:", losses)
        print("   verdict:", "PASS" if m >= band - 1e-9 else "FAIL", f"(claimed {m:.3f} vs band {band:.3f}, delta {m - band:+.3f})")
oracle = sum(max(r[k] for k in W) for r in rows) / n
print(f"oracle union {oracle:.3f} (+{oracle - sp:.3f})")
if "select_how" in rows[0]:
    import collections; print("select_how:", collections.Counter(r["select_how"] for r in rows))
print("fallback fired on:", [r["doc"] for r in rows if r.get("iterative_fallback") != r.get("iterative")])
