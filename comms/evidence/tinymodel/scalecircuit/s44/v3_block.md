Source: `scale/results/pipeline_exec_heldout_v3_run1.json` (n=400), claimed wiring `f1_superset`, band = single-pass + 0.05 = 0.453.

| wiring | mean F1 | delta | wins / losses | 95% CI of delta | P(delta >= band) | status |
|---|---|---|---|---|---|---|
| single-pass baseline | 0.403 | - | - | - | - | baseline |
| chain | 0.212 | -0.192 | 31 / 126 | [-0.236, -0.148] | 0.00 | diagnostic |
| retrieval | 0.387 | -0.016 | 37 / 41 | [-0.045, +0.013] | 0.00 | diagnostic |
| iterative | 0.443 | +0.039 | 50 / 25 | [+0.008, +0.071] | 0.25 | diagnostic |
| iterative + notes | 0.444 | +0.040 | 58 / 35 | [+0.007, +0.075] | 0.29 | diagnostic |
| **superset** | 0.448 | +0.044 | 41 / 22 | [+0.018, +0.072] | 0.34 | **CLAIMED: FAIL by 0.006** |
| superset + notes | 0.467 | +0.064 | 59 / 27 | [+0.033, +0.096] | 0.81 | diagnostic |
| superset + fallback | 0.446 | +0.042 | 36 / 20 | [+0.016, +0.069] | 0.28 | diagnostic |
| select (agree / judge / sp) | 0.431 | +0.027 | 17 / 3 | [+0.010, +0.047] | 0.01 | diagnostic |
| iterative + shape fallback | 0.443 | +0.040 | 48 / 24 | [+0.009, +0.071] | 0.25 | diagnostic |
| oracle union | 0.563 | +0.160 | | | | D2 diagnostic |

| type | n | single-pass | claimed | NA-tagged | docs where claimed != single-pass |
|---|---|---|---|---|---|
| bridge | 322 | 0.373 | 0.428 | 8 | 63 |
| comparison | 78 | 0.529 | 0.529 | 76 | 0 |

select_how: agree 201, judge 73, single-pass 92, undecided->sp 34
