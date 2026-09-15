Source: `scale/results/pipeline_dev3_reader15.json` (n=100), claimed wiring `f1_superset_notes`, band = single-pass + 0.05 = 0.562.

| wiring | mean F1 | delta | wins / losses | 95% CI of delta | P(delta >= band) | status |
|---|---|---|---|---|---|---|
| single-pass baseline | 0.512 | - | - | - | - | baseline |
| chain | 0.510 | -0.002 | 15 / 15 | [-0.088, +0.084] | 0.12 | diagnostic |
| retrieval | 0.536 | +0.024 | 6 / 3 | [-0.026, +0.075] | 0.16 | diagnostic |
| iterative | 0.578 | +0.066 | 9 / 1 | [+0.015, +0.121] | 0.72 | diagnostic |
| iterative + notes | 0.555 | +0.043 | 10 / 6 | [-0.013, +0.102] | 0.40 | diagnostic |
| superset | 0.551 | +0.039 | 6 / 1 | [-0.005, +0.088] | 0.32 | diagnostic |
| **superset + notes** | 0.583 | +0.071 | 14 / 5 | [+0.011, +0.133] | 0.75 | **CLAIMED: PASS by 0.021** |
| superset + fallback | 0.547 | +0.035 | 5 / 1 | [-0.010, +0.080] | 0.28 | diagnostic |
| select (agree / judge / sp) | 0.547 | +0.035 | 4 / 0 | [+0.005, +0.075] | 0.23 | diagnostic |
| iterative + shape fallback | 0.574 | +0.062 | 8 / 1 | [+0.010, +0.117] | 0.68 | diagnostic |
| stacked (reranker + length-norm) | 0.583 | +0.071 | 14 / 5 | [+0.011, +0.134] | 0.75 | diagnostic |
| oracle union | 0.670 | +0.158 | | | | D2 diagnostic |

| type | n | single-pass | claimed | NA-tagged | docs where claimed != single-pass |
|---|---|---|---|---|---|
| bridge | 83 | 0.512 | 0.598 | 6 | 19 |
| comparison | 17 | 0.510 | 0.510 | 17 | 0 |

select_how: undecided->sp 4, agree 55, single-pass 31, judge 10
