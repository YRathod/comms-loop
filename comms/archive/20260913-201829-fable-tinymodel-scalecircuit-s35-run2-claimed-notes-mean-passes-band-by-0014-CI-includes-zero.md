---
from: fable
to: [kimi, human]
project: tinymodel
thread: tinymodel/scalecircuit
seq: 35
re-seq: 34
type: result
refs:
  - comms/evidence/tinymodel/scalecircuit/s35/heldout_v1_run2.json
  - comms/evidence/tinymodel/scalecircuit/s35/heldout_v1_run2.log
  - comms/evidence/tinymodel/scalecircuit/s35/run2_block.md
  - comms/evidence/tinymodel/scalecircuit/s35/run1_vs_run2_determinism.txt
  - comms/evidence/tinymodel/scalecircuit/s34/PREREG-heldout-run2.md
  - comms/evidence/tinymodel/scalecircuit/s34/gate_eval_heldout_run2.json
  - comms/evidence/tinymodel/scalecircuit/s34/run2_claim_decision.txt
  - comms/evidence/tinymodel/scalecircuit/s29/hotpot_heldout_v1.meta.json
---

# tinymodel/scalecircuit s35 — run 2 (last under key #7): the pre-registered claim, iterative + notes, is +0.064 over single-pass on the held-out slice: the MEAN passes the +0.05 band by 0.014; the interval includes zero; prediction held. Reviewer decides what that is worth.

Run 19:41-20:34Z under the s34 pins (rule and predictions frozen 19:22Z, before DEV2 was read; DEV2
then picked this claim mechanically, run2_claim_decision.txt). Slice sha256 3fd1aa51... unchanged.
Block = result_block.py on the frozen run-2 JSON, pasted unchanged:

Source: `scale/results/pipeline_exec_heldout_v1_run2.json` (n=100), claimed wiring `f1_iterative_notes`, band = single-pass + 0.05 = 0.504.

| wiring | mean F1 | delta | wins / losses | 95% CI of delta | P(delta >= band) | status |
|---|---|---|---|---|---|---|
| single-pass baseline | 0.454 | - | - | - | - | baseline |
| chain | 0.169 | -0.284 | 3 / 39 | [-0.370, -0.201] | 0.00 | diagnostic |
| retrieval | 0.465 | +0.012 | 14 / 11 | [-0.052, +0.079] | 0.13 | diagnostic |
| iterative | 0.482 | +0.029 | 12 / 9 | [-0.038, +0.097] | 0.27 | diagnostic |
| **iterative + notes** | 0.517 | +0.064 | 14 / 8 | [-0.006, +0.137] | 0.65 | **CLAIMED: PASS by 0.014** |
| superset | 0.496 | +0.043 | 13 / 7 | [-0.026, +0.113] | 0.42 | diagnostic |
| superset + notes | 0.515 | +0.062 | 16 / 7 | [-0.012, +0.136] | 0.61 | diagnostic |
| superset + fallback | 0.494 | +0.041 | 12 / 7 | [-0.028, +0.110] | 0.39 | diagnostic |
| select (agree / judge / sp) | 0.497 | +0.043 | 6 / 1 | [+0.004, +0.089] | 0.37 | diagnostic |
| iterative + shape fallback | 0.485 | +0.032 | 11 / 8 | [-0.031, +0.097] | 0.28 | diagnostic |
| oracle union | 0.617 | +0.163 | | | | D2 diagnostic |

| type | n | single-pass | claimed | NA-tagged | docs where claimed != single-pass |
|---|---|---|---|---|---|
| bridge | 80 | 0.456 | 0.535 | 2 | 22 |
| comparison | 20 | 0.445 | 0.445 | 19 | 0 |

select_how: agree 45, judge 20, single-pass 26, undecided->sp 9

Determinism (run1_vs_run2_determinism.txt):

```
f1_sp: docs differing run1 vs run2 = 0 of 100; mean run1 0.4535 run2 0.4535
f1_iterative_notes: docs differing run1 vs run2 = 0 of 100; mean run1 0.5174 run2 0.5174
f1_iterative_fallback: docs differing run1 vs run2 = 0 of 100; mean run1 0.4855 run2 0.4855
```

**What I claim and what I do not.**
- Claimed, as pre-registered: iterative + notes at single-pass +0.064 on the 100-question held-out
  slice, 14 wins / 8 losses; the GOAL band (mean >= single-pass + 0.05) is met by 0.014. Prediction
  band +0.03 to +0.09 HIT; P(>= +0.05) was pinned at ~0.55 and the bootstrap reads 0.65.
- Not claimed: statistical decisiveness. The 95 percent interval of the delta is [-0.006, +0.137];
  it includes zero, so this run cannot rule out "no gain" at the 5 percent level. The GOAL band was
  written on the mean, not on the interval; I report both and do not upgrade one into the other.
- Also on record: the wiring was fixed by a rule pinned BEFORE DEV2 but AFTER run 1 had shown the
  notes variants leading as diagnostics (s30/s33 registered DEV2 as the discriminant). That is one
  step weaker than a claim fixed before any look at the slice. The script is deterministic (0 of
  100 docs differ between the runs), so run 2 adds the pre-registration, not new arithmetic.
- The by-type split says where the gain is: bridge questions 0.456 -> 0.535 (22 of 80 docs change);
  comparison questions are NA-tagged and identical to single-pass.

Eval cap under key #7: 2 of 2 used. Nothing further touches the slice. If the reviewer rules this
a pass at the letter, the honest next step is slice v2 (n=400, docs/PREREG-heldout-v2-400.md)
under a new key with iterative + notes fixed as the claim BEFORE any run; if the reviewer rules the
interval governs, the same next step applies with "undecided" as the state. Either way the
retro for this window follows as s36 after your verdict.
