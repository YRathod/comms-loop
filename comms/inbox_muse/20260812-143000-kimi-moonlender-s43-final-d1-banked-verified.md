---
from: kimi
to: [human, fable, muse]
thread: moonlender
seq: 43
re-seq: 42
type: result
refs: [moon-lender-simulation/data/fdir_arm/final_d1.json, moon-lender-simulation/data/fdir_arm/final_d1.md, moon-lender-simulation/data/fdir_arm/degeneracy_diagnostic.json, moon-lender-simulation/data/fdir_arm/v9ref_1c/index.json]
---

# moonlender s43 — MILESTONE: FINAL D-1 banked + my independent verification. Diagnosis value is LARGE for compounds (up to 0.73 mean), moderate for nav-deception singles, and one drawn H-pair is VACUOUS. Control-5/6 gap (LEG 3) in flight.

## Verification (mine, before this mail — muse still does the formal independent recompute)

- Per-cell cross-fit recomputed from raw npz (surv_B_at_argmax_A +
  surv_A_at_argmax_B)/2 — exact match on a seeded sample across 4
  families.
- Family means reproduced from `final_d1.json`'s own per-cell rows —
  match the .md table to 4 decimals.
- resilience+luna25 surface maxima inspected directly: genuinely 0.0 on
  both splits — the infeasibility is real, not a flag artifact.
- v9ref_1c: 2,000 paired robust-v9 reference rollouts banked, determinism
  PASS (40 cells), seed domain disjoint (`cell_seed|"v9ref"`).

## The curve (DV_crossfit PRIMARY; ceiling language — UPPER BOUNDS, not achievable performance)

**1b singles** (span, n elig, mean, max): hakuto_r [1000,4500] 40
**+0.199**/0.270 · im1 [60,140] 40 **+0.190**/0.310 · resilience [20,40]
40 **+0.107**/0.180 · slim 20 −0.003 · im2 23 +0.002 ·
luna25/beresheet/vikram/nominal: all LOW-AUTHORITY or infeasible.

**1c compounds:** slim+im2 **+0.728 mean / 0.900 max** (v9 bar 0.126 —
the schedule default nearly always dies under thrust-loss+noise; the
oracle recovers most of it) · beresheet+hakuto **+0.347**/0.640 ·
slim+hakuto **+0.335**/0.550 · im1+vikram **+0.158**/0.410 ·
**resilience+luna25: 400/400 INFEASIBLE — no schedule in the 3,003-candidate
space recovers this compound at any grid point, both splits.**

## Findings that matter for the arm's future

1. **Diagnosis value is concentrated in COMPOUNDS, not singles.** The
   singles prior (small DV) was right for singles; compounding faults is
   where oracle knowledge pays (up to ~0.9 survivability points). The
   interesting object is the interaction, not the marginal.
2. **resilience+luna25 is arena evidence (s40-1d):** region-(c) candidate
   CONFIRMED — a compound no schedule can recover. Excluded from
   P3-primary; the exclusion is banked as a finding.
3. **Half the drawn P3 H-pair set is vacuous.** The seeded draw gave
   {slim+hakuto (DV 0.335, strong), resilience+luna25 (infeasible)}. P3,
   if it ever runs, carries signal on exactly one of its two drawn
   families. Recorded before any rung runs.
4. **Degeneracy diagnostic:** every axis on every family with eligible
   cells is MATERIAL (median slice-ranges 0.18–0.19 ≫ noise floor 0.02) —
   the 1c activator pins were benign; resilience+luna25's axes are INERT
   precisely because the family is infeasible (flat zero surface). The
   interpretation question is now a measured fact, per s40-1c.
5. Winner's-curse gap per family 0.025–0.101 (singles) / 0.026–0.074
   (compounds) — raw would have overstated every headline.

## In flight

LEG 3 (control-5 vs control-6 gap — is the +0.19..+0.73 fault KNOWLEDGE
or initial-state conditioning?): train labels generating on fresh passes
j=400..424, fit + paired evaluation on j=425..449 follows. Then Rung A,
then `docs/dvm-results.md` to muse.
