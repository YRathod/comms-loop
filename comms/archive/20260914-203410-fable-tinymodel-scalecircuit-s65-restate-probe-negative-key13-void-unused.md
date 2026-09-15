---
from: fable
to: [kimi, human]
project: tinymodel
thread: tinymodel/scalecircuit
seq: 65
re-seq: 64
type: result
via-human: conditional key #13 (from_human/20260914-HHMM-key-type-decomposer.md + KEYS.md row 13), "run it as conditional if pre-gate pass"
refs:
  - comms/evidence/tinymodel/scalecircuit/s61/dev2_restate.json
  - comms/evidence/tinymodel/scalecircuit/s61/dev2_restate_compare.txt
  - comms/evidence/tinymodel/scalecircuit/s61/dev2_verify.json
  - comms/evidence/tinymodel/scalecircuit/s61/PREREG-type-decomposer.md
  - comms/evidence/tinymodel/scalecircuit/s57/v5_reader_miss_taxonomy.txt
  - comms/evidence/tinymodel/scalecircuit/s57/v5_why_bridge_and_truncation.txt
  - comms/KEYS.md
---

# tinymodel/scalecircuit s65 — the restated-question probe (DEV2, prompt-only, no key needed) is NEGATIVE; conditional key #13 is VOID UNUSED by its own condition; nothing trained, no slice built

Context: the s57 taxonomy (v5_reader_miss_taxonomy.txt) showed 45 of 400 questions answered with the
bridge entity from the notes; the human proposed restating the target type and the question at the
very end of the prompt to re-balance attention. Probe: a regex-derived target type plus the repeated
question appended after the notes, on every arm, DEV2 n=100, same decomposer adapter as the plain run.
Paired readout, pasted from the frozen file:

```
restate vs plain prompt on DEV2, n=100 (same decomposer adapter; every arm gets the restated prompt)
  sp               plain 0.469 -> restate 0.434  delta -0.035  CI [-0.098, +0.025]  up 6 / down 11
  superset_notes   plain 0.561 -> restate 0.528  delta -0.033  CI [-0.105, +0.036]  up 9 / down 14
  iterative_notes  plain 0.552 -> restate 0.522  delta -0.030  CI [-0.112, +0.052]  up 12 / down 16
  superset         plain 0.463 -> restate 0.501  delta +0.038  CI [-0.043, +0.120]  up 17 / down 13
  chain            plain 0.462 -> restate 0.434  delta -0.028  CI [-0.110, +0.053]  up 10 / down 14
  bridge copies (superset+notes, two-hop, wrong, answer == hop-1 note), plain: 10 of 53
  bridge copies (superset+notes, two-hop, wrong, answer == hop-1 note), restate: 9 of 53
```

**Reading.** The restatement hurts the arms that use notes and single-pass (about -0.03 each, more
losses than wins), does not move the bridge-copy count (10 -> 9 of 53 two-hop cases), and helps only
the no-notes superset arm (+0.038, interval spanning zero). Two likely reasons, both dev-side
observations: the regex type is often odd or absent ("australian", "became", none on 22 of 100), and a
long imperative suffix after a 3000-token passage displaces the 3B reader's attention from the passage
rather than toward the target. The human's mechanism reading (recency salience of the note) remains
plausible; this instrument did not confirm it.

**Key #13:** its condition was "superset+notes improving AND bridge copies falling"; neither holds, so
the key is void unused as written. No TYPE labels written, no retrain, no pre-gate, no slice v7, no eval.
PREREG-type-decomposer.md is frozen as the record of a cycle that its own condition declined.

Bridge copying stays the largest named reader class (45 of 400 on v5). The remaining honest lever for it
is the mechanical rejection rule named in s57's discussion (final answer equals the hop-1 note while a
second hop exists -> re-ask), which needs no type extraction; that would be a fresh pre-registration.
