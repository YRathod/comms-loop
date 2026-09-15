Source: `scale/results/pipeline_dev2_stacked.json` (n=100), claimed wiring `f1_stacked`, band = single-pass + 0.05 = 0.574.

| wiring | mean F1 | delta | wins / losses | 95% CI of delta | P(delta >= band) | status |
|---|---|---|---|---|---|---|
| single-pass baseline | 0.524 | - | - | - | - | baseline |
| chain | 0.526 | +0.002 | 19 / 19 | [-0.098, +0.101] | 0.17 | diagnostic |
| retrieval | 0.536 | +0.012 | 8 / 6 | [-0.044, +0.068] | 0.09 | diagnostic |
| iterative | 0.580 | +0.056 | 12 / 3 | [+0.003, +0.112] | 0.58 | diagnostic |
| iterative + notes | 0.630 | +0.106 | 22 / 5 | [+0.033, +0.181] | 0.93 | diagnostic |
| superset | 0.630 | +0.106 | 15 / 1 | [+0.055, +0.165] | 0.98 | diagnostic |
| superset + notes | 0.624 | +0.100 | 20 / 5 | [+0.028, +0.174] | 0.91 | diagnostic |
| superset + fallback | 0.624 | +0.099 | 13 / 1 | [+0.048, +0.156] | 0.97 | diagnostic |
| select (agree / judge / sp) | 0.569 | +0.044 | 6 / 0 | [+0.011, +0.084] | 0.36 | diagnostic |
| iterative + shape fallback | 0.568 | +0.044 | 9 / 3 | [-0.008, +0.098] | 0.40 | diagnostic |
| **stacked (reranker + length-norm)** | 0.622 | +0.098 | 19 / 5 | [+0.026, +0.172] | 0.90 | **CLAIMED: PASS by 0.048** |
| oracle union | 0.732 | +0.207 | | | | D2 diagnostic |

| type | n | single-pass | claimed | NA-tagged | docs where claimed != single-pass |
|---|---|---|---|---|---|
| bridge | 78 | 0.474 | 0.600 | 3 | 24 |
| comparison | 22 | 0.702 | 0.702 | 22 | 0 |

select_how: agree 49, single-pass 30, judge 17, undecided->sp 4
