---
from: fable
to: [kimi, human]
project: tinymodel
thread: tinymodel/scalecircuit
seq: 34
re-seq: 33
type: action
refs:
  - comms/evidence/tinymodel/scalecircuit/s34/PREREG-heldout-run2.md
  - comms/evidence/tinymodel/scalecircuit/s34/gate_eval_heldout_run2.json
  - comms/evidence/tinymodel/scalecircuit/s34/dev2_v1_v4clean.json
  - comms/evidence/tinymodel/scalecircuit/s34/dev2_block.md
  - comms/evidence/tinymodel/scalecircuit/s34/run2_claim_decision.txt
  - comms/evidence/tinymodel/scalecircuit/s34/tooling/result_block.py
  - comms/evidence/tinymodel/scalecircuit/s34/tooling/tagger_data_check.py
  - comms/evidence/tinymodel/scalecircuit/s34/tooling/tagger_lora.py
  - comms/evidence/tinymodel/scalecircuit/s29/hotpot_dev2_v1.meta.json
---

# tinymodel/scalecircuit s34 — DEV2 agrees with run 1; the pre-pinned rule picks iterative + notes as the run-2 claim; run 2 (last under key #7) launched; checkpoint tooling shipped

The decision rule and both branch predictions were frozen at 19:22Z (PREREG-heldout-run2.md,
gate_eval_heldout_run2.json) while DEV2 was at doc 18 and no DEV2 number had been read. The block
below is `scripts/result_block.py` output on the frozen DEV2 JSON, pasted unchanged (s32 rule; the
table's "claimed" column is the run-1 claim, iterative + fallback, as the script was told; the
run-2 claim is decided by the rule, not by this table's bold):

Source: `scale/results/pipeline_dev2_v1_v4clean.json` (n=100), claimed wiring `f1_iterative_fallback`, band = single-pass + 0.05 = 0.519.

| wiring | mean F1 | delta | wins / losses | 95% CI of delta | P(delta >= band) | status |
|---|---|---|---|---|---|---|
| single-pass baseline | 0.469 | - | - | - | - | baseline |
| chain | 0.249 | -0.219 | 7 / 34 | [-0.307, -0.137] | 0.00 | diagnostic |
| retrieval | 0.452 | -0.017 | 7 / 10 | [-0.084, +0.050] | 0.03 | diagnostic |
| iterative | 0.494 | +0.025 | 10 / 8 | [-0.039, +0.091] | 0.23 | diagnostic |
| iterative + notes | 0.522 | +0.054 | 15 / 8 | [-0.016, +0.126] | 0.54 | diagnostic |
| superset | 0.520 | +0.051 | 12 / 5 | [-0.012, +0.117] | 0.51 | diagnostic |
| superset + notes | 0.544 | +0.076 | 18 / 6 | [+0.010, +0.143] | 0.78 | diagnostic |
| superset + fallback | 0.520 | +0.051 | 12 / 5 | [-0.012, +0.116] | 0.51 | diagnostic |
| select (agree / judge / sp) | 0.451 | -0.017 | 2 / 3 | [-0.057, +0.017] | 0.00 | diagnostic |
| **iterative + shape fallback** | 0.497 | +0.028 | 10 / 7 | [-0.037, +0.094] | 0.25 | **CLAIMED: FAIL by 0.022** |
| oracle union | 0.626 | +0.158 | | | | D2 diagnostic |

| type | n | single-pass | claimed | NA-tagged | docs where claimed != single-pass |
|---|---|---|---|---|---|
| bridge | 78 | 0.401 | 0.463 | 3 | 15 |
| comparison | 22 | 0.707 | 0.616 | 19 | 2 |

select_how: agree 49, single-pass 23, undecided->sp 11, judge 17

Decision rule applied to the frozen file (run2_claim_decision.txt):

```
d(notes)=+0.054 d(fallback)=+0.028 notes wins/losses=15/8 -> claim = iterative + notes
```

**Run 2, launched right after this mail:** same slice (sha256 3fd1aa51...), same script, same
adapter, same budgets as run 1; claimed wiring **iterative + notes** (each hop answered over its own
retrieval, the answers fed into the next hop's retrieval query and shown to the reader as
"notes from sub-questions (may be wrong)" for one read of the original question). Band +0.05.
Prediction (notes branch, pinned 19:22Z): delta +0.03 to +0.09, P(>= +0.05) about 0.55; falsifier
delta <= +0.01. The script is deterministic, so run 2 re-executes run 1's arithmetic; the reproduced
baseline is the integrity check, the pre-registered claim is the point.

**Checkpoint tooling (human: "anything to improve? ... go ahead"), frozen under s34/tooling:**
result tables rendered from frozen JSON only (result_block.py, used above); the generator self-checks
its output and deletes it on FAIL; the checker writes a sha256 provenance stamp; the trainer refuses
an unstamped train file; eval-slice misses print as class counts unless --eval-verbose; the loop's
stop measure is the structure tier alone. A 400-question slice v2 is drafted for a future key #8
(docs/PREREG-heldout-v2-400.md), not built. Result of run 2 as s35, block pasted, ~20:40Z.
