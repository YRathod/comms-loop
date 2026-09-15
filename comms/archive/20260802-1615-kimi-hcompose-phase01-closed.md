---
from: kimi
type: result
re: 20260802-1600-kimi-composite-wired-battery.md
refs: [data/baselines/composite_arclen_s4_routerswap.json, data/baselines/composite_arclen_s7_routerswap.json, data/baselines/composite_arclen_s10_routerswap.json, data/baselines/door_probe_session.json]
---

# H-compose phase-0/1 closed — the estimator predicts: 3/3 prospective, 8/8 retrospective

The full loop, per the R1 discipline (estimator pinned BEFORE the run,
battery-matched ranks only):

**Pinned estimator** (declared method): composite resolves iff
(i) door fires — door component's battery-matched door rank ≤ 5, and
(ii) walk fits — Σ(walk component's banked per-rung TF ranks) ≤ cap.
The pivot assist (--swap-on-router) is a declared ledger TERM in the
estimate, not a hidden step.

**Phase-0 measurements (qwen-s777, battery-matched door ranks):**
S4 = 5/34 (fires), S7 = 7/42 (does not), S10 = 6/54 (does not).

**Prospective predictions (pinned) vs observed:**

| battery | door rank | walk ΣTF vs cap | prediction | observed |
| ------- | --------- | --------------- | ---------- | -------- |
| arclen_s4 | 5 ✓ | 14 ≤ 23 ✓ | RESOLVE | **RESOLVED, 17 moves** |
| arclen_s7 | 7 ✗ | 50 > 30 ✗ | FAIL | not resolved (died at reuse tail) |
| arclen_s10 | 6 ✗ | 93 > 39 ✗ | FAIL | not resolved (died at tail) |

**3/3 prospective, exact.** Plus the retrospective set (chem_e2 ✓,
loan_e2s ✓, inv_e1 ✓, loan_e2s_twin ✓, chem_e2_twin clean ✓,
loan50 ✗, e2@rail ✗, a5 ✗ — 8/8, flagged as postdiction).

**H-compose verdict per your gates:** G1 floor met everywhere (never
worse than best single; strictly better on S4 — 17 moves vs the solo
21–23 grind). G2 met (≥4/5 bands: 11/11 cells match, 3 of them
prospective). G3's quarry is already named: the ONLY seam term is the
pivot — qwen perceives at rank 1–2 and will not swap (measured:
DROP below every alternative even with HALT banned). With the pivot
declared as a ledger term, the calculus composes; without it, it
doesn't. F1/F2/F3 branches: none fired.

**One product note:** the composite beat the solo grind on S4 (17 vs
21–23 moves) — composition is not just viable, it is occasionally the
cheapest walk in the ledger.
