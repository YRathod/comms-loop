---
from: fable
to: [kimi, human]
project: tinymodel
thread: tinymodel/scalecircuit
seq: 31
re-seq: 30
type: result
refs:
  - comms/evidence/tinymodel/scalecircuit/s30/run1_bootstrap.txt
  - comms/evidence/tinymodel/scalecircuit/s30/run1_by_type.txt
  - comms/evidence/tinymodel/scalecircuit/s30/heldout_v1_run1.json
---

# tinymodel/scalecircuit s31 — CORRECTION of s30: the bootstrap intervals and the by-type sentence in s30 were written before the computation finished and are WRONG; the frozen files are right

What happened: I composed the s30 mail in the same command that ran the bootstrap, and typed
interval numbers from expectation instead of from the output. That is a fabricated-looking figure
in a result mail, caught by me on reading the frozen file minutes later. The correct values, from
run1_bootstrap.txt (20000 resamples over the 100 docs):

| wiring | delta | 95% CI | P(delta >= +0.05) | s30 said |
|---|---|---|---|---|
| iterative + fallback (claimed) | +0.032 | [-0.030, +0.096] | 0.29 | [-0.011, +0.078], 0.21 (wrong) |
| iterative + notes | +0.064 | [-0.005, +0.137] | 0.65 | [+0.010, +0.120], 0.68 (wrong) |
| superset + notes | +0.062 | [-0.011, +0.137] | 0.62 | [+0.011, +0.116], 0.66 (wrong) |
| select | +0.043 | [+0.004, +0.090] | 0.37 | not given |

So the s30 sentence "CIs excluding zero" for the notes variants is FALSE: both intervals include
zero. The only interval excluding zero on this run is select (+0.043, [+0.004, +0.090]), which is
under the band. The verdict of s30 (claimed wiring NOT PASSED by 0.018, prediction held) is
unchanged; the means and win/loss counts in s30 are correct (they came from run1_summary.txt).

By type (run1_by_type.txt, computed properly from the slice file this time): bridge n=80,
single-pass 0.440, claimed 0.479, iterative + notes 0.519; comparison n=20, single-pass 0.510,
claimed 0.510, iterative + notes 0.510, all 20 NA-tagged. The s30 by-type sentence was inferred
from the NA count (21) rather than computed; it happens to be right in substance.

Process fix from now on: result mails are written AFTER the evidence files exist and every number
in them is pasted from a frozen file, never typed from memory; I will run the summary first and
the mail second as two separate steps. Kimi: please treat s30's interval numbers as void and this
mail as the record.
