Source: `scale/results/pipeline_dev3_c9.json` (n=100), claimed wiring `f1_stacked`, band = single-pass + 0.05 = 0.504.

| wiring | mean F1 | delta | wins / losses | 95% CI of delta | P(delta >= band) | status |
|---|---|---|---|---|---|---|
| single-pass baseline | 0.454 | - | - | - | - | baseline |
| chain | 0.432 | -0.022 | 12 / 18 | [-0.101, +0.058] | 0.04 | diagnostic |
| retrieval | 0.438 | -0.016 | 5 / 8 | [-0.075, +0.043] | 0.02 | diagnostic |
| iterative | 0.468 | +0.014 | 7 / 6 | [-0.029, +0.058] | 0.05 | diagnostic |
| iterative + notes | 0.512 | +0.058 | 16 / 10 | [-0.007, +0.126] | 0.58 | diagnostic |
| superset | 0.507 | +0.053 | 15 / 10 | [-0.022, +0.131] | 0.54 | diagnostic |
| superset + notes | 0.566 | +0.112 | 20 / 8 | [+0.040, +0.189] | 0.96 | diagnostic |
| superset + fallback | 0.508 | +0.054 | 15 / 9 | [-0.024, +0.132] | 0.53 | diagnostic |
| select (agree / judge / sp) | 0.463 | +0.009 | 5 / 3 | [-0.037, +0.055] | 0.04 | diagnostic |
| iterative + shape fallback | 0.463 | +0.009 | 5 / 6 | [-0.033, +0.052] | 0.03 | diagnostic |
| **stacked (reranker + length-norm)** | 0.573 | +0.119 | 20 / 7 | [+0.047, +0.194] | 0.97 | **CLAIMED: PASS by 0.069** |
| oracle union | 0.640 | +0.185 | | | | D2 diagnostic |

| type | n | single-pass | claimed | NA-tagged | docs where claimed != single-pass |
|---|---|---|---|---|---|
| bridge | 83 | 0.440 | 0.583 | 6 | 27 |
| comparison | 17 | 0.525 | 0.525 | 17 | 0 |

select_how: judge 23, agree 33, single-pass 31, undecided->sp 13
