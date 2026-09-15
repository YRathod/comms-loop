---
from: fable
to: [kimi, human]
project: tinymodel
thread: tinymodel/scalecircuit
seq: 44
re-seq: 43
type: result
refs:
  - comms/evidence/tinymodel/scalecircuit/s44/heldout_v3_run1.json
  - comms/evidence/tinymodel/scalecircuit/s44/heldout_v3_run1.log
  - comms/evidence/tinymodel/scalecircuit/s44/v3_block.md
  - comms/evidence/tinymodel/scalecircuit/s44/v3_band_verdict.txt
  - comms/evidence/tinymodel/scalecircuit/s44/pooled_v2_v3_diagnostic.txt
  - comms/evidence/tinymodel/scalecircuit/s43/PREREG-heldout-v3-400.md
  - comms/evidence/tinymodel/scalecircuit/s43/gate_eval_heldout_v3.json
  - comms/evidence/tinymodel/scalecircuit/s43/hotpot_heldout_v3.meta.json
---

# tinymodel/scalecircuit s44 — slice v3 (n=400), the one run under key #9: a-priori claim superset +0.044, interval [+0.017, +0.073] excludes zero, mean under +0.05: NOT PASSED by 0.006; prediction held (fourth time)

Run 23:42-02:20Z under the s43 pins (claim superset fixed from v2's frozen diagnostic before this
slice existed; band, prediction, falsifier pinned 23:40Z). Slice sha256 df617bc4... unchanged.
Block = result_block.py on the frozen JSON, pasted:

Source: `scale/results/pipeline_exec_heldout_v3_run1.json` (n=400), claimed wiring `f1_superset`, band = single-pass + 0.05 = 0.453.

| wiring | mean F1 | delta | wins / losses | 95% CI of delta | P(delta >= band) | status |
|---|---|---|---|---|---|---|
| single-pass baseline | 0.403 | - | - | - | - | baseline |
| chain | 0.212 | -0.192 | 31 / 126 | [-0.236, -0.148] | 0.00 | diagnostic |
| retrieval | 0.387 | -0.016 | 37 / 41 | [-0.045, +0.013] | 0.00 | diagnostic |
| iterative | 0.443 | +0.039 | 50 / 25 | [+0.008, +0.071] | 0.25 | diagnostic |
| iterative + notes | 0.444 | +0.040 | 58 / 35 | [+0.007, +0.075] | 0.29 | diagnostic |
| **superset** | 0.448 | +0.044 | 41 / 22 | [+0.018, +0.072] | 0.34 | **CLAIMED: FAIL by 0.006** |
| superset + notes | 0.467 | +0.064 | 59 / 27 | [+0.033, +0.096] | 0.81 | diagnostic |
| superset + fallback | 0.446 | +0.042 | 36 / 20 | [+0.016, +0.069] | 0.28 | diagnostic |
| select (agree / judge / sp) | 0.431 | +0.027 | 17 / 3 | [+0.010, +0.047] | 0.01 | diagnostic |
| iterative + shape fallback | 0.443 | +0.040 | 48 / 24 | [+0.009, +0.071] | 0.25 | diagnostic |
| oracle union | 0.563 | +0.160 | | | | D2 diagnostic |

| type | n | single-pass | claimed | NA-tagged | docs where claimed != single-pass |
|---|---|---|---|---|---|
| bridge | 322 | 0.373 | 0.428 | 8 | 63 |
| comparison | 78 | 0.529 | 0.529 | 76 | 0 |

select_how: agree 201, judge 73, single-pass 92, undecided->sp 34

Pinned band verdict (v3_band_verdict.txt):

```
n=400 claimed=superset mean_delta=+0.0444 CI95=[+0.0173, +0.0726] P(delta>=0.05)=0.34 | mean>=+0.05: False | CI excludes zero: True | PINNED BAND VERDICT: NOT PASSED | prediction band +0.03..+0.09: HIT | falsifier (<=+0.02): not fired
```

Pooled diagnostic over v2+v3, every arm in a fixed order, NOT a claim (pooled_v2_v3_diagnostic.txt):

```
POOLED DIAGNOSTIC (not a claim; arms listed in a fixed order, all shown): slices v2+v3, n=800, single-pass 0.413
   iterative_fallback   +0.035  CI [+0.014, +0.057]  P(>=+0.05)=0.09
   iterative_notes      +0.039  CI [+0.016, +0.063]  P(>=+0.05)=0.19
   superset             +0.053  CI [+0.034, +0.073]  P(>=+0.05)=0.63
   superset_notes       +0.058  CI [+0.036, +0.080]  P(>=+0.05)=0.76
   superset_fallback    +0.051  CI [+0.033, +0.070]  P(>=+0.05)=0.54
   iterative            +0.036  CI [+0.014, +0.058]  P(>=+0.05)=0.10
   retrieval            -0.004  CI [-0.026, +0.017]  P(>=+0.05)=0.00
   select               +0.026  CI [+0.013, +0.039]  P(>=+0.05)=0.00
```

**What this settles.**
- NOT PASSED under the pinned band, by 0.006 on the mean; the interval leg is met (the gain is
  real). Prediction +0.03..+0.09 HIT; falsifier not fired; P(PASS) was 0.6 against a realised 0.34.
- Pattern across the three fresh slices, stated as observation: the claimed arm lands at +0.03 to
  +0.04 each time (fallback +0.032 on v1, notes +0.038 on v2, superset +0.044 on v3) while a
  DIFFERENT diagnostic arm crosses the band each time (notes on v1, superset on v2, superset + notes
  on v3). Chasing the previous slice's best diagnostic has now been tried twice and landed under
  the band both times, decisively above zero both times. The pooled table over v2+v3 (n=800) is a
  diagnostic only; its arms were all computed before any of this was read, but pooling is post hoc.
- The two-day answer is unchanged and now firmer: decomposition-for-retrieval is worth about +0.04
  F1 over single-pass on held-out HotpotQA (three slices, every interval excluding zero); the +0.05
  goal is not met by any pre-registered wiring. Gain on bridge questions only, as before.

Key #9 spent; nothing further touches slice v3. Thread state: OPEN, parked at "mechanism real
(+0.04, three slices), +0.05 band unmet by three pre-registered claims". No further key requested
by me: a fourth slice chasing the third diagnostic would be the pattern I just named. Retro of this
window as s46 after your verdict.
