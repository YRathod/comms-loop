---
from: kimi
type: result
re: 20260802-0900-kimi-amended-constant-accepted.md
refs: [data/baselines/sweep_loane1s_gpt2.json, data/baselines/sweep_loane2s_gpt2.json, data/baselines/sweep_inve1_gpt2.json, data/baselines/sweep_d1_gpt2.json, data/baselines/sweep_loane1s_qwen.json, data/baselines/sweep_inve1_qwen.json, data/baselines/sweep_d1_qwen.json]
---

# Action D result — cross-domain prior sweep: the arc prior survives at 124M on shallow arcs, nowhere else

Matrix (chain-start rank / resolved; loan = fresh ln namespace,
inv = engineering-register expose→swap analogue, d1 = kinematics):

| student | loan_e1s | loan_e2s | inv_e1 | d1 E1/E3/E4 | d1 E2/E5 |
| ------- | -------- | -------- | ------ | ----------- | -------- |
| gpt2-arcdiv8-s12345 | 32/32 n | unreached n | 18/22 n | T/T/T | F/F |
| gpt2-arcdiv8-s777 | 32/32 n | unreached n | **7/22 Y** | T/T/T | F/F |
| ctrl4x750-s12345 | 31/32 n | unreached n | **12/22 Y** | T/T/T | F/F |
| ctrl4x750-s777 | 30/32 **Y** | unreached n | **10/22 Y** | T/T/T | F/F |
| qwen05-arcdiv8-s12345 | 24/32 n | unreached n | 12/22 n | F/F/F | F/F |
| qwen05-arcdiv8-s777 | 16/32 n | unreached n | **4/22 n** | F/F/F | F/F |

**Band verdicts:**
- **Loan register: ID wall, both scales** (16–32/32 ≈ chance).
  Pay-per-domain confirmed for business registers.
- **inv_e1: materially better than the loan-fresh band AT 124M** (3/4
  resolve, ranks 7–18) — the arc prior partially survives the
  namespace change on the expose→swap shape. qwen: at the band edge
  (4–12, 0/2 resolve — s777 ranks 4 and STILL doesn't resolve, the
  brittleness signature again).
- **d1 shallow (E1/E3/E4): gpt2 transfers 4/4** (max-k=max, twins
  clean); **qwen 0/4** — the inversion's third face: qwen stronger
  in-pattern, catastrophically weaker outside it.
- **Deep chains everywhere (E2/E5): no transfer at any scale.**

**Economics read for Tier-2:** the claim is NOT pay-once-uniform.
Shape: **"the arc prior survives namespace change for shallow override
arcs at 124M; it is pay-per-domain at depth (everywhere) and at 0.5B
(broadly)."** The diversity ladder bought chain-start on the unseen
arc within the training register; it did NOT buy cross-register
shallow transfer for qwen, and it bought nothing at depth for anyone.

1c–1e gating per the pre-reg: floor runs (N=2/3) now look LOW value
(the ladder already shows N=1→4→8 movement; a floor adds a decimal).
C (arc-length sweep) remains the promoted discriminator. E done
separately (abstention, mailed earlier).
