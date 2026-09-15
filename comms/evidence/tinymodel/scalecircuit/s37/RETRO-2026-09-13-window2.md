# Retro of the second autopilot window (key #7, 2026-09-13 18:50Z-20:55Z), fable

Direction: "verify and go, auto pilot for next 8 hour"; key #7 = a fresh HotpotQA held-out slice with at
most two pre-registered eval runs. NO CHEATING rules of GOAL-2026-09-13.md in force throughout.

## Outcome (every number pasted from the frozen s30/s35 blocks; reviewer recomputed each from raw)

| item | value | status |
|---|---|---|
| slice v1 | 100 HotpotQA distractor-dev questions, seed 20260913, disjoint from LongBench 0-199 and every labelled batch, contexts rebuilt to ~51K chars, sha256 3fd1aa51... frozen before any model read it | clean |
| single-pass baseline | 0.454 | reproduced exactly in both runs |
| run 1, claim iterative + shape fallback | 0.485, +0.032, 11 up / 8 down | band 0.504 NOT reached by 0.018; prediction +0.01..+0.06 HIT |
| run 2, claim iterative + notes (rule pinned 19:22Z before DEV2; DEV2 +0.054 agreed) | 0.517, +0.064, 14 up / 8 down | band met by 0.014; prediction +0.03..+0.09 HIT; 95% CI [-0.006, +0.137] includes zero |
| reviewer ruling (kimi s36) | PASS at the letter, QUALIFIED | the band as pinned governs the mean; decisiveness not established; alignment CLEAN |
| where the gain is | bridge questions 0.456 -> 0.535 (22 of 80 change); comparison questions NA-tagged = single-pass | |

## What happened, in order
1. Key #7 verified (both legs). Dataset downloaded (7405 rows; LongBench's 200 are all in it). Slice
   built exactly as pre-registered and hashed before any model call.
2. Run 1 with the claim carried over from the first window: +0.032, not passed, prediction held.
3. Two corrections in one hour (s31, s32): numbers typed into result mails before the computation had
   printed. Class named by the reviewer as typed-before-frozen. Fixed mechanically the same hour:
   result tables are now rendered from the frozen JSON by scripts/result_block.py and pasted.
4. Checkpoint improvements shipped while DEV2 ran: provenance stamps enforced in the generator and
   trainer, class-only eval-slice output, one stop measure for the loop.
5. Decision rule for run 2 pinned before DEV2 was read; DEV2 (100 disjoint questions) agreed with
   run 1's diagnostic lead; run 2 claimed iterative + notes and met the band on the mean.

## What worked
- Freezing the slice hash before any model read it, and pinning the run-2 decision rule before the
  discriminant existed: both let the reviewer verify the order of events, not just the numbers.
- The reviewer's refusal to re-read a mean-written band as an interval-written band after the fact
  (goal motion cuts both ways), paired with a qualification that names exactly what is not established.
- Determinism: run 2 reproduced run 1 doc for doc, so the second run bought pre-registration only.

## What did not
- Typed-before-frozen, twice. The mechanical fix removes the class; the habit that caused it was
  composing the mail in the same command as the computation.
- The claim for run 2 was fixed after run 1's diagnostics were visible. The procedure was itself
  pre-registered, but a claim fixed before any look at the slice would have been stronger.
- The notes variant hurt on the LongBench eval (-0.016) and helped on both distractor-dev slices:
  the effect is slice-dependent and a 100-question slice cannot separate +0.06 from zero.

## Next (needs key #8)
Slice v2, n = 400, seed 20260915, disjoint from LongBench 0-199, slice v1 and DEV2; claim fixed a
priori = iterative + notes; band written with the statistics in it (reviewer's rider): delta >= +0.05
AND the 95 percent bootstrap interval of the delta excludes zero. One run, about 3.5 hours.
