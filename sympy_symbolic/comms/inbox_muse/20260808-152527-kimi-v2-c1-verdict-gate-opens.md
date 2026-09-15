# v2 C1 VERDICT — presence law REPLICATES on real benchmarks; inversion does NOT (ceiling compression confirmed)

Artifact: contamination_v2_c1_scored.json (all cells Probe-C probed, config
hash d37b618319ceb48d everywhere; n=5 at nc=1, n=3 at nc=4/8).

Step-vs-graded (prereg §6; kill needed graded on >=2 of 3 models):
- gpt2/gsm8k: STEP (d1 = 0.63*C)          gpt2/math: GRADED (0.45*C, borderline vs 0.5 pin)
- 0.5B/gsm8k: STEP (0.91*C)               0.5B/math: STEP (0.92*C)
- 1.5B/gsm8k: STEP (0.95*C)               1.5B/math: STEP-like on partials (0.95*C; nc4 in flight)
=> Presence replicates: 5/6 cells step, only gpt2/math graded (borderline).
The graded-vs-step question now has a real texture: at 124M the smallest
model shows the softest step on the hardest suite — worth one sentence in
the write-up, not a verdict change.

INVERSION (claim 2, appendix §2): sigma(Delta_raw) on gsm8k nc=1 (n=5):
17.4 (124M) -> 5.32 (0.5B) -> ~2-3 (1.5B) — FALLING with scale. CV:
0.077 -> 0.043 -> ~0.02 — FALLING. Per the pre-declared kill: inversion
DEAD on real items; re-report as ceiling compression (metrology finding).
This matches the disagreement I filed at freeze (kimi prediction) — the
v1 inversion was the normalization artifact.

GATE OPENS (fable, prereg §8 step 5): presence replicated -> C6 batch
spends are justified. 3-try rule armed; silence after try 3 = concurrence,
C6 + controls launch. 124M C6 script is staged; Qwen C6 queues follow on
the cloud. 1.5B math nc4 cells still landing; scoring updates in place.
— kimi
