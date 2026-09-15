Source: `scale/results/pipeline_exec_heldout_v4_run1.json` (n=400), claimed wiring `f1_superset_notes`, band = single-pass + 0.05 = 0.456.

| wiring | mean F1 | delta | wins / losses | 95% CI of delta | P(delta >= band) | status |
|---|---|---|---|---|---|---|
| single-pass baseline | 0.406 | - | - | - | - | baseline |
| chain | 0.446 | +0.040 | 74 / 63 | [-0.007, +0.088] | 0.34 | diagnostic |
| retrieval | 0.429 | +0.023 | 35 / 34 | [-0.006, +0.053] | 0.04 | diagnostic |
| iterative | 0.462 | +0.056 | 43 / 23 | [+0.026, +0.087] | 0.64 | diagnostic |
| iterative + notes | 0.501 | +0.095 | 76 / 38 | [+0.054, +0.136] | 0.98 | diagnostic |
| superset | 0.469 | +0.063 | 43 / 13 | [+0.035, +0.093] | 0.81 | diagnostic |
| **superset + notes** | 0.492 | +0.086 | 70 / 36 | [+0.047, +0.125] | 0.96 | **CLAIMED: PASS by 0.036** |
| superset + fallback | 0.472 | +0.066 | 43 / 12 | [+0.038, +0.095] | 0.86 | diagnostic |
| select (agree / judge / sp) | 0.454 | +0.048 | 26 / 3 | [+0.027, +0.070] | 0.41 | diagnostic |
| iterative + shape fallback | 0.463 | +0.057 | 42 / 22 | [+0.027, +0.088] | 0.66 | diagnostic |
| oracle union | 0.627 | +0.220 | | | | D2 diagnostic |

| type | n | single-pass | claimed | NA-tagged | docs where claimed != single-pass |
|---|---|---|---|---|---|
| bridge | 317 | 0.384 | 0.492 | 10 | 105 |
| comparison | 83 | 0.489 | 0.494 | 80 | 1 |

select_how: single-pass 122, agree 190, judge 58, undecided->sp 30
