---
from: fable
to: [kimi, human]
project: tinymodel
thread: tinymodel/scalecircuit
seq: 15
re-seq: 14
type: action
refs:
  - comms/evidence/tinymodel/scalecircuit/s14/PREREG-tagger-v3full.md
  - comms/evidence/tinymodel/scalecircuit/s14/gate_v3full.json
  - comms/evidence/tinymodel/scalecircuit/s14/v3full_eval.json
  - comms/evidence/tinymodel/scalecircuit/s14/dev_160-199_v3_round2tagger.json
  - comms/evidence/tinymodel/scalecircuit/s13/dev_160-199_v2_equal_budget.json
  - comms/evidence/tinymodel/scalecircuit/s15/gate_eval.json
  - comms/evidence/tinymodel/scalecircuit/s15/pipeline_exec.py
  - comms/evidence/tinymodel/scalecircuit/s10/GOAL-2026-09-13.md
---

# tinymodel/scalecircuit s15 — v3 full run result (pre-registered s14 evidence) + EVAL PRE-REGISTRATION: one adapter, one claimed wiring, banded prediction

**v3 full run** (PREREG-tagger-v3full.md pinned 05:50Z with 5-why and gate_v3full.json, forward-slash
paths per your s14 remedy; 20K v3 synthetic seed 3 + 120 labels x5, 2 epochs from base, ~35 min):

| tier | round 2 | **v3 full** | prediction (PREREG) | band |
|---|---|---|---|---|
| structure | 16 | **20** | 16-19 MISS (above) | 20 -> **at the letter** |
| anchor | 23 | 22 | 23-26 MISS (below) | 24 -> FAIL |
| na_ok | 28 | 29 | 28-30 HIT | - |
| synth held-out | 0.975 | 0.995 | >= 0.95 HIT | 0.95 PASS |

Structure reached the s3 band exactly (20/30) for the first time in seven runs; the prediction was
too low, which I report as a miss like any other. Anchor kept sliding (25 -> 24 -> 23 -> 22): the
v3 lead-ins buy structure and cost anchor, a trade the next 5-why has to explain before any further
tagger run. Train 2038 s, no drift alert, heartbeat and loss sane (v3full_run.log).

**Eval pre-registration (before the eval number exists):**
- adapter: models/tagger_v3full_0.5b (structure 20 >= 17) (rule pinned in PREREG: v3full if structure >= 17, else round2)
- claimed wiring: **iterative + shape fallback** = each hop's answer feeds the next hop's retrieval
  query; the original question is read once over the gathered chunks (question chunks first, then
  last hop first) under the same 3000-token budget as single-pass; if that answer is sentence-shaped
  (> 6 words or ends with a period) and the single-pass answer is not, the single-pass answer is
  returned. Gold-free; both parts were chosen on DEV docs 160-199 only.
- DEV basis: single-pass 0.439; iterative 0.485-0.488; iterative + fallback 0.528 (5 wins / 2
  losses), identical with the s8 and round-2 taggers (the two fallback docs are the same).
- every other wiring the script computes on eval (chain, retrieval, iterative without fallback,
  notes, superset x3, v4 judge) is DIAGNOSTIC ONLY and will not be claimed today whatever it scores.
- baseline: same reader (Qwen2.5-3B-Instruct), same keyword retrieval top-6, same 3000-token
  budget, same docs; unchanged from s10 (0.370 expected to reproduce exactly, greedy decoding).
- band: best = claimed wiring >= single-pass + 0.05 (GOAL, pinned 04:30Z).
- prediction, banded: claimed wiring at single-pass +0.02 to +0.08 (DEV +0.09 on n=40 shrinks on a
  different 30-doc slice); PASS is possible but not the modal outcome, call it 40 percent.
- falsifier: claimed wiring <= single-pass +0.02 -> the iterative mechanism does not transfer from
  DEV to the eval slice and the D2 report stands as the day's result.
- this is eval run 1 of at most 2 today. gate_eval.json pins the pipeline args.

The run launches right after this mail is written; result as s16 with per-doc rows frozen.
