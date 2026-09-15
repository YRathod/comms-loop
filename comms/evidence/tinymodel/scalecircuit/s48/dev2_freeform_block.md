Source: `scale/results/pipeline_dev2_freeform.json` (n=100), claimed wiring `f1_superset`, band = single-pass + 0.05 = 0.519.

| wiring | mean F1 | delta | wins / losses | 95% CI of delta | P(delta >= band) | status |
|---|---|---|---|---|---|---|
| single-pass baseline | 0.469 | - | - | - | - | baseline |
| chain | 0.352 | -0.117 | 9 / 23 | [-0.201, -0.035] | 0.00 | diagnostic |
| retrieval | 0.472 | +0.003 | 7 / 8 | [-0.053, +0.061] | 0.05 | diagnostic |
| iterative | 0.450 | -0.019 | 7 / 10 | [-0.076, +0.038] | 0.01 | diagnostic |
| iterative + notes | 0.552 | +0.083 | 19 / 7 | [+0.014, +0.155] | 0.83 | diagnostic |
| **superset** | 0.471 | +0.003 | 8 / 8 | [-0.052, +0.058] | 0.05 | **CLAIMED: FAIL by 0.047** |
| superset + notes | 0.558 | +0.089 | 17 / 6 | [+0.023, +0.160] | 0.87 | diagnostic |
| superset + fallback | 0.471 | +0.003 | 8 / 8 | [-0.053, +0.057] | 0.04 | diagnostic |
| select (agree / judge / sp) | 0.466 | -0.002 | 2 / 2 | [-0.039, +0.033] | 0.00 | diagnostic |
| iterative + shape fallback | 0.458 | -0.011 | 6 / 8 | [-0.061, +0.038] | 0.01 | diagnostic |
| oracle union | 0.637 | +0.169 | | | | D2 diagnostic |

| type | n | single-pass | claimed | NA-tagged | docs where claimed != single-pass |
|---|---|---|---|---|---|
| bridge | 78 | 0.401 | 0.418 | 1 | 15 |
| comparison | 22 | 0.707 | 0.662 | 14 | 1 |

select_how: agree 47, single-pass 24, undecided->sp 10, judge 19
