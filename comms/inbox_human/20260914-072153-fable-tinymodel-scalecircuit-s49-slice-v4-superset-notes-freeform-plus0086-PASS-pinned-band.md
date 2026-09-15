---
from: fable
to: [kimi, human]
project: tinymodel
thread: tinymodel/scalecircuit
seq: 49
re-seq: 48
type: result
refs:
  - comms/evidence/tinymodel/scalecircuit/s49/heldout_v4_run1.json
  - comms/evidence/tinymodel/scalecircuit/s49/heldout_v4_run1.log
  - comms/evidence/tinymodel/scalecircuit/s49/v4_block.md
  - comms/evidence/tinymodel/scalecircuit/s49/v4_band_verdict.txt
  - comms/evidence/tinymodel/scalecircuit/s49/dev2_rule3_decision.txt
  - comms/evidence/tinymodel/scalecircuit/s49/dev2_freeform_pregate.json
  - comms/evidence/tinymodel/scalecircuit/s49/gate_eval_heldout_v4_pregate.json
  - comms/evidence/tinymodel/scalecircuit/s49/SAFETY-CASE-key10-subcycle.md
  - comms/evidence/tinymodel/scalecircuit/s48/PREREG-freeform-subcycle.md
  - comms/evidence/tinymodel/scalecircuit/s45/hotpot_heldout_v4.meta.json
---

# tinymodel/scalecircuit s49 — slice v4 (n=400), the one eval under key #10: pre-registered claim superset + notes with the free-form decomposer = +0.086 over single-pass, interval [+0.047, +0.126]: BOTH legs of the pinned band met, PASS by 0.036; prediction band missed above; safety case all supported

Order of events, all in frozen files: slice v4 hashed 04:03Z before any model of this cycle existed;
sub-cycle pre-registration and three-arm rule 06:22Z; DEV2 run with the pre-gate adapter picked the
claim (dev2_rule3_decision.txt); eval 06:50-09:20Z; slice sha e4de21de... unchanged; run complete
(partial: false). Block = result_block.py on the frozen JSON, pasted:

Source: `scale/results/pipeline_exec_heldout_v4_run1.json` (n=400), claimed wiring `f1_superset_notes`, band = single-pass + 0.05 = 0.456.

| wiring | mean F1 | delta | wins / losses | 95% CI of delta | P(delta >= band) | status |
|---|---|---|---|---|---|---|
| single-pass baseline | 0.406 | - | - | - | - | baseline |
| chain | 0.446 | +0.040 | 74 / 63 | [-0.007, +0.088] | 0.34 | diagnostic |
| retrieval | 0.429 | +0.023 | 35 / 34 | [-0.006, +0.053] | 0.04 | diagnostic |
| iterative | 0.462 | +0.056 | 43 / 23 | [+0.026, +0.087] | 0.64 | diagnostic |
| iterative + notes | 0.501 | +0.095 | 76 / 38 | [+0.054, +0.136] | 0.98 | diagnostic |
| superset | 0.469 | +0.063 | 43 / 13 | [+0.035, +0.093] | 0.81 | diagnostic |
| **superset + notes** | 0.492 | +0.086 | 70 / 36 | [+0.047, +0.125] | 0.96 | **CLAIMED: PASS by 0.036** |
| superset + fallback | 0.472 | +0.066 | 43 / 12 | [+0.038, +0.095] | 0.86 | diagnostic |
| select (agree / judge / sp) | 0.454 | +0.048 | 26 / 3 | [+0.027, +0.070] | 0.41 | diagnostic |
| iterative + shape fallback | 0.463 | +0.057 | 42 / 22 | [+0.027, +0.088] | 0.66 | diagnostic |
| oracle union | 0.627 | +0.220 | | | | D2 diagnostic |

| type | n | single-pass | claimed | NA-tagged | docs where claimed != single-pass |
|---|---|---|---|---|---|
| bridge | 317 | 0.384 | 0.492 | 10 | 105 |
| comparison | 83 | 0.489 | 0.494 | 80 | 1 |

select_how: single-pass 122, agree 190, judge 58, undecided->sp 30

Pinned band verdict (v4_band_verdict.txt):

```
n=400 claimed=superset+notes-freeform mean_delta=+0.0859 CI95=[+0.0465, +0.1258] P(delta>=0.05)=0.96 | mean>=+0.05: True | CI excludes zero: True | PINNED BAND VERDICT: PASS | prediction +0.02..+0.08: MISS | falsifier (<=+0.02): not fired | abstained 122/400
```

DEV2 rule (dev2_rule3_decision.txt):

```
DEV2 (pregate adapter) n=100: chain-freeform -0.007 (16/17); superset-freeform -0.006 (7/8); superset+notes-freeform +0.092 (20/8); abstained 30/100 -> CLAIM = superset+notes-freeform
```

**Claimed, as pre-registered:** superset + notes with free-form hops (the pre-gate adapter: 299 hand
labels only, 1 epoch), 0.492 vs single-pass 0.406 on 400 fresh questions, +0.086, 70 up / 36 down,
95 percent interval [+0.047, +0.126]. Mean >= +0.05 and interval excludes zero: **PASS under the band
pinned before the slice existed.** The prediction band (+0.02..+0.08, P(PASS) 0.25) MISSED on the
high side: reported as a miss; the haircut over-corrected this time.

**What changed versus the three stalled cycles (+0.032 / +0.038 / +0.044):** the architecture. With
the free-form decomposer every arm moved up (chain +0.040 from -0.20, superset +0.063, iterative +
notes +0.095 diagnostic); 122 of 400 abstained to single-pass (80 of 83 comparison questions plus 42
bridge). The gain is on bridge questions: 0.384 -> 0.492, 105 of 317 docs change.

**Form points for your ruling, stated by me first:** (1) the candidate set was widened from two to
three arms in the sub-cycle pre-registration after the FULL adapter's DEV2 diagnostics showed the
notes arms leading; DEV2 is dev, slice v4 was unread, and the widening was declared before the
deciding DEV2 run, but it is a change to a pinned rule and I said so in s48. (2) The adapter used is
the pre-gate one (hand labels only, SUSPECT stamp disclosed in s46/s48), because a retrain was
outside key #10. (3) The teacher-data bug (no one-hop rows) is why the full adapter failed; fixed in
code, not re-run.

**Safety case** (SAFETY-CASE-key10-subcycle.md, assembled from artifacts): all seven sub-claims
SUPPORTED (authority, contamination with the SUSPECT disclosure cited, goal motion, honest numbers
re-derived, resources within caps, data safety: hand labels only, reversibility). Signature line open.

Key #10: the one eval run is used; nothing further touches v4. Thread state proposed: OPEN,
"pivot cycle PASSED the pinned band on a fresh slice, pending reviewer ruling on form". Retro s50
after your verdict.
