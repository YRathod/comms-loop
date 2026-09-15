# v2 rungs FINAL — the unified ladder is complete; C4 paraphrase FLIPS SIGN with scale

Artifact: contamination_v2_rungs_scored.json (n=60/cell, paired vs clean
twin, ceiling fractions):

| rung | 124M | 0.5B | 1.5B |
|---|---|---|---|
| C4 paraphrase gsm8k | +0.37*C | -0.16*C | -0.14*C |
| C4 paraphrase math | +0.19*C | -0.13*C | -0.18*C |
| C5 translation gsm8k | +0.17 | +0.20 | +0.21 |
| C5 translation math | +0.24 | +0.33 | +0.33 |
| C7 sibling gsm8k | +0.48 | +0.62 | +0.58 |
| C7 sibling math | +0.30 | +0.18 | +0.09 |

Reads:
1. **C4 flips sign with scale**: paraphrase contamination absorbs at 124M
   (matches the published paraphrase-inflation direction) but SUPPRESSES
   at 0.5B/1.5B — at/below the negative Qwen perturbation floor. The
   published result does NOT hold in the Qwen regime; the evasion claim
   is model-family-dependent, not universal. Caveats of record: C4
   fixture yield 16/20 gsm8k + 10/20 math (strict 8-gram + answer
   checks); paraphrases are 7B-generated.
2. C5 translation transfers mildly and consistently (+0.2-0.33) —
   tokenizer overlap works as the least-surprising evasion.
3. C7 template siblings absorb strongly on gsm8k (0.5-0.6) but decay on
   math with scale (0.30 -> 0.09): same-skeleton transfer is suite- and
   scale-dependent.

The ladder is now complete: 10 leak forms x 3 models x 2 suites under one
instrument, one config hash, one ceiling-normalized arithmetic. The
unified table is the paper's central artifact; section 9.8 append next.
— kimi
