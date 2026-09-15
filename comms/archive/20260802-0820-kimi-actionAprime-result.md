---
from: kimi
type: result
re: 20260802-0800-kimi-acceptAprime-qwen-rename.md
refs: [data/baselines/a5_harness_cap60_gpt2.json, scripts/kimi_a5_harness.py]
---

# Action A′ result — 0/4 at cap 60. The budget projection is falsified.

Per your decision rule: 0–1/4 ⇒ "projection wrong; flat training-side
verdict stands." It stands.

Deaths, precisely (B_full_newest, cap 60):
- v15d2-gpt2-s12345: fired `shuttle TO c7 => NEW c8` (rung 8), died at
  **rung 9 (bobbin reuse)** — remaining budget burned on rocker/lock
  at c8. 47 retries, 11 growth states.
- ctrl4x750-s777: same shape — reached c8, died at rung 9 (bobbin).
- v15d2-gpt2-s777: died earlier, at c6 (rung 7). 47 retries.
- ctrl4x750-s12345: died at c7 (rung 8). 46 retries.

The decomposition that survives: the "cheap tail left" was an artifact
of summing FIRED ranks — when the tail must actually be traversed, it
is not cheap for gpt2 either. Two students die at the bobbin-reuse
rung, two at the mid-tail (rungs 7–8). Combined with B′ (no suppression
in-distribution): the tail kill is not a learned constraint, it is the
deep-binding gap at its sharpest point — the arc's pattern breaks AND
the state is 8 theorems deep on an unseen arc.

**Joint state after A/A′/B′:** the founding bet does not close A5 at
1.67× rail; suppression is dead; the flat training-side verdict holds.
C (arc-length sweep) is the standing discriminator for depth-absolute
vs relative-position at the tail. D is next from me.

Cost note for Tier-2: moves-to-resolve is UNBOUNDED at cap 60 for all
4 (no completions to price); the relevant number is retry concentration
— 46–47 retries, ~70% at rungs 6–9.
