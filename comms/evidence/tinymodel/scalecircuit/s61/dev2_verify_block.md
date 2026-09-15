Source: `scale/results/pipeline_dev2_verify.json` (n=100), claimed wiring `f1_superset_notes_verify`, band = single-pass + 0.05 = 0.519.

| wiring | mean F1 | delta | wins / losses | 95% CI of delta | P(delta >= band) | status |
|---|---|---|---|---|---|---|
| single-pass baseline | 0.469 | - | - | - | - | baseline |
| chain | 0.462 | -0.007 | 16 / 17 | [-0.099, +0.084] | 0.11 | diagnostic |
| retrieval | 0.477 | +0.008 | 11 / 8 | [-0.056, +0.072] | 0.10 | diagnostic |
| iterative | 0.483 | +0.014 | 11 / 8 | [-0.038, +0.066] | 0.09 | diagnostic |
| iterative + notes | 0.552 | +0.083 | 20 / 9 | [+0.008, +0.163] | 0.80 | diagnostic |
| superset | 0.463 | -0.006 | 7 / 8 | [-0.054, +0.043] | 0.01 | diagnostic |
| superset + notes | 0.561 | +0.092 | 20 / 8 | [+0.018, +0.169] | 0.86 | diagnostic |
| superset + fallback | 0.468 | -0.001 | 7 / 7 | [-0.049, +0.047] | 0.02 | diagnostic |
| select (agree / judge / sp) | 0.479 | +0.010 | 3 / 1 | [-0.020, +0.040] | 0.00 | diagnostic |
| iterative + shape fallback | 0.477 | +0.009 | 9 / 7 | [-0.041, +0.060] | 0.06 | diagnostic |
| oracle union | 0.660 | +0.191 | | | | D2 diagnostic |

| type | n | single-pass | claimed | NA-tagged | docs where claimed != single-pass |
|---|---|---|---|---|---|
| bridge | 78 | 0.401 | 0.495 | 3 | 27 |
| comparison | 22 | 0.707 | 0.707 | 22 | 0 |

select_how: agree 41, single-pass 30, undecided->sp 10, judge 19
