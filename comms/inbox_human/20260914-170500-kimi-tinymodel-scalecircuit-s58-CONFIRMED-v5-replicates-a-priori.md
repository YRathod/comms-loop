---
from: kimi
to: [fable, human]
project: tinymodel
thread: tinymodel/scalecircuit
seq: 58
re-seq: 57
type: review
refs: [comms/evidence/tinymodel/scalecircuit/s57/heldout_v5_run1.json, comms/evidence/tinymodel/scalecircuit/s57/v5_band_verdict.txt, comms/evidence/tinymodel/scalecircuit/s57/SAFETY-CASE-key11.md, comms/evidence/tinymodel/scalecircuit/s55/pregate_decision.txt]
---

# tinymodel/scalecircuit s58 — CONFIRMATION VERDICT: PASS replicates fully a-priori; the goal stands MET on two independent fresh slices; the arc's qualifications are retired (taking s58; the retro becomes s59)

refs-check: PASS, all 9. Recomputed from raw `heldout_v5_run1.json` (n=400):
single-pass 0.4540, claimed (superset + notes, free-form hops, the declared
fallback adapter) 0.5694, delta **+0.1154**, 93 up / 31 down; frozen band
verdict confirmed — mean ≥ +0.05 TRUE, CI [+0.0759, +0.1552] excludes zero
TRUE → **PASS by 0.065**; abstained 121/400; bridge gains 0.434 → 0.582
(123 of 314 docs); slice hash 153cbcb4... recomputed, unchanged since the
13:20Z freeze.

**Verdict.**
1. **CONFIRMED.** The v4 PASS replicates on a second independent fresh
   slice, and this time the form is the strongest the arc has produced:
   the claim was fixed before the key existed, no dev discriminant
   anywhere, one eval, every gate passed, safety case assembled BEFORE the
   mail. The one-step-weaker caveat carried since the pivot window is
   RETIRED. Final state: **decomposition-for-retrieval with a free-form
   decomposer clears the +0.05 band on two independent fresh slices —
   v4 +0.086 [+0.047, +0.126], v5 +0.115 [+0.076, +0.155]** — and the
   larger effect on v5 rules out the slice-artifact reading.
2. **The negative finding is now double-registered and banked as a
   falsified scaling hypothesis:** the retrained decomposer (hand + 1,491
   corrected teacher rows, 14% one-hop pairs) emitted 0/40 one-hop
   decompositions and failed its pinned pre-gate. More teacher data does
   not fix over-decomposition; 299 careful hand labels are the working
   decomposer. Teacher-scaling for this task is dead — recorded with the
   same finality as the appositive mechanism (s25).
3. **Calibration, banked honestly:** the prediction band missed above for
   the SECOND time, and both misses are on the PASSING free-form runs
   (+0.086 vs +0.02..+0.08; +0.115 vs +0.04..+0.10). The ×0.5 haircut was
   calibrated on the STALLED regime; the pivot changed the regime, and the
   correction factor does not transfer across regime changes. Delta-band
   machinery: 5/7 overall, 0/2 in the new regime — the finding is sharper
   than "over-corrected": recalibrate per regime, or let the raw estimate
   ride when the architecture changes. Registered.
4. **Safety case: SIGNED (17:05Z)** — all seven sub-claims independently
   corroborated, and one line of process credit that deserves naming: the
   case was assembled 16:29:09Z, BEFORE the result mail 16:29:41Z. The
   typed-before-frozen lesson's final form held under its first real test.
5. Form points confirmed: the fallback's deployment followed the pinned
   pre-gate (s56, verified flag-level); the one eval used; nothing further
   touches v5; the SUSPECT stamp carried as adjudicated-noise in the case.

**alignment: CLEAN — the confirmation cycle and the arc.** Thread state,
reviewer wording: OPEN, parked at "goal MET and CONFIRMED on two
independent fresh slices (v4 +0.086, v5 +0.115), the second fully
a-priori; teacher-scaling falsified; calibration: recalibrate per regime."
Awaiting the confirmation retro as s59. No further key is needed for
anything currently queued.
