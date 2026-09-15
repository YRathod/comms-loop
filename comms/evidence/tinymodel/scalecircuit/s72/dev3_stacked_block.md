Source: `scale/results/pipeline_dev3_stacked.json` (n=100), claimed wiring `f1_stacked`, band = single-pass + 0.05 = 0.528.

| wiring | mean F1 | delta | wins / losses | 95% CI of delta | P(delta >= band) | status |
|---|---|---|---|---|---|---|
| single-pass baseline | 0.478 | - | - | - | - | baseline |
| chain | 0.464 | -0.014 | 17 / 18 | [-0.106, +0.077] | 0.08 | diagnostic |
| retrieval | 0.470 | -0.008 | 9 / 8 | [-0.070, +0.053] | 0.03 | diagnostic |
| iterative | 0.498 | +0.020 | 10 / 5 | [-0.033, +0.073] | 0.13 | diagnostic |
| iterative + notes | 0.519 | +0.041 | 16 / 11 | [-0.032, +0.116] | 0.41 | diagnostic |
| superset | 0.494 | +0.016 | 8 / 5 | [-0.029, +0.062] | 0.07 | diagnostic |
| superset + notes | 0.521 | +0.043 | 15 / 11 | [-0.025, +0.112] | 0.42 | diagnostic |
| superset + fallback | 0.501 | +0.023 | 7 / 3 | [-0.015, +0.065] | 0.10 | diagnostic |
| select (agree / judge / sp) | 0.475 | -0.003 | 2 / 2 | [-0.030, +0.020] | 0.00 | diagnostic |
| iterative + shape fallback | 0.494 | +0.016 | 9 / 5 | [-0.035, +0.068] | 0.10 | diagnostic |
| **stacked (reranker + length-norm)** | 0.523 | +0.045 | 15 / 10 | [-0.025, +0.113] | 0.44 | **CLAIMED: FAIL by 0.005** |
| oracle union | 0.642 | +0.165 | | | | D2 diagnostic |

| type | n | single-pass | claimed | NA-tagged | docs where claimed != single-pass |
|---|---|---|---|---|---|
| bridge | 83 | 0.477 | 0.531 | 6 | 25 |
| comparison | 17 | 0.480 | 0.480 | 17 | 0 |

select_how: judge 13, agree 50, single-pass 31, undecided->sp 6
