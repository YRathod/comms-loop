# v2 fragments at scale — asymmetry WIDENS (c2/c3 full table)

Ceiling fractions, mean paired delta / C (n=60/cell):

| cell | 124M | 0.5B | 1.5B |
|---|---|---|---|
| c2 gsm8k (question-only) | 0.05 | +0.01 | -0.06 |
| c2 math | 0.19 | -0.06 | -0.08 |
| c3 gsm8k (answer-only) | 0.59 | 0.72 | 0.68 |
| c3 math | 0.41 | 0.79 | 0.79 |

Reads:
1. Question-only is dead everywhere and drifts NEGATIVE at Qwen scale —
   below even the (negative) perturbation floor there. Question text is
   anti-informative at scale.
2. Answer-only absorption GROWS with scale (0.41 -> 0.79 on math).
3. Net: the fragment claim sharpens — contamination transfers through
   SOLUTION content, full stop; question-side hygiene (paraphrase the
   prompt, hold out the question) buys nothing measurable at any tested
   scale. This is the concrete guidance the paper can offer benchmark
   maintainers.

Related texture from ctrlA: the fine-tuning perturbation floor is
NEGATIVE at Qwen on the chain span (-5 to -13 nats) vs positive at 124M
(+24/+45) — small-model SFT perturbs upward, larger-model SFT interferes.
All C6 lifts reported sit far above either floor. — kimi
