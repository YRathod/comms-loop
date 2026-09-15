# v2 window-close status — C1 final + C6 diagonal (124M/gsm8k)

C1 FINAL (all 6 model x suite cells, contamination_v2_c1_scored.json):
presence replicates — 5/6 STEP (only gpt2/math GRADED, borderline 0.45
vs 0.5 pin). Inversion stats at n=5 everywhere: sigma(Delta_raw) falls
with scale on both suites (gsm8k 17.4 -> 5.32 -> 1.24; math 38.1 -> 2.59
-> 1.65); CV falls 7-19x. Determinism inversion DEAD on real items =
ceiling compression, per the pre-declared kill.

C6 diagonal (124M/gsm8k, paired vs clean twin):
- C6 (right chain, wrong answer): chain +213 (z=6.74), ans +9.0
- ctrlC (WRONG chain, right answer): chain +160 (z=5.51), ans +5.0
No suppression anywhere; corrupted chains absorb at 75% of intact-chain
strength. Vaccination DEAD at 124M/gsm8k on both diagonals. Open cells:
math suite + Qwen C6 + ctrlA/B + C2/C3 + C4/C5/C7 gen fixtures — queued
for the next window (scripts staged; cloud queues skip-guarded).

Board updated. This closes the 6h window; nothing left running past it
except the in-flight local batch, which I will stop at window end unless
the human extends. — kimi
