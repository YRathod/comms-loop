---
from: human
to: [kimi, muse]
thread: moonlender
seq: 11
re-seq: 10
type: review-request
refs: [moon-lender-simulation/docs/prereg-fdir-schedule-v0.md, moon-lender-simulation/docs/fdir-arm-ladder-pending.md, moon-lender-simulation/baselines/step1_b.json, moon-lender-simulation/baselines/step1_c.json, moon-lender-simulation/baselines/step1a_crash_telemetry.json]
---

# moonlender s11 — STEP-2 PREREG drafted (PROSPECTIVE, zero data generated). Critique requested BEFORE first datum.

`docs/prereg-fdir-schedule-v0.md`. §§1–8 become immutable the moment the
first training datum is generated — so this is the last point at which
the design can be changed without an amendment record. **Nothing has been
generated. Nothing has been trained.**

## What it freezes

- **Claim:** telemetry → `(predicted survival → schedule params | ABSTAIN)`
  beating **robust-v9** on held-out severities AND held-out pairs, matched
  budget, no false-confidence.
- **Six controls**, all mandatory: robust-v9, hand rule-table,
  residual-checker, random-schedule (no-model floor), oracle-severity
  regressor (**ceiling**), false-fire negative control.
- **Reordering vs the old ladder:** the cheap-regressor smoothness gate
  (Rung A) now runs **BEFORE** the expensive 2D data generation. A jagged
  map kills the arm for minutes instead of ~5 hours.
- **Model-size ladder inverted:** start at the smallest thing that can
  pass; escalate to 124M only on a *failed gate*, never on preference.
  "Solved by a 30k-parameter regressor" is a preferred outcome.
- **Safety prediction P4** is independent of the performance prediction
  P3: false-confidence > 0.10 fails the arm *even if P3 passes*.
- **§8 absorbs the s4 review**: paired statistics primary and
  pre-registered this time (the R6 fix), per-episode dumps standard,
  n/seeds/config-hash in every artifact, search≠confirm seeds, no
  retro-edits, no seed-shopping, PVSG mandatory on prior-violating passes.
- **The s10 open inference is carried in §8 with its pinned ablation** —
  no design decision may rest on it until run.

## Where I most want the knife

1. **R-A — is the oracle-severity ceiling really a ceiling?** §6 argues the
   telemetry model cannot beat a clean-input regressor because it must
   *additionally* extract severity. Attack this: is there a case where raw
   telemetry carries schedule-relevant signal that the true-severity
   vector does NOT (e.g. terrain/geometry state)? If so the "ceiling"
   is not a ceiling and Rung A's kill criterion is wrong.
2. **R-B — thresholds.** 0.80 pass / 0.50 kill (Rungs A,B), +0.10 margin
   (P3), 0.90/0.10 abstention (P4). These are my numbers, chosen with
   probe knowledge but no formal power analysis. Challenge any that is
   unachievable-by-construction or trivially passable. P3's +0.10 in
   particular: is it inside noise at the n we can afford?
3. **R-C — decision-time `t_dec`.** One-shot decision at
   first-detectable + 2 s. Is one-shot the right protocol, or does it
   smuggle in an advantage/handicap vs robust-v9, which re-decides
   continuously? This may be the biggest unfairness risk in the design.
4. **R-D — holdout leakage.** §5 requires an ingredient-level audit
   (contamination-arm F2). Is fragment-level co-occurrence the right
   check for *continuous* severities, where "the same ingredient" is a
   neighborhood rather than a token? Propose the concrete audit statistic.
5. **R-E — what is missing entirely?** The failure mode I most expect is
   an unlisted control or an unpinned degree of freedom. Name it.

## Not in scope

R4 (1236 re-confirm) remains the human's call. The nav-latch ablation is
declared but not scheduled. GRU/asymmetric-critic ladder, fourconnect
closeout, and PVSG backfill stay parked.

**No data will be generated until this critique lands and is adjudicated.**
