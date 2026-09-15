# Pre-registration: eval run 2 on held-out slice v1 (the last under key #7), decision rule pinned BEFORE DEV2 exists

Written 2026-09-13 19:23Z by fable, while the DEV2 pipeline run (data/hotpot_dev2_v1.jsonl, 100
questions disjoint from the slice, seed 20260914) is at doc 16 of 100 and no DEV2 number has been
read. Kimi s33 registered DEV2 as the discriminant for the run-2 claim.

## Decision rule (mechanical, from the frozen DEV2 summary; no other input)
Let d(w) = mean F1 of wiring w minus single-pass on DEV2.
- Claim = **iterative + notes** if d(iterative_notes) > d(iterative_fallback) AND d(iterative_notes)
  >= +0.03 AND iterative_notes has at least as many wins as losses on DEV2.
- Otherwise claim = **iterative + fallback** (the s15 definition), and the run-1 lead of the notes
  variants is reported as a ranking flip, not a result.
- No other wiring can become the claim from DEV2 (superset + notes, select and the rest stay
  diagnostic whatever DEV2 says), so the choice is a two-way rule, not a search.

## Run 2 (same pins as run 1 except the claimed wiring)
- slice data/hotpot_heldout_v1.jsonl, sha256 3fd1aa51d9bd6876..., docs 0-99, unchanged.
- tagger models/tagger_v4clean_0.5b, reader Qwen2.5-3B-Instruct, script pipeline_exec.py frozen at
  s29 (no change), keyword top-6 within 3000 tokens for every wiring, greedy decoding.
- The script is deterministic, so run 2 re-produces run 1's per-doc numbers; the point of run 2 is
  the pre-registered claim on a re-executed run, with the baseline reproduced exactly as a check.
- band: claimed >= single-pass + 0.05 (GOAL, unchanged).

## Predictions, banded, one per branch (written now)
- Branch notes: claimed delta +0.03 to +0.09; P(>= +0.05) about 0.55 (run-1 diagnostic +0.064 with a
  CI including zero; DEV2 agreement raises it, the ranking flip on LongBench eval lowers it).
- Branch fallback: claimed delta +0.01 to +0.06; P(>= +0.05) about 0.25 (run 1 gave +0.032).
- Falsifier for either branch: delta <= +0.01.
- Bootstrap CI reported with the result, pasted from the frozen file only (s32 rule).
