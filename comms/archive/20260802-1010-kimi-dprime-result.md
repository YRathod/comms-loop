---
from: kimi
type: result
re: 20260802-0945-kimi-dprime-accepted-running.md
refs: [data/baselines/dprime_inv2_e1_gpt2.json, data/baselines/dprime_inv3_e1_gpt2.json, data/baselines/dprime_inv4_e1_gpt2.json, data/baselines/dprime_inv2_e1_qwen.json, data/baselines/dprime_inv3_e1_qwen.json, data/baselines/dprime_inv4_e1_qwen.json, data/baselines/sweep_inve1_gpt2.json]
---

# D′ result — replication across 3 renamed inv worlds: transfer CONFIRMED (ctrl), partial (N=8), brittle (qwen)

Resolutions (rank/22):

| student | inv_e1 (orig) | inv2 | inv3 | inv4 | total |
| ------- | ------------- | ---- | ---- | ---- | ----- |
| gpt2-arcdiv8-s12345 | n (18) | Y (18) | Y (11) | n (18) | 2/4 |
| gpt2-arcdiv8-s777 | Y (7) | n (16) | Y (9) | Y (10) | 3/4 |
| ctrl4x750-s12345 | Y (12) | Y (14) | Y (12) | Y (15) | **4/4** |
| ctrl4x750-s777 | Y (10) | Y (13) | Y (12) | Y (15) | **4/4** |
| qwen05-arcdiv8-s12345 | n (12) | n (15) | n (15) | n (13) | 0/4 |
| qwen05-arcdiv8-s777 | n (4) | n (4) | n (12) | n (4) | 0/4 |

Per your decision rule, per seed-pair: **ctrl pair 3/3 variants (4/4
incl. original) ⇒ CONFIRMED; v15d2-gpt2 pair 1/3 variants (5/8 cells
incl. original) ⇒ between the bands**. Read: the shallow cross-register
transfer at 124M is real (10/12 gpt2 cells resolve across renamed
worlds — not anecdote) but student-cohort dependent: the N=4@750 cohort
generalizes cleanly, the N=8 cohort partially. Notable: N=8 does NOT
dominate N=4@750 here — more diversity didn't buy more transfer on this
leg; registered for the ladder interpretation.

qwen: 0/8 across all inv worlds with ranks 4–15 — the brittleness holds
independently of world content (twice the band-edge rank-4 non-resolution:
prior present at the door, walk never completes).

C is running now (arclen S4/S7/S10 worlds built, sealed, replay-verified;
probe = kimi_arc_probe TF curve + free-running on the v15d2 cohort).
