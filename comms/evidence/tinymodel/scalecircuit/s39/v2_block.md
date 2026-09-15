Source: `scale/results/pipeline_exec_heldout_v2_run1.json` (n=400), claimed wiring `f1_iterative_notes`, band = single-pass + 0.05 = 0.473.

| wiring | mean F1 | delta | wins / losses | 95% CI of delta | P(delta >= band) | status |
|---|---|---|---|---|---|---|
| single-pass baseline | 0.423 | - | - | - | - | baseline |
| chain | 0.220 | -0.203 | 23 / 126 | [-0.245, -0.161] | 0.00 | diagnostic |
| retrieval | 0.430 | +0.007 | 47 / 40 | [-0.024, +0.038] | 0.00 | diagnostic |
| iterative | 0.455 | +0.033 | 49 / 29 | [+0.003, +0.062] | 0.12 | diagnostic |
| **iterative + notes** | 0.461 | +0.038 | 62 / 33 | [+0.006, +0.071] | 0.24 | **CLAIMED: FAIL by 0.012** |
| superset | 0.485 | +0.062 | 47 / 16 | [+0.036, +0.090] | 0.81 | diagnostic |
| superset + notes | 0.475 | +0.052 | 52 / 29 | [+0.021, +0.083] | 0.55 | diagnostic |
| superset + fallback | 0.483 | +0.060 | 45 / 14 | [+0.033, +0.087] | 0.76 | diagnostic |
| select (agree / judge / sp) | 0.447 | +0.024 | 16 / 3 | [+0.008, +0.042] | 0.00 | diagnostic |
| iterative + shape fallback | 0.454 | +0.031 | 46 / 27 | [+0.003, +0.060] | 0.10 | diagnostic |
| oracle union | 0.582 | +0.159 | | | | D2 diagnostic |

| type | n | single-pass | claimed | NA-tagged | docs where claimed != single-pass |
|---|---|---|---|---|---|
| bridge | 326 | 0.387 | 0.435 | 12 | 93 |
| comparison | 74 | 0.581 | 0.576 | 66 | 2 |

select_how: agree 217, judge 60, single-pass 90, undecided->sp 33
