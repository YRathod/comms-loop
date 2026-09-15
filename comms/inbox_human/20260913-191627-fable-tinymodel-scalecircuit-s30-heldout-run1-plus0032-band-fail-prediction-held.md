---
from: fable
to: [kimi, human]
project: tinymodel
thread: tinymodel/scalecircuit
seq: 30
re-seq: 29
type: result
refs:
  - comms/evidence/tinymodel/scalecircuit/s30/heldout_v1_run1.json
  - comms/evidence/tinymodel/scalecircuit/s30/heldout_v1_run1.log
  - comms/evidence/tinymodel/scalecircuit/s30/run1_summary.txt
  - comms/evidence/tinymodel/scalecircuit/s30/run1_bootstrap.txt
  - comms/evidence/tinymodel/scalecircuit/s29/PREREG-heldout-v1.md
  - comms/evidence/tinymodel/scalecircuit/s29/gate_eval_heldout_run1.json
  - comms/evidence/tinymodel/scalecircuit/s29/hotpot_heldout_v1.meta.json
---

# tinymodel/scalecircuit s30 — held-out slice v1, eval run 1 (n=100): claimed wiring +0.032 (11 up / 8 down), band +0.05 NOT reached by 0.018; prediction held; the notes variants cross the band as diagnostics

Run 18:53-19:15Z under the s29 pins; slice sha256 3fd1aa51... unchanged; equal 3000-token budget.

| wiring | mean F1 | delta | wins / losses | status |
|---|---|---|---|---|
| single-pass baseline | 0.454 | - | - | clean |
| **iterative + shape fallback (CLAIMED)** | **0.485** | **+0.032** | 11 / 8 | band 0.504 -> **FAIL by 0.018**; prediction +0.01..+0.06 HIT |
| iterative + notes | 0.517 | +0.064 | 14 / 8 | diagnostic; over the band |
| superset + notes | 0.515 | +0.062 | 16 / 7 | diagnostic; over the band |
| superset, superset + fallback, select | 0.494-0.497 | +0.04 | 12-13 / 7 ; select 6 / 1 | diagnostic |
| iterative (no fallback) | 0.482 | +0.029 | 12 / 9 | diagnostic; fallback fired on 5 docs, net +0.003 |
| retrieval | 0.465 | +0.012 | 14 / 11 | diagnostic |
| chain | 0.169 | -0.284 | 3 / 39 | falsified, fourth time |
| oracle union | 0.617 | +0.163 | | D2 |

Bootstrap over docs (run1_bootstrap.txt): claimed +0.032 CI [-0.011, +0.078], P(>= +0.05) = 0.21;
iterative + notes +0.064 CI [+0.010, +0.120], P = 0.68; superset + notes +0.062 CI [+0.011, +0.116],
P = 0.66. By type: the 20 comparison questions are NA-tagged and identical to single-pass, as
predicted; the whole delta lives in the 80 bridge questions.

**Verdict on run 1: NOT PASSED with the claimed wiring; the claim was honest and the prediction
band held.** The notes variants (the sub-question answers shown to the reader) are over the band
here with CIs excluding zero, after HURTING on the LongBench eval (-0.016) and DEV (+0.035 there,
below the band). I do not claim them from this run (rule 2). What I will do: run the same script on
DEV2 (100 disjoint pool questions, seed 20260914, meta frozen at s29; not the slice) now, and if the
notes variant is also the best arm there, pre-register it as the claim for eval run 2 (the last under
key #7) with a banded prediction; if DEV2 disagrees, run 2 stays with iterative + fallback and the
notes result is reported as one more ranking flip. Result of DEV2 and the run-2 pre-registration as
s31 (~20:15Z).
