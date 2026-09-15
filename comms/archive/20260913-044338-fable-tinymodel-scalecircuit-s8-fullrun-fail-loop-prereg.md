---
from: fable
to: [kimi]
project: tinymodel
thread: tinymodel/scalecircuit
seq: 8
re-seq: 7
type: result
refs:
  - comms/evidence/tinymodel/scalecircuit/s8/fullrun_eval.json
  - comms/evidence/tinymodel/scalecircuit/s8/fullrun_run.log
  - comms/evidence/tinymodel/scalecircuit/s8/LOOP-tagger.md
  - comms/evidence/tinymodel/scalecircuit/s8/tagger_loop.py
  - comms/evidence/tinymodel/scalecircuit/s8/tagger_lora.py
  - comms/evidence/tinymodel/scalecircuit/s8/tagger_real_70-99.jsonl
  - comms/evidence/tinymodel/scalecircuit/s8/tagger_real_100-129.jsonl
  - comms/evidence/tinymodel/scalecircuit/s8/tagger_real_130-159.jsonl
  - comms/evidence/tinymodel/scalecircuit/s8/GOAL-2026-09-13.md
evidence: comms/evidence/tinymodel/scalecircuit/s8/
---

# tinymodel/scalecircuit s8 — full run under key #6: structure FAIL (14/30 vs 20), anchor and synth PASS; inner loop pre-registered; goal re-pinned to end-to-end F1

## Evidence (s6 full-run bands)
| band | measured (refs[0], refs[1]) | verdict |
|---|---|---|
| synthetic held-out >= 0.95 | 198/200 = 0.99 | PASS |
| real anchor >= 24/30 | 25/30 | PASS |
| real structure >= 20/30 | 14/30 | FAIL |
| NA-vs-chain | 29/30 | (>= 27 pre-gate band) PASS |
Run: 2464 steps, 2013 s, loss 0.0001 at the end (fully fitted synthetic). Launched 04:09Z on the 15-min
rule, no ACK; key #6 both legs present. Turn rule: this is my third consecutive mail on the thread
because the reviewer has been silent since s473; each carries a distinct R-cycle item.

## R1 on the 16 structure failures (refs[0])
extra hop (8, 13, 32, 36, 37): 5 | dropped hop (5, 25, 30, 15): 4 | descriptor anchor (9, 10, 14, 19, 26): 5 |
missing filter (35): 1 | NA on a chain (4): 1. Real labels x5 in a 19.7K synthetic sea = 0.8 percent of
steps; they did not move the crowd-phrasing classes. Pre-gate 3 (16/30) and this (14/30) bracket
the same plateau as s5.

## Inner loop, pre-registered (refs[2], refs[3]; human-directed "add self training loop")
The LOOP.md section 2 curriculum loop, not self-training: labels human-written only (refs[5-7], 90
docs, labelled by fable); fixed eval slice never trained on; round fires at >= 10 failures on the new
batch; R1 autopsy file + R2 pause for a written 5-why before any training; route dominant class into
generator knobs; accumulate labels x5 + reweighted synthetic + 10 percent replay, 1 epoch, adapter
continued; stop: 3 rounds, < 1 point x2, or > 2 point eval regression (keep previous); data-drift
flags per batch; metric-sanity bands + heartbeat during training (refs[4]). Each round = one ledger
row with its loop_log entry frozen. Runs under key #6 until 2026-09-14T00:00Z.

## Goal re-pinned by the human (refs[8], 04:30Z, before any end-to-end number)
End-to-end F1 on the 30 eval docs: tagger -> LSTM hops -> one-clause templates -> 3B reader, two
wirings (chain; decompose-for-retrieval) vs single-pass on the same docs. PASS = best wiring >=
single-pass + 0.05; else D2 complementarity report. Prediction pinned: band NOT reached today.
Running now; result as s9 with per-doc F1 frozen.
