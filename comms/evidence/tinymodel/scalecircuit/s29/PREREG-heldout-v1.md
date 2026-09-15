# Pre-registration: fresh HotpotQA held-out slice v1 and eval run 1 on it (key #7)

Written 2026-09-13 ~18:55Z by fable under KEYS.md key #7 (from_human/20260913-HHMM-key-heldout-slice.md,
expires 2026-09-15T00:00Z), human autopilot window 18:50Z-02:50Z, NO CHEATING rules of
GOAL-2026-09-13.md in force. Written BEFORE the dataset is read by any model and before the slice exists.

## Slice construction (deterministic, frozen with a sha256 before any model reads it)
- source: HF datasets `hotpot_qa`, config `distractor`, split `validation` (7405 rows), downloaded
  to tiny-model/data/hotpot_distractor_validation.jsonl (raw, untouched).
- exclusion: any row whose normalised question text (lowercase, whitespace-collapsed) equals a
  LongBench hotpotqa question (docs 0-199) is excluded; so is any row whose question appears in any
  hand-labelled batch (40-199, same set).
- sampling: random.Random(20260913).sample over the remaining rows, n = 100, in that order.
- context, to match the LongBench setting the earlier numbers were measured in: the row's own 10
  paragraphs plus the 10 paragraphs of 8 other rows drawn with the same rng (never another slice
  member), each paragraph written as "Title\n<sentences joined>", all 90 shuffled with the same rng
  and joined by blank lines. Budgets and retrieval identical to the LongBench runs (keyword top-6,
  3000 tokens for every wiring).
- fields: input (question), context, answers ([answer]), _id (HotpotQA id), level, type.
- output: data/hotpot_heldout_v1.jsonl; sha256 recorded in comms evidence s29 before any model call.
- the slice is never labelled, never trained on, never used as generator material or as DEV.

## Eval run 1 (of at most 2 under key #7)
- pipeline: scripts/pipeline_exec.py frozen at s15 (+ a --data path argument, no behavioural change),
  reader Qwen2.5-3B-Instruct, tagger models/tagger_v4clean_0.5b (clean), LSTM decomp_filter_lstm.pt.
- claimed wiring: iterative + shape fallback (s15 definition), the only arm never negative on both
  earlier slices. Everything else the script computes is diagnostic and will not be claimed.
- baseline: single-pass, same reader, retrieval, budget, docs.
- band: claimed >= single-pass + 0.05 (GOAL, unchanged). n = 100, so one doc = 0.01 F1.
- prediction, banded: claimed wiring delta +0.01 to +0.06; P(delta >= +0.05) about 0.30.
  Distribution note, written now: HotpotQA distractor questions are on average shorter and more
  templated than LongBench's selection, and 20 percent are yes/no comparison questions that the
  tagger maps to NA (single-pass fallback), so the delta may be diluted toward zero.
- falsifier: delta <= +0.01 -> the iterative mechanism does not carry to this slice; report as such.
- bootstrap 95 percent CI over docs reported with the result; the band verdict is on the mean.
