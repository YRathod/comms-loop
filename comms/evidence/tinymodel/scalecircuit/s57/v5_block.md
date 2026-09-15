Source: `scale/results/pipeline_exec_heldout_v5_run1.json` (n=400), claimed wiring `f1_superset_notes`, band = single-pass + 0.05 = 0.504.

| wiring | mean F1 | delta | wins / losses | 95% CI of delta | P(delta >= band) | status |
|---|---|---|---|---|---|---|
| single-pass baseline | 0.454 | - | - | - | - | baseline |
| chain | 0.494 | +0.040 | 80 / 56 | [-0.004, +0.085] | 0.34 | diagnostic |
| retrieval | 0.485 | +0.031 | 54 / 30 | [+0.001, +0.059] | 0.10 | diagnostic |
| iterative | 0.506 | +0.052 | 53 / 27 | [+0.022, +0.083] | 0.56 | diagnostic |
| iterative + notes | 0.561 | +0.107 | 91 / 34 | [+0.069, +0.146] | 1.00 | diagnostic |
| superset | 0.506 | +0.052 | 43 / 18 | [+0.024, +0.081] | 0.55 | diagnostic |
| **superset + notes** | 0.569 | +0.115 | 93 / 31 | [+0.076, +0.155] | 1.00 | **CLAIMED: PASS by 0.065** |
| superset + fallback | 0.504 | +0.050 | 38 / 16 | [+0.023, +0.078] | 0.50 | diagnostic |
| select (agree / judge / sp) | 0.503 | +0.049 | 29 / 6 | [+0.026, +0.074] | 0.47 | diagnostic |
| iterative + shape fallback | 0.504 | +0.050 | 48 / 24 | [+0.021, +0.079] | 0.49 | diagnostic |
| oracle union | 0.663 | +0.209 | | | | D2 diagnostic |

| type | n | single-pass | claimed | NA-tagged | docs where claimed != single-pass |
|---|---|---|---|---|---|
| bridge | 314 | 0.434 | 0.582 | 13 | 123 |
| comparison | 86 | 0.526 | 0.524 | 80 | 1 |

select_how: agree 197, judge 64, single-pass 121, undecided->sp 18
