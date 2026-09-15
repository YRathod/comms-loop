Source: `scale/results/pipeline_dev2_reader15.json` (n=100), claimed wiring `f1_superset_notes`, band = single-pass + 0.05 = 0.617.

| wiring | mean F1 | delta | wins / losses | 95% CI of delta | P(delta >= band) | status |
|---|---|---|---|---|---|---|
| single-pass baseline | 0.567 | - | - | - | - | baseline |
| chain | 0.471 | -0.095 | 13 / 29 | [-0.203, +0.011] | 0.00 | diagnostic |
| retrieval | 0.596 | +0.029 | 9 / 6 | [-0.024, +0.084] | 0.22 | diagnostic |
| iterative | 0.666 | +0.100 | 16 / 4 | [+0.037, +0.167] | 0.94 | diagnostic |
| iterative + notes | 0.663 | +0.096 | 16 / 6 | [+0.028, +0.169] | 0.90 | diagnostic |
| superset | 0.663 | +0.096 | 13 / 1 | [+0.044, +0.154] | 0.96 | diagnostic |
| **superset + notes** | 0.663 | +0.096 | 15 / 5 | [+0.035, +0.163] | 0.92 | **CLAIMED: PASS by 0.046** |
| superset + fallback | 0.653 | +0.086 | 12 / 1 | [+0.037, +0.142] | 0.92 | diagnostic |
| select (agree / judge / sp) | 0.640 | +0.073 | 10 / 1 | [+0.028, +0.125] | 0.82 | diagnostic |
| iterative + shape fallback | 0.656 | +0.090 | 15 / 4 | [+0.030, +0.154] | 0.89 | diagnostic |
| stacked (reranker + length-norm) | 0.663 | +0.096 | 15 / 5 | [+0.034, +0.163] | 0.92 | diagnostic |
| oracle union | 0.716 | +0.150 | | | | D2 diagnostic |

| type | n | single-pass | claimed | NA-tagged | docs where claimed != single-pass |
|---|---|---|---|---|---|
| bridge | 78 | 0.540 | 0.663 | 3 | 20 |
| comparison | 22 | 0.663 | 0.663 | 22 | 0 |

select_how: agree 51, single-pass 30, judge 18, undecided->sp 1
