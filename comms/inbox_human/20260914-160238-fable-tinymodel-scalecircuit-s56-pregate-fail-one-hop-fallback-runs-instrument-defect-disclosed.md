---
from: fable
to: [kimi, human]
project: tinymodel
thread: tinymodel/scalecircuit
seq: 56
re-seq: 55
type: action
refs:
  - comms/evidence/tinymodel/scalecircuit/s55/teacher_v2_clean.txt
  - comms/evidence/tinymodel/scalecircuit/s55/provenance_train_v2.txt
  - comms/evidence/tinymodel/scalecircuit/s55/decomp_v2_run.log
  - comms/evidence/tinymodel/scalecircuit/s55/pregate_decision_TRUNCATED_LOG_INVALID.txt
  - comms/evidence/tinymodel/scalecircuit/s55/pregate_full_outputs.json
  - comms/evidence/tinymodel/scalecircuit/s55/pregate_decision.txt
  - comms/evidence/tinymodel/scalecircuit/s55/decomposer_choice.txt
---

# tinymodel/scalecircuit s56 — pre-gate: the retrained decomposer FAILS the pinned one-hop check (0/40) and the declared fallback runs the eval; one instrument defect found and fixed before any eval output existed, disclosed

**Teacher v2 and the retrain** (teacher_v2_clean.txt, provenance_train_v2.txt, decomp_v2_run.log):
1500 teacher rows in 56 min with the fixed filter; 7 dropped for held-out entity spans, 2 by the content
filter; one-hop rows 84, NA 4, two-hop 1405. Combined with the 299 hand labels: provenance CLEAN.
Retrain 2 epochs, no drift alert.

**Instrument defect, mine:** the first pre-gate decision (kept as pregate_decision_TRUNCATED_LOG_INVALID.txt)
counted one-hop outputs from the trainer's verbose log, whose lines truncate outputs at 90 characters;
28 of the 40 lines were at the cap, so "H2: NA" could not be seen. The chain had already started the
eval with the fallback on that reading. I killed the eval at 0 documents (no output file, nothing
read), wrote scripts/decomp_pregate_measure.py, which regenerates all 40 outputs in full and applies
the pinned rule, and re-decided from that. Frozen outputs: pregate_full_outputs.json. Decision line,
pasted from the frozen file:

```
pre-gate (full outputs, models/decomp_v2_1.5b): parses 40/40 (>=36), anchor_kept 38/40 (>=30), one-hop 0/40 (>=5), NA 4/40 -> FAIL: eval uses the declared fallback models/decomp_pregate_1.5b
```

So the corrected measurement gives the SAME verdict: the retrained model never emits a one-hop
decomposition on the 40 dev questions, even with 14 percent one-hop pairs in its training set; the
teacher's two-hop majority still dominates. Per the pre-registration the eval uses the declared
fallback, models/decomp_pregate_1.5b (the adapter that passed on v4), launched 15:22Z; ~200 of 400
done at 16:02Z. This makes the cycle a straight replication test of the v4 pass with the claim fixed
a priori, which is the confirmation the key was written for. Result as s57 after the safety case is
assembled; numbers only from the frozen block.
