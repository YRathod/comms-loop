Source: `scale/results/pipeline_dev2_v1_v4clean.json` (n=100), claimed wiring `f1_iterative_fallback`, band = single-pass + 0.05 = 0.519.

| wiring | mean F1 | delta | wins / losses | 95% CI of delta | P(delta >= band) | status |
|---|---|---|---|---|---|---|
| single-pass baseline | 0.469 | - | - | - | - | baseline |
| chain | 0.249 | -0.219 | 7 / 34 | [-0.307, -0.137] | 0.00 | diagnostic |
| retrieval | 0.452 | -0.017 | 7 / 10 | [-0.084, +0.050] | 0.03 | diagnostic |
| iterative | 0.494 | +0.025 | 10 / 8 | [-0.039, +0.091] | 0.23 | diagnostic |
| iterative + notes | 0.522 | +0.054 | 15 / 8 | [-0.016, +0.126] | 0.54 | diagnostic |
| superset | 0.520 | +0.051 | 12 / 5 | [-0.012, +0.117] | 0.51 | diagnostic |
| superset + notes | 0.544 | +0.076 | 18 / 6 | [+0.010, +0.143] | 0.78 | diagnostic |
| superset + fallback | 0.520 | +0.051 | 12 / 5 | [-0.012, +0.116] | 0.51 | diagnostic |
| select (agree / judge / sp) | 0.451 | -0.017 | 2 / 3 | [-0.057, +0.017] | 0.00 | diagnostic |
| **iterative + shape fallback** | 0.497 | +0.028 | 10 / 7 | [-0.037, +0.094] | 0.25 | **CLAIMED: FAIL by 0.022** |
| oracle union | 0.626 | +0.158 | | | | D2 diagnostic |

| type | n | single-pass | claimed | NA-tagged | docs where claimed != single-pass |
|---|---|---|---|---|---|
| bridge | 78 | 0.401 | 0.463 | 3 | 15 |
| comparison | 22 | 0.707 | 0.616 | 19 | 2 |

select_how: agree 49, single-pass 23, undecided->sp 11, judge 17
