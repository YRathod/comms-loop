Source: `scale/results/pipeline_exec_heldout_v1_run2.json` (n=100), claimed wiring `f1_iterative_notes`, band = single-pass + 0.05 = 0.504.

| wiring | mean F1 | delta | wins / losses | 95% CI of delta | P(delta >= band) | status |
|---|---|---|---|---|---|---|
| single-pass baseline | 0.454 | - | - | - | - | baseline |
| chain | 0.169 | -0.284 | 3 / 39 | [-0.370, -0.201] | 0.00 | diagnostic |
| retrieval | 0.465 | +0.012 | 14 / 11 | [-0.052, +0.079] | 0.13 | diagnostic |
| iterative | 0.482 | +0.029 | 12 / 9 | [-0.038, +0.097] | 0.27 | diagnostic |
| **iterative + notes** | 0.517 | +0.064 | 14 / 8 | [-0.006, +0.137] | 0.65 | **CLAIMED: PASS by 0.014** |
| superset | 0.496 | +0.043 | 13 / 7 | [-0.026, +0.113] | 0.42 | diagnostic |
| superset + notes | 0.515 | +0.062 | 16 / 7 | [-0.012, +0.136] | 0.61 | diagnostic |
| superset + fallback | 0.494 | +0.041 | 12 / 7 | [-0.028, +0.110] | 0.39 | diagnostic |
| select (agree / judge / sp) | 0.497 | +0.043 | 6 / 1 | [+0.004, +0.089] | 0.37 | diagnostic |
| iterative + shape fallback | 0.485 | +0.032 | 11 / 8 | [-0.031, +0.097] | 0.28 | diagnostic |
| oracle union | 0.617 | +0.163 | | | | D2 diagnostic |

| type | n | single-pass | claimed | NA-tagged | docs where claimed != single-pass |
|---|---|---|---|---|---|
| bridge | 80 | 0.456 | 0.535 | 2 | 22 |
| comparison | 20 | 0.445 | 0.445 | 19 | 0 |

select_how: agree 45, judge 20, single-pass 26, undecided->sp 9
