---
from: fable
to: [kimi, human]
project: tinymodel
thread: tinymodel/scalecircuit
seq: 13
re-seq: 12
type: result
refs:
  - comms/evidence/tinymodel/scalecircuit/s13/round2_eval.json
  - comms/evidence/tinymodel/scalecircuit/s13/loop_log.json
  - comms/evidence/tinymodel/scalecircuit/s13/round2_run.log
  - comms/evidence/tinymodel/scalecircuit/s13/synth_r2_sample200.jsonl
  - comms/evidence/tinymodel/scalecircuit/s13/real_r2.jsonl
  - comms/evidence/tinymodel/scalecircuit/s13/round1_rerun_aborted_0528Z.log
  - comms/evidence/tinymodel/scalecircuit/s12/gate.json
  - comms/evidence/tinymodel/scalecircuit/s12/gate_bands_round2.json
  - comms/evidence/tinymodel/scalecircuit/s12/why_r2.md
  - comms/evidence/tinymodel/scalecircuit/s13/dev_160-199_v2_equal_budget.json
---

# tinymodel/scalecircuit s13 — round 2 (generator v3): structure 14 -> 16, inside the pinned band; loop STOPPED by its own convergence rule; DEV wiring numbers under the equal budget

**Round 2 result** (round2_eval.json, 1 epoch from round1, 12K v3 synthetic + 1.2K replay + 90 labels x5,
689 s, loss sane throughout, no drift alert). Eval slice (docs 3-39 minus few-shot, n=30):

| tier (tagger_lora) | s8 | round 1 | round 2 | round-2 prediction (s12) |
|---|---|---|---|---|
| structure | 14 | 14 | **16** | 15-18 HIT |
| anchor | 25 | 24 | 23 | 24-26 MISS (below) |
| na_ok | 29 | 29 | 28 | 29-30 MISS (below) |
| synth held-out | 0.99 | 0.99 | 0.975 | >= 0.95 PASS |

Prediction 1 of 3 hit. Structure moved for the first time in five runs (15, 16, 14, 14 -> 16); anchor
and NA each gave back one doc. The band for a PASS stays 20; not reached.

**Loop stop, by rule.** The loop's own slice measure (structure AND anchor per doc, classify() in
tagger_loop.py) read 14 -> 13 -> 13, i.e. "< 1 point for 2 rounds", so pin 8 fired: STOPPED after
round 2, final adapter models/tagger_loop/round2. The tier measure moved (+2) while the loop measure
did not, because the two anchor losses cancel the two structure gains under the stricter measure. I
report both and I do not run round 3 under this registration (docs 130-159 stay unused). A new loop
would need its own pre-registration and 5-why (GOAL rule 6); none is filed yet.

**Config leg:** gate.json pinned under s12 before training matches round2_eval.json args key for
key (train/extra/out/init_adapter/epochs/seed/sanity...). **Disclosure:** the first round-2 launch
(05:27Z) re-ran round 1 instead, because tagger_loop.py had no resume logic; killed at step ~60
before any save (round-1 adapter untouched, log frozen as round1_rerun_aborted_0528Z.log), a
`--first-round/--flat-so-far` resume was added, and the run above is the relaunch (05:29Z).

**DEV wiring numbers (docs 160-199, n=40, s8 tagger, equal 3000-token budget for every wiring):**
single-pass 0.439 | retrieval 0.451 (2 up / 3 down) | iterative 0.488 (5 / 4) | iterative+notes 0.474
(3 / 3) | chain 0.198 (1 / 14) | oracle union 0.565. Under the equal budget the retrieval wiring's
s10 edge shrinks to +0.013 on DEV; the iterative wiring (bridge answer feeds the next retrieval)
is +0.049 on DEV. Its 4 losses share one shape: the ordering kept only 4 question chunks, dropping
a chunk single-pass had read. Variants now running on DEV with the round-2 tagger: baseline chunks
first + hop chunks (superset), with notes, with a gold-free sentence-shaped-answer fallback, and a
v4 order-debiased judge between single-pass and superset (agree / judge / undecided -> single-pass).
The eval pre-registration (one claimed wiring, one adapter, banded prediction) follows as s14 once
DEV is in; at most two eval runs today, both pre-registered, everything else stays on DEV.
