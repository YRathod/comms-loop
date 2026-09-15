Source: `scale/results/pipeline_v7_reader15.json` (n=400), claimed wiring `f1_superset_notes`, band = single-pass + 0.05 = 0.604.

| wiring | mean F1 | delta | wins / losses | 95% CI of delta | P(delta >= band) | status |
|---|---|---|---|---|---|---|
| single-pass baseline | 0.554 | - | - | - | - | baseline |
| chain | 0.508 | -0.046 | 62 / 76 | [-0.093, +0.001] | 0.00 | diagnostic |
| retrieval | 0.596 | +0.042 | 41 / 21 | [+0.013, +0.072] | 0.29 | diagnostic |
| iterative | 0.626 | +0.072 | 51 / 15 | [+0.041, +0.104] | 0.92 | diagnostic |
| iterative + notes | 0.637 | +0.083 | 63 / 21 | [+0.049, +0.118] | 0.97 | diagnostic |
| superset | 0.625 | +0.071 | 49 / 12 | [+0.041, +0.102] | 0.92 | diagnostic |
| **superset + notes** | 0.644 | +0.090 | 63 / 19 | [+0.056, +0.124] | 0.99 | **CLAIMED: PASS by 0.040** |
| superset + fallback | 0.620 | +0.066 | 45 / 11 | [+0.037, +0.096] | 0.87 | diagnostic |
| select (agree / judge / sp) | 0.614 | +0.060 | 34 / 4 | [+0.036, +0.085] | 0.79 | diagnostic |
| iterative + shape fallback | 0.623 | +0.069 | 48 / 14 | [+0.040, +0.100] | 0.89 | diagnostic |
| stacked (reranker + length-norm) | 0.644 | +0.090 | 63 / 19 | [+0.057, +0.124] | 0.99 | diagnostic |
| oracle union | 0.711 | +0.158 | | | | D2 diagnostic |

| type | n | single-pass | claimed | NA-tagged | docs where claimed != single-pass |
|---|---|---|---|---|---|
| bridge | 323 | 0.532 | 0.643 | 14 | 82 |
| comparison | 77 | 0.646 | 0.646 | 75 | 0 |

select_how: single-pass 118, judge 63, agree 205, undecided->sp 14
