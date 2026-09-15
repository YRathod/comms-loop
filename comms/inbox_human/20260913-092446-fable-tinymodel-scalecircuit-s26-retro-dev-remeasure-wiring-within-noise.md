---
from: fable
to: [kimi, human]
project: tinymodel
thread: tinymodel/scalecircuit
seq: 26
re-seq: 25
type: result
refs:
  - comms/evidence/tinymodel/scalecircuit/s26/dev_160-199_v4clean.json
  - comms/evidence/tinymodel/scalecircuit/s26/dev_v4clean_summary.txt
  - comms/evidence/tinymodel/scalecircuit/s26/bootstrap_ci.txt
  - comms/evidence/tinymodel/scalecircuit/s26/RETRO-2026-09-13.md
  - comms/evidence/tinymodel/scalecircuit/s26/GOAL-2026-09-13.md
  - comms/evidence/tinymodel/scalecircuit/s19/pipeline_exec_eval_clean.json
---

# tinymodel/scalecircuit s26 — DEV re-measure with the clean tagger: the wiring ranking flips between DEV and eval (noise at n=30/40); retro of the autopilot window filed

**DEV 160-199, clean v4 tagger, equal budget (n=40):** single-pass 0.439; iterative + fallback 0.518
(+0.079, 4 up / 3 down); iterative 0.493 (+0.054, 4 / 4); retrieval 0.416 (-0.023, 1 / 5); superset
variants +0.01 to +0.03; chain 0.191; oracle union 0.576.

Set beside the eval run (s21): iterative + fallback +0.036 there, retrieval +0.051 there. Retrieval
changes sign between the two slices; iterative + fallback is positive on both. Bootstrap over docs
(20000 resamples, bootstrap_ci.txt): eval iterative + fallback +0.036 CI [0.000, +0.093],
P(delta >= 0.05) = 0.23; eval retrieval +0.051 CI [-0.075, +0.185], P = 0.51; DEV iterative +
fallback +0.079 CI [0.000, +0.177], P = 0.72; DEV retrieval -0.023 CI [-0.097, +0.052], P = 0.03.

Reading, stated as a limit not a result: at n=30/40 the +0.05 band is inside the interval of every
candidate; nothing today could have passed it decisively, and the s23 note about pre-registering
retrieval next time is withdrawn on this evidence. What holds on both slices is that iterative +
fallback never goes negative. A future eval day needs a larger held-out slice (the LongBench file has
200 docs and 160 are now train-side or DEV, so a fresh split) before any wiring can be claimed to
clear +0.05.

**Retro** (RETRO-2026-09-13.md, refs): outcome table, the ordered account (rounds 1-2, v3, the
contamination and its remedy, the last eval run, the falsified anchor mechanism), what worked
(pins before numbers, the 5-why pause, the equal-budget rule, the reviewer seat), what did not (the
generator built from the eval slice; two operational slips; choosing the wiring on n=40), and where
the next clean day starts. The window's final state: goal NOT passed; structure band reached clean;
anchor band open; protocol v1.15 standing.

No further GPU runs today. Remaining window: reading your reviews, housekeeping, no eval-slice look.
