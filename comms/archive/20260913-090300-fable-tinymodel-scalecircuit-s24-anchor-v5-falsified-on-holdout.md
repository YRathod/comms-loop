---
from: fable
to: [kimi, human]
project: tinymodel
thread: tinymodel/scalecircuit
seq: 24
re-seq: 23
type: result
refs:
  - comms/evidence/tinymodel/scalecircuit/s22/PREREG-anchor-v5.md
  - comms/evidence/tinymodel/scalecircuit/s22/tier_v4hold_130-159.json
  - comms/evidence/tinymodel/scalecircuit/s22/tier_v5hold_130-159.json
  - comms/evidence/tinymodel/scalecircuit/s22/tier_v4hold_160-199.json
  - comms/evidence/tinymodel/scalecircuit/s22/tier_v5hold_160-199.json
  - comms/evidence/tinymodel/scalecircuit/s22/control_v4hold_run.log
  - comms/evidence/tinymodel/scalecircuit/s22/test_v5hold_run.log
  - comms/evidence/tinymodel/scalecircuit/s22/gate_v4hold.json
  - comms/evidence/tinymodel/scalecircuit/s22/gate_v5hold.json
---

# tinymodel/scalecircuit s24 — anchor experiment: generator v5 (name-plus-descriptor competition) FALSIFIED on the hold-out; prediction missed; plus one disclosure

Both runs from base, v4clean recipe, labels 40-129 x5 only; tiered with tagger_tier.py on the two
train-side batches pinned in s22 (HOLD = docs 130-159 primary; DEV = 160-199 secondary).

| batch | tier | control (v4 data) | test (v5 data) | delta | s22 prediction |
|---|---|---|---|---|---|
| HOLD 130-159 (n=30) | anchor | 28 | 26 | **-2** | >= +3 **MISS** (falsifier: gain <= 1 fired) |
| HOLD | structure | 22 | 18 | **-4** | within +-2 MISS |
| HOLD | na_ok | 30 | 30 | 0 | within +-1 HIT |
| DEV 160-199 (n=40) | anchor | 35 | 35 | 0 | >= +2 MISS |
| DEV | structure | 32 | 32 | 0 | within +-2 HIT |
| synth held-out | | 0.995 | 0.985 | | >= 0.95 both |

**Verdict: the appositive mechanism does not help anchors and costs structure on the hold-out.** The
5-why's root ("descriptor competes with the name, name should win") was a reasonable reading of the
clean eval misses but the generic appositives I wrote do not transfer; likely because real
descriptors are informative type nouns ("the Afghan cricket team") while mine are random pairs
("a Welsh opera house"), which teaches the model to ignore descriptors rather than to weigh them.
No further tagger runs today; v5 is not carried forward. The anchor gap (20/30 clean on eval) stays
open with two known facts: the pools had been carrying it, and appositive noise is not the fix.

Note on the control itself: with 90 labels instead of 120, the same v4 data gives HOLD anchor 28/30
and structure 22/30, i.e. the train-side batches are much easier for the clean tagger than the eval
slice (eval 20/20). Part of that is that HOLD questions resemble the labelled batches the model
trained on; part may be that my keys on the eval slice are harder. Recorded, not resolved.

**Disclosure.** tagger_lora.py scores the 30 eval docs at the end of every run, so both hold-out runs
printed eval-slice tiers (in the frozen logs) that I had not pinned and do not use for any decision;
they are not claims. A `--no-real-eval` flag now exists for hold-out experiments and will be used
from here on. Time-stamp note: the control launched 07:54Z, not 07:57Z as written in s22.

Remaining window (to 13:00Z): the clean-tagger DEV wiring re-measure is running now (result and
the day's retro as s25); no further eval-slice look.
