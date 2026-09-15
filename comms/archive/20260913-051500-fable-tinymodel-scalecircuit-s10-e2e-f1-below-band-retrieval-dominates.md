---
from: fable
to: [kimi, human]
project: tinymodel
thread: tinymodel/scalecircuit
seq: 10
re-seq: 9
type: result
refs:
  - comms/evidence/tinymodel/scalecircuit/s10/pipeline_exec_e2e.json
  - comms/evidence/tinymodel/scalecircuit/s10/e2e_run.log
  - comms/evidence/tinymodel/scalecircuit/s10/e2e_summary.txt
  - comms/evidence/tinymodel/scalecircuit/s10/pipeline_exec.py
  - comms/evidence/tinymodel/scalecircuit/s10/GOAL-2026-09-13.md
  - comms/evidence/tinymodel/scalecircuit/s8/fullrun_eval.json
---

# tinymodel/scalecircuit s10 — end-to-end F1 on the 30 eval docs: best wiring +0.036 over single-pass, band +0.05 NOT reached; chain wiring falsified, retrieval wiring never loses

Setup (frozen in pipeline_exec.py): tagger = s8 adapter (models/tagger_lora_0.5b) -> LSTM hops
(decomp_filter_lstm.pt) -> one-clause templates per relation -> reader Qwen2.5-3B-Instruct over the
doc's paragraphs (keyword retrieval, top 6, <=3000 tokens), F1 vs HotpotQA gold on docs 3-39 minus
the 10 few-shot docs (n=30). Baseline = the same reader, same retrieval, original question.
Two wirings as in the long-bench campaign: chain (answer hop by hop, substitute) and retrieval
(hop questions only gather paragraphs, one read of the original question).

| wiring | mean F1 | wins vs single-pass | losses | per-doc in json |
|---|---|---|---|---|
| single-pass baseline | 0.370 | - | - | f1_sp |
| chain | 0.118 | 1 (doc 20) | 11 | f1_chain |
| retrieval | 0.405 | 2 (docs 19, 20) | 0 | f1_retrieval |
| oracle union (max per doc) | 0.405 | | | |

Band (GOAL-2026-09-13.md, pinned 04:30Z before any number): best wiring >= single-pass + 0.05 =
0.420. Best = retrieval 0.405 -> **FAIL by 0.015** (one more doc at F1 ~0.5 would have crossed it;
that is the honest size of the gap, not a near-miss claim). The written expectation in the goal
file was that the band is NOT reached today; that stands confirmed.

D2 complementarity: the oracle union equals the retrieval wiring exactly, so chain adds nothing
the retrieval wiring does not already get. Retrieval is a strict improvement (2 up, 0 down):
the decomposed hop questions pull in the bridge paragraph the keyword retriever misses on the
original question (doc 19 +0.67, doc 20 +0.40) and never displace a paragraph that mattered.

Chain wiring, 11 losses, autopsy classes from the traces (rung 0 done, keys stand):
- 5 wrong tag propagates (docs 8, 10, 23, 28, 36): the s8 structure failure lands here; a wrong
  relation makes hop 1 ask the wrong question and the substitution poisons hop 2.
- 4 right tag, hop answer is the wrong shape (docs 13, 15, 22, 33): the one-clause template yields
  an entity where the gold wants an attribute (doc 33 "44" vs "Taoiseach of Ireland") or a list
  where one item was needed.
- 2 reader refuses on the sub-question but answers the original (docs 5, 24).
Root for the chain arm = the tagger's structure error (s8) compounded by template shape; this
is the same root the inner loop is attacking, so no separate route is registered.

Status vs today's pinned goal: NOT PASSED. Loop round 1 is training now (5-why written at
s8/why_r1.md, route TAGGER_DEPTH_WEIGHTS 20,35,30,15, docs 70-99 labels joined); after each round
that improves structure I re-run this exact script and report the delta against the same band.
Stop conditions unchanged (cap 3 rounds; key #6 expiry 2026-09-14T00:00Z).

Prediction, banded before round 1 finishes: structure on the fixed slice moves from 14 to 16-19
(below the 20 band) and retrieval F1 moves by less than 0.02, because the retrieval wiring is
insensitive to relation names and only depth changes what paragraphs get pulled.
