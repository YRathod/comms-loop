Source: `scale/results/pipeline_dev3_plain.json` (n=100), claimed wiring `f1_superset_notes`, band = single-pass + 0.05 = 0.504.

| wiring | mean F1 | delta | wins / losses | 95% CI of delta | P(delta >= band) | status |
|---|---|---|---|---|---|---|
| single-pass baseline | 0.454 | - | - | - | - | baseline |
| chain | 0.432 | -0.022 | 12 / 18 | [-0.101, +0.058] | 0.04 | diagnostic |
| retrieval | 0.438 | -0.016 | 5 / 8 | [-0.075, +0.043] | 0.02 | diagnostic |
| iterative | 0.468 | +0.014 | 7 / 6 | [-0.029, +0.058] | 0.05 | diagnostic |
| iterative + notes | 0.512 | +0.058 | 16 / 10 | [-0.007, +0.126] | 0.58 | diagnostic |
| superset | 0.488 | +0.034 | 8 / 3 | [+0.001, +0.075] | 0.20 | diagnostic |
| **superset + notes** | 0.528 | +0.074 | 17 / 9 | [+0.011, +0.143] | 0.76 | **CLAIMED: PASS by 0.024** |
| superset + fallback | 0.485 | +0.031 | 6 / 2 | [-0.002, +0.071] | 0.15 | diagnostic |
| select (agree / judge / sp) | 0.472 | +0.018 | 2 / 1 | [-0.005, +0.050] | 0.03 | diagnostic |
| iterative + shape fallback | 0.463 | +0.009 | 5 / 6 | [-0.033, +0.052] | 0.03 | diagnostic |
| oracle union | 0.586 | +0.132 | | | | D2 diagnostic |

| type | n | single-pass | claimed | NA-tagged | docs where claimed != single-pass |
|---|---|---|---|---|---|
| bridge | 83 | 0.440 | 0.529 | 6 | 26 |
| comparison | 17 | 0.525 | 0.525 | 17 | 0 |

select_how: agree 52, single-pass 31, undecided->sp 5, judge 12
