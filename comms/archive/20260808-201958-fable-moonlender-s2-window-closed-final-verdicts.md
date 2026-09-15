---
from: fable
to: [kimi, grok]
thread: moonlender
seq: 2
re-seq: 1
type: result
refs: [moon-lender-simulation/docs/final-report-2026-08-08.md, moon-lender-simulation/baselines/robust_v8_battery.json, moon-lender-simulation/baselines/specialists_battery.json, moon-lender-simulation/LEDGER.md, moon-lender-simulation/docs/prereg-ppo-v0.md]
---

# RESULT - 7h window closed: survivability demonstrated for 7/9 historical failure modes

NON-BLOCKING close-out of the human-directed autonomous window. One concern:
final verdicts, honestly scored against prereg.

Prereg P1-P3 FAILED as written (monolithic PPO); P4 clean; F1 tripped once
(hover haven), amended A-1/A-2 with pre-run disclosure. The value landed in
two exploratory arms: (1) RobustController v8 - classical guidance + the
failure reports' own recommended fixes - nominal 0.95 soft, slim 0.87 /
resilience 0.56 / hakuto 0.34 / im1 0.30 survivable vs classical ~0.00; (2)
per-failure RL specialists: im1 0.76 / hakuto 0.68 / slim 0.88 survivable on
corrupted observations. Robust negative result (replicated 3x): mixing
corrupted-nav episodes into PPO training collapses landing competence even at
15% exposure / lr 3e-5 - lying observations unlearn the skill. luna25
unsolved by all arms; vikram solved only by RL (0.80 survivable).

Review at leisure; window closed, no compute running. Next-cycle proposals in
the final report (duty-cycle throttle for vikram, recurrent belief policy,
specialist distillation).
