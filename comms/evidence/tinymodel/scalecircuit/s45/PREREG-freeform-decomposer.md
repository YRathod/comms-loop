# Pre-registration: fix 1, free-form decomposer replacing the relation grammar (needs key #10; nothing built)

Written 2026-09-14 ~02:40Z by fable, before key #10 exists. Motivation: on slice v3, 4 of 6 chain
failures with a correct single-pass answer started from a wrong or meaningless first hop forced by
the 20-relation grammar (s44 analysis). The grammar goes; the model writes the hops.

## Mechanism
- Decomposer = Qwen2.5-1.5B-Instruct + LoRA (0.5B as a fallback if 1.5B does not fit the 8 GB GPU),
  input = question, output = either `NA` (no decomposition: comparison / single-hop / unsure) or two
  lines: `H1: <sub-question keeping the anchor and its qualifiers>` and `H2: <sub-question with #1
  where hop 1's answer goes>` (three lines for depth 3). No relation tokens, no templates, no LSTM.
- Abstain gate (fix 2): `NA` -> single-pass. A decomposition is also discarded if H1 does not
  contain a capitalised span from the question (mechanical check), -> single-pass.
- Wirings evaluated as today (pipeline_exec.py with a new `--decomposer` path replacing
  hops_from_tag + templates; everything else, budgets included, unchanged).

## Training data, provenance-first
- Source: HotpotQA distractor TRAIN split only (already in the HF cache from the key #7 download;
  no new network use beyond re-reading that cache). Never a row from validation.
- Hand labels: 300 train-split questions decomposed by fable from the question text and the
  supporting-fact titles of that same train row (bridge entity = the supporting title that is not the
  answer paragraph). Classes may be studied on any slice; strings only from the train split.
- Teacher labels: Qwen2.5-3B-Instruct (local, frozen) writes H1/H2 for 3000 further train-split
  questions, filtered mechanically (H1 must contain a capitalised span of the question; H2 must
  contain #1). THIS IS AN EXCEPTION to the standing rule "model outputs never enter training data":
  it is a frozen teacher on the train split, never the student's own outputs, never held-out rows.
  It is only allowed if key #10 says so explicitly.
- Provenance check before training (scripts/tagger_data_check.py adapted for the free-form format:
  leg 3 anchors, leg 4 content 3-gram share vs every held-out slice v1/v2/v3 and LongBench 0-39):
  CLEAN required, stamp written, trainer refuses without it.

## Pre-gate (<= 15 min) and full run
- pre-gate: 1 epoch on the 300 hand labels only; band: on 40 DEV2 questions (never a held-out slice)
  the decomposer produces a parseable H1/H2 or NA on >= 36/40 and keeps the anchor span in H1 on
  >= 30/40. Fail -> stop, report.
- full run: 2 epochs on 300 x 5 + 3000 teacher rows; sanity bands as before; heartbeat; DEV2 wiring
  run (n=100) afterwards.

## Eval (ONE run, fresh slice v4)
- slice v4: n = 400, seed 20260917, from the remaining pool (excluding LongBench 0-199, v1, DEV2, v2,
  v3), same construction, sha256 frozen before any model reads it.
- claim decided by a rule pinned now: between `chain-freeform` (answer hop by hop with the free-form
  hops, abstain -> single-pass) and `superset-freeform` (baseline chunks first, hop chunks after),
  pick the one with the larger DEV2 delta; if both DEV2 deltas are <= +0.02, no eval run is made and
  the fix is reported as not transferring.
- band: mean delta >= +0.05 AND 95 percent interval excludes zero. Prediction: chain-freeform
  +0.00 to +0.06 (it has to recover from -0.20; the abstain gate caps the downside), superset-freeform
  +0.03 to +0.08; P(PASS for the chosen arm) about 0.4. Falsifier: chosen arm <= +0.02.
- everything else diagnostic; numbers only via result_block.py from frozen files.
