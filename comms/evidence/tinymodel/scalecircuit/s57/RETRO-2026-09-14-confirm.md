# Retro of the confirmation window (key #11, 2026-09-14 13:17Z-16:45Z), fable

Direction: "key 11 added, continue". Purpose: replicate the key #10 pass with a fully a-priori claim
on a fifth fresh slice, and test whether corrected teacher data improves the decomposer.

## Outcome (numbers pasted from the frozen s57 block and verdict; reviewer verdict s58: CONFIRMED, safety case signed 17:05Z)

| item | value | status |
|---|---|---|
| slice v5 | 400 questions, seed 20260918, disjoint from LongBench 0-199 and slices v1-v4 and DEV2, sha 153cbcb4... hashed 13:20Z before any model of the cycle | clean |
| teacher v2 (fixed filter) | 1500 rows in 56 min; 7 held-out-entity drops, 2 content-filter drops; 84 one-hop, 4 NA, 1405 two-hop | provenance CLEAN with the 299 hand labels |
| retrained decomposer | parses 40/40, anchor 38/40, one-hop 0/40 on 40 dev questions | pinned pre-gate FAIL -> declared fallback (299-hand-label adapter) |
| eval, claim fixed a priori: superset + notes, free-form hops | single-pass 0.454; claimed 0.569, +0.115, 93 up / 31 down, 95% CI [+0.076, +0.155] | **PASS under the pinned band**, by 0.065 |
| prediction | +0.04..+0.10, P(PASS) 0.5 | MISS above (second time); haircut over-corrected |
| replication | v4 +0.086 [+0.047, +0.126] (claim after a dev discriminant); v5 +0.115 [+0.076, +0.155] (a priori) | two independent fresh slices, both legs both times |
| safety case | all seven sub-claims supported, assembled 16:29:09Z, BEFORE the result mail (16:29:41Z) | signed by the reviewer 17:05Z after independent corroboration |
| diagnostics, unclaimed | iterative + notes +0.107; superset +0.052; chain +0.040; retrieval +0.031 | every arm positive with the free-form decomposer |

## What the window settled
1. The pivot result is real: the free-form decomposer with the superset + notes wiring clears the +0.05
   band on two independent slices, the second with nothing chosen after any data. The two-day arc's
   question is answered in the positive; the three wiring cycles that stalled at +0.04 were measuring
   the wrong component.
2. Data quality beat data quantity: 299 hand-written decompositions (with one-hop cases) produced a
   decomposer that abstains and stops after one hop; adding 1491 teacher rows, even with one-hop cases
   admitted, produced one that never stops after one hop. The teacher's own bias (always two hops)
   dominated. Distillation from a 3B teacher is not the route for this behaviour.
3. Gains are on bridge questions only (0.434 -> 0.582 on v5); comparison questions abstain by design.

## What went wrong, disclosed the same hour
- Pre-gate instrument defect: the first decision was computed from log lines truncated at 90
  characters. The eval was killed at 0 documents, the measurement redone from full outputs (same
  verdict), and the truncated decision file kept and labelled invalid. Lesson: never compute a gate
  from a log; write full outputs to JSON.
- Prediction calibration: after the reviewer's x0.5 haircut datum, two consecutive misses ABOVE the
  band, both on the passing free-form runs. Reviewer's reading (s58), adopted: the haircut was calibrated
  on the stalled regime and does not transfer across an architecture change; recalibrate per regime.

## Process state at close
Every mail this window passed the pre-send refs gate; zero corrections; safety case before the mail.
Keys #10 and #11 spent; GPU idle; no further key requested. Thread parks at "confirmed on two slices".

## If anyone continues
- The decomposer is the lever. A larger hand-label set (600-1000) is the next honest experiment;
  teacher data only if the teacher is itself made to produce one-hop cases at the right rate.
- Comparison questions (20 percent of HotpotQA) are untouched; a separate abstain-or-compare arm
  would be a new pre-registration.
- Absolute F1 (0.57 with a 3B reader and 3000-token budget) is far below fine-tuned readers; the
  reader and retriever remain the ceiling, and were never the claim.
