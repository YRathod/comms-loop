# Pre-registration: confirmation cycle for the free-form decomposer (needs key #11; nothing built)

Written 2026-09-14 ~13:00Z by fable, before key #11 exists. Purpose: confirm the key #10 pass with a
fully a-priori claim on a fifth fresh slice, and test whether corrected teacher data helps.

## Claim, fixed now (no dev discriminant in this cycle)
superset + notes with free-form hops (baseline chunks first, hop chunks after, the hop answers shown to
the reader as notes), the arm that passed on slice v4 (s50/s52).

## Decomposer
- Retrain: Qwen2.5-1.5B-Instruct + LoRA, 2 epochs, on 299 hand labels x5 + teacher rows regenerated with
  the FIXED filter (H2 may be NA; scripts/decomp_teacher.py as of s48), capped at 1500 kept, train split
  only, content-filtered, provenance CLEAN (SUSPECT on the hand file already adjudicated, s46/s49).
- Pre-gate on 40 unlabelled DEV2 questions: parseable >= 36/40, anchor kept >= 30/40, AND at least 5 of
  40 outputs are one-hop (H2: NA) so the over-decomposition failure is visibly gone.
- Fallback, declared now: if the retrained adapter fails the pre-gate, the eval uses the existing key-#10
  pre-gate adapter (models/decomp_pregate_1.5b, hand labels only), unchanged. Either way ONE eval run.

## Eval
- slice v5: n = 400, seed 20260918, from the pool after excluding LongBench 0-199, v1, DEV2, v2, v3, v4;
  same construction; sha256 frozen before any model of this cycle reads it.
- pipeline unchanged (s29 script + --decomposer path, equal 3000-token budget, greedy).
- band unchanged: PASS = mean delta >= +0.05 AND the 95 percent bootstrap interval of the per-doc delta
  (20000 resamples, seed 0) excludes zero.
- prediction: delta +0.04 to +0.10; P(PASS) 0.5 (raw read 0.9 from the v4 interval, haircut applied
  once; kimi s52 notes the haircut has variance). Falsifier: delta <= +0.02.
- everything else diagnostic; numbers via result_block.py; safety case assembled and reviewer-signable
  BEFORE the result mail is written; pre-send refs gate on every mail.
