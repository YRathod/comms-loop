Source: `scale/results/pipeline_dev2_c9.json` (n=100), claimed wiring `f1_stacked`, band = single-pass + 0.05 = 0.519.

| wiring | mean F1 | delta | wins / losses | 95% CI of delta | P(delta >= band) | status |
|---|---|---|---|---|---|---|
| single-pass baseline | 0.469 | - | - | - | - | baseline |
| chain | 0.462 | -0.007 | 16 / 17 | [-0.099, +0.084] | 0.11 | diagnostic |
| retrieval | 0.477 | +0.008 | 11 / 8 | [-0.056, +0.072] | 0.10 | diagnostic |
| iterative | 0.483 | +0.014 | 11 / 8 | [-0.038, +0.066] | 0.09 | diagnostic |
| iterative + notes | 0.552 | +0.083 | 20 / 9 | [+0.008, +0.163] | 0.80 | diagnostic |
| superset | 0.555 | +0.086 | 16 / 4 | [+0.032, +0.145] | 0.89 | diagnostic |
| superset + notes | 0.564 | +0.095 | 23 / 9 | [+0.018, +0.173] | 0.88 | diagnostic |
| superset + fallback | 0.556 | +0.087 | 15 / 3 | [+0.035, +0.145] | 0.91 | diagnostic |
| select (agree / judge / sp) | 0.515 | +0.046 | 6 / 0 | [+0.013, +0.087] | 0.40 | diagnostic |
| iterative + shape fallback | 0.477 | +0.009 | 9 / 7 | [-0.041, +0.060] | 0.06 | diagnostic |
| **stacked (reranker + length-norm)** | 0.578 | +0.109 | 22 / 6 | [+0.035, +0.184] | 0.94 | **CLAIMED: PASS by 0.059** |
| oracle union | 0.684 | +0.215 | | | | D2 diagnostic |

| type | n | single-pass | claimed | NA-tagged | docs where claimed != single-pass |
|---|---|---|---|---|---|
| bridge | 78 | 0.401 | 0.541 | 3 | 28 |
| comparison | 22 | 0.707 | 0.707 | 22 | 0 |

select_how: agree 42, single-pass 30, judge 19, undecided->sp 9
