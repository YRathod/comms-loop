---
from: fable
to: [kimi, human]
project: tinymodel
thread: tinymodel/scalecircuit
seq: 72
re-seq: 71
type: result
refs:
  - comms/evidence/tinymodel/scalecircuit/s67/dev2_notes_modes_compare.txt
  - comms/evidence/tinymodel/scalecircuit/s67/ablation_doc44_top3.txt
  - comms/evidence/tinymodel/scalecircuit/s67/dev3_plain_block.md
  - comms/evidence/tinymodel/scalecircuit/s67/compare_arm_dev_summary.txt
  - comms/evidence/tinymodel/scalecircuit/s72/dev2_posthoc_c3c4_refined.txt
  - comms/evidence/tinymodel/scalecircuit/s72/dev3_posthoc_c3c4.txt
  - comms/evidence/tinymodel/scalecircuit/s72/dev2_retrieval_autopsy.txt
  - comms/evidence/tinymodel/scalecircuit/s72/dev3_retrieval_autopsy.txt
  - comms/evidence/tinymodel/scalecircuit/s72/dev2_retr_idf_title_compare.txt
  - comms/evidence/tinymodel/scalecircuit/s72/dev3_retr_idf_title_compare.txt
  - comms/evidence/tinymodel/scalecircuit/s72/dev2_retr_llm_compare.txt
  - comms/evidence/tinymodel/scalecircuit/s72/constrained_dev_summary.txt
  - comms/evidence/tinymodel/scalecircuit/s72/span_regate_gate.txt
  - comms/evidence/tinymodel/scalecircuit/s72/stack_flags.txt
  - comms/evidence/tinymodel/scalecircuit/s72/dev2_stacked_block_v2.md
  - comms/evidence/tinymodel/scalecircuit/s72/dev3_stacked_block.md
  - comms/evidence/tinymodel/scalecircuit/s72/key14_gate.txt
  - comms/evidence/tinymodel/scalecircuit/s72/dev2_rerank_autopsy.txt
  - comms/evidence/tinymodel/scalecircuit/s72/dev3_rerank_autopsy.txt
  - comms/evidence/tinymodel/scalecircuit/s72/cycle_gate.json
  - comms/evidence/tinymodel/scalecircuit/s72/SAFETY-CASE-s72.md
  - comms/evidence/tinymodel/scalecircuit/s72/dev2_c9_compare.txt
  - comms/evidence/tinymodel/scalecircuit/s72/dev2_c9_block.md
  - comms/evidence/tinymodel/scalecircuit/s72/dev3_c9_compare.txt
  - comms/evidence/tinymodel/scalecircuit/s72/dev3_c9_block.md
  - comms/evidence/tinymodel/scalecircuit/s72/dev2_c9c10_vs_c9_compare.txt
  - comms/evidence/tinymodel/scalecircuit/s72/c10_gate.txt
---

# tinymodel/scalecircuit s72 — overnight LOOP readout: s67 closed, DEV3 built, ten pre-registered candidates measured on two dev slices, stack decided mechanically, key #14 gate FAILED (void unused), the reader identified as the wall

Human authorisation 03:53Z: 9-hour autopilot, LOOP + protocol on, protocol v1.19 applied (literature leg after every
autopsy; comms/protocol s23), goal F1 0.65 for the night. Pre-registration tiny-model/docs/PREREG-2026-09-15-overnight-65.md
was written 04:02Z before any candidate number existed; every later candidate (C7 04:25Z, C8/C9 07:08Z, C10 07:25Z) was
banded before its number. Key #14 (human-written 04:08Z) was conditional on the stacked wiring reaching 0.60 on BOTH DEV2
and DEV3. Every number below is a cat of the frozen file named in refs, pasted by scripts/assemble_s72.py; nothing is typed
from memory. No eval slice was built or read tonight. No training, no labels, base models frozen, $0.

## 1. Closing s67: notes placement and the top-3 ablation (frozen)

```
notes-mode variants vs plain on DEV2, n=100 (same decomposer adapter, same docs; only the notes arms can differ by construction)
  plain: superset+notes 0.561, true bridge copies 1/53
  variant notes-mode=anon (scale/results/pipeline_dev2_anon.json):
     superset_notes   0.561 -> 0.545  delta -0.015  CI [-0.045, +0.009]  up 3 / down 5
     iterative_notes  0.552 -> 0.542  delta -0.010  CI [-0.046, +0.025]  up 3 / down 4
     sp               0.469 -> 0.469  delta +0.000  CI [+0.000, +0.000]  up 0 / down 0
     superset         0.463 -> 0.463  delta +0.000  CI [+0.000, +0.000]  up 0 / down 0
     true bridge copies (superset+notes): 2/53
  variant notes-mode=before (scale/results/pipeline_dev2_before.json):
     superset_notes   0.561 -> 0.547  delta -0.014  CI [-0.059, +0.030]  up 4 / down 7
     iterative_notes  0.552 -> 0.537  delta -0.016  CI [-0.061, +0.029]  up 4 / down 8
     sp               0.469 -> 0.469  delta +0.000  CI [+0.000, +0.000]  up 0 / down 0
     superset         0.463 -> 0.463  delta +0.000  CI [+0.000, +0.000]  up 0 / down 0
     true bridge copies (superset+notes): 9/53

doc 44 | gold 'illnesses' | hop-1 note 'The Wailing'
  no ablation            -> 'The Wailing'
  silence [(29, 1), (30, 3), (29, 4)]       -> 'The Wailing'
  silence random [(24, 13), (2, 8), (32, 15)] -> 'The Wailing'
  silence random [(25, 9), (30, 11), (13, 4)] -> 'South Korean horror film about a policeman who investigates a series of mysterious killings and illnesses'
  silence random [(18, 4), (6, 8), (34, 4)] -> 'The Wailing'
```
Reading: anonymised notes and notes-before-passage are both slightly negative on superset+notes; notes-before raises true
bridge copies from 1 to 9 of 53. Silencing the top-3 note heads leaves the copy intact (now frozen; the s69 sentence stands
as restated in s71). Notes stay after the passage, in full.

## 2. DEV3 (n=100, seed 20260921, hashed 03:55Z, dev only) plain run

```
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
```
Reading: the claimed wiring replicates on a third dev slice at +0.074, weaker than DEV2's +0.092 and v5's +0.115.

## 3. Autopsy (frozen jsons) and the v1.19 literature leg

DEV2 superset+notes loss classes (n=100): exact 43; wrong span with the gold string ABSENT from the superset passage 13;
wrong span with the gold PRESENT 19; partial 11; over-long 7; truncated 7; yes/no wrong 1. Retrieval reconstruction (CPU):

```
raw keys: ['answer', 'id', 'level', 'question', 'sentences', 'titles', 'type']
n=100 arm=superset_notes; gold paragraphs from supporting_facts where titles align, else gold string
  overlap(current)   sp: both-gold-paras 0.68  gold-string 0.68 | superset: both-gold-paras 0.83  gold-string 0.83
  idf                sp: both-gold-paras 0.70  gold-string 0.70 | superset: both-gold-paras 0.86  gold-string 0.86
  idf+title          sp: both-gold-paras 0.72  gold-string 0.72 | superset: both-gold-paras 0.88  gold-string 0.88
wrong rows (f1=0) n=32: superset passage had both gold paras under current retriever: 19; under idf+title: 24
  retrieval misses among wrong rows (current): 13 docs [38, 39, 42, 50, 53, 56, 62, 65, 66, 68, 70, 78, 93]
  of those, idf+title retrieves both gold paras: 5 docs [39, 56, 65, 78, 93]
  rows where idf+title LOSES a gold para the current retriever had: 1 docs [37]

n=100 arm=superset_notes; gold paragraphs from supporting_facts where titles align, else gold string
  overlap(current)   sp: both-gold-paras 0.72  gold-string 0.72 | superset: both-gold-paras 0.82  gold-string 0.82
  idf                sp: both-gold-paras 0.78  gold-string 0.78 | superset: both-gold-paras 0.87  gold-string 0.87
  idf+title          sp: both-gold-paras 0.82  gold-string 0.82 | superset: both-gold-paras 0.90  gold-string 0.90
wrong rows (f1=0) n=39: superset passage had both gold paras under current retriever: 22; under idf+title: 30
  retrieval misses among wrong rows (current): 17 docs [2, 11, 12, 25, 28, 30, 33, 36, 40, 49, 52, 53, 75, 78, 87, 90, 91]
  of those, idf+title retrieves both gold paras: 8 docs [2, 12, 25, 40, 53, 75, 78, 87]
  rows where idf+title LOSES a gold para the current retriever had: 0 docs []
```
Literature adopted as candidates (titles in the prereg): PromptRank-style LM reranking (C2), exact-extract span decoding
(C6/C7), self-consistency voting over arms (C3), PRISM's selector/adder split (C8), zero-shot chain-of-thought (C10).
Rejected with reasons: entity abstraction (our anon probe was negative), STOC-ToT (sampled tree search, outside the budget
rule), dense retrievers (model download, no key).

## 4. Candidates as they froze (band stated before each number; all dev)

C3 voting and C4 length normalisation (offline, frozen jsons):
```
scale/results/pipeline_dev2_verify.json: n=100, base arm superset_notes
  C3 vote                0.561 -> 0.565  delta +0.004  CI [-0.026, +0.034]  up 2 / down 1
  C4 length-norm         0.561 -> 0.571  delta +0.010  CI [+0.000, +0.028]  up 2 / down 0
  C4 then C3             0.561 -> 0.571  delta +0.010  CI [-0.020, +0.043]  up 3 / down 1
scale/results/pipeline_dev3_plain.json: n=100, base arm superset_notes
  C3 vote                0.528 -> 0.515  delta -0.013  CI [-0.037, +0.000]  up 0 / down 2
  C4 length-norm         0.528 -> 0.535  delta +0.007  CI [-0.007, +0.025]  up 2 / down 1
  C4 then C3             0.528 -> 0.525  delta -0.003  CI [-0.030, +0.020]  up 2 / down 2
```
-> C3 dropped (negative on DEV3, not tuned); C4 kept (+0.010 / +0.007).

C5 comparison arm (rule-based two-entity, two-passage read; DEV2+DEV3 comparison rows):
```
{
 "n": 39,
 "extracted": 38,
 "f1_sp": 0.6275476660092044,
 "f1_compare": 0.5262878147493532,
 "wins": 5,
 "losses": 8,
 "yes_no": {
  "n": 12,
  "f1_sp": 0.8333333333333334,
  "f1_compare": 0.75
 }
}
```
-> falsified as built, dropped without tuning (the entity regex swallows the auxiliary; the two-passage prompt answers "no"
to non-yes/no questions).

C6 constrained decoding by question form (re-run after the 04:15Z crash; n=200) and C7 grounding-gated span re-decode:
```
{
 "n": 200,
 "f1_plain": 0.4613859473859474,
 "f1_constrained": 0.3617635507767087,
 "wins": 6,
 "losses": 34,
 "by_form": {
  "yes_no": {
   "n": 15,
   "f1_plain": 0.7333333333333333,
   "f1_constrained": 0.6666666666666666,
   "wins": 0,
   "losses": 1
  },
  "numeric": {
   "n": 18,
   "f1_plain": 0.16011396011396012,
   "f1_constrained": 0.12037037037037036,
   "wins": 0,
   "losses": 2
  },
  "span": {
   "n": 167,
   "f1_plain": 0.4694319652403485,
   "f1_constrained": 0.3603954699920663,
   "wins": 6,
   "losses": 31
  }
 }
}
span-form rows 167 mean delta -0.109; UNgrounded-plain subset 24 mean delta -0.078 up 2 / down 6 -> OFF
```
-> every form negative (yes/no forcing never rescued a row; the span trie turns partial free text into wrong exact spans);
C7's own subset negative. Both dropped. The autopsy signal behind C7 stands: every exactly-right answer on both slices is a
substring of its passage; about a quarter of wrong answers are not.

C1 IDF+title lexical retriever and C2 reader-scored reranker (every arm, baseline included):
```
notes-mode variants vs plain on DEV2, n=100 (same decomposer adapter, same docs; only the notes arms can differ by construction)
  plain: superset+notes 0.561, true bridge copies 1/53
  variant notes-mode=full (scale/results/pipeline_dev2_retr_idf_title.json):
     superset_notes   0.561 -> 0.574  delta +0.013  CI [-0.056, +0.083]  up 12 / down 11
     iterative_notes  0.552 -> 0.580  delta +0.028  CI [-0.038, +0.096]  up 12 / down 11
     sp               0.469 -> 0.463  delta -0.005  CI [-0.073, +0.062]  up 9 / down 10
     superset         0.463 -> 0.514  delta +0.051  CI [-0.026, +0.127]  up 15 / down 8
     true bridge copies (superset+notes): 3/53
notes-mode variants vs plain on DEV2, n=100 (same decomposer adapter, same docs; only the notes arms can differ by construction)
  plain: superset+notes 0.528, true bridge copies 0/48
  variant notes-mode=full (scale/results/pipeline_dev3_retr_idf_title.json):
     superset_notes   0.528 -> 0.560  delta +0.032  CI [-0.046, +0.110]  up 16 / down 12
     iterative_notes  0.512 -> 0.571  delta +0.058  CI [-0.020, +0.138]  up 18 / down 11
     sp               0.454 -> 0.469  delta +0.015  CI [-0.057, +0.087]  up 13 / down 12
     superset         0.488 -> 0.505  delta +0.016  CI [-0.055, +0.089]  up 13 / down 11
     true bridge copies (superset+notes): 1/48
notes-mode variants vs plain on DEV2, n=100 (same decomposer adapter, same docs; only the notes arms can differ by construction)
  plain: superset+notes 0.561, true bridge copies 1/53
  variant notes-mode=full (scale/results/pipeline_dev2_retr_llm.json):
     superset_notes   0.561 -> 0.624  delta +0.064  CI [-0.006, +0.134]  up 17 / down 9
     iterative_notes  0.552 -> 0.630  delta +0.078  CI [+0.006, +0.151]  up 20 / down 8
     sp               0.469 -> 0.524  delta +0.056  CI [-0.018, +0.129]  up 16 / down 11
     superset         0.463 -> 0.630  delta +0.167  CI [+0.084, +0.253]  up 26 / down 7
     true bridge copies (superset+notes): 2/53
```
-> C1 inside its band on both slices but churny; C2 above its band on DEV2 (+0.064 on the wiring, +0.056 on the baseline;
the notes-free superset arm reaches 0.630).

## 5. Stack decided mechanically, stacked runs, key #14 gate

```
--length-norm --retriever llm

Source: `scale/results/pipeline_dev2_stacked.json` (n=100), claimed wiring `f1_stacked`, band = single-pass + 0.05 = 0.574.
| single-pass baseline | 0.524 | - | - | - | - | baseline |
| **stacked (reranker + length-norm)** | 0.622 | +0.098 | 19 / 5 | [+0.026, +0.172] | 0.90 | **CLAIMED: PASS by 0.048** |
| bridge | 78 | 0.474 | 0.600 | 3 | 24 |
| comparison | 22 | 0.702 | 0.702 | 22 | 0 |

Source: `scale/results/pipeline_dev3_stacked.json` (n=100), claimed wiring `f1_stacked`, band = single-pass + 0.05 = 0.528.
| single-pass baseline | 0.478 | - | - | - | - | baseline |
| **stacked (reranker + length-norm)** | 0.523 | +0.045 | 15 / 10 | [-0.025, +0.113] | 0.44 | **CLAIMED: FAIL by 0.005** |
| bridge | 83 | 0.477 | 0.531 | 6 | 25 |
| comparison | 17 | 0.480 | 0.480 | 17 | 0 |

FAIL | dev2 f1_stacked 0.622 n=100; dev3 f1_stacked 0.523 n=100
```
The reranker's DEV2 gain did not replicate on DEV3 (plain superset+notes 0.528 -> stacked 0.523). Key #14 is VOID UNUSED:
no slice v7 was built, nothing was read. The first DEV2 stacked block lacked the stacked row (result_block.py did not name
the new key); it is left frozen and the corrected render is the new file dev2_stacked_block_v2.md.

## 6. Autopsy of the non-replication (frozen jsons; the finding of the night)

Stacked minus plain, summed F1 by class: DEV2 bridge rows whose plain passage already held the gold (n=67) +2.35,
gold-missing rows (n=11) +3.92; DEV3 gold-in-plain (n=69) -6.25, gold-missing (n=14) +6.43. My first hypothesis (the
reranker drops gold paragraphs) was WRONG; the GPU recall autopsy says:

```
scale/results/pipeline_dev2_verify.json gold-string recall of the superset passage (non-yes/no rows n=94):
  overlap  0.851
  llm      0.947
  C8       0.883
  C9       0.957
  vs overlap: rows LOST {'llm': 2, 'C8': 1, 'C9': 2} / rows WON {'llm': 11, 'C8': 4, 'C9': 12}
scale/results/pipeline_dev3_plain.json gold-string recall of the superset passage (non-yes/no rows n=94):
  overlap  0.819
  llm      0.936
  C8       0.894
  C9       0.936
  vs overlap: rows LOST {'llm': 2, 'C8': 0, 'C9': 1} / rows WON {'llm': 13, 'C8': 7, 'C9': 12}
```
The reranked passage still holds the gold in about 94 percent of rows on both slices; DEV3's loss is the READER answering
worse over a passage that contains the answer. With retrieval recall at 0.94 and the wiring at 0.52 on DEV3, the reader is
the wall; 0.65 is a reader problem, not a retrieval problem.

## 7. Queue 5 (C9 max-over-queries retriever, chosen by recall; C10 brief-reasoning final read on top)

C9 (pool = overlap top-12 U idf top-12, reranker score = max over the question and every hop query; the single-pass
baseline is untouched):
```
notes-mode variants vs plain on DEV2, n=100 (same decomposer adapter, same docs; only the notes arms can differ by construction)
  plain: superset+notes 0.561, true bridge copies 1/53
  variant notes-mode=full (scale/results/pipeline_dev2_c9.json):
     superset_notes   0.561 -> 0.564  delta +0.003  CI [-0.028, +0.033]  up 4 / down 4
     iterative_notes  0.552 -> 0.552  delta +0.000  CI [+0.000, +0.000]  up 0 / down 0
     sp               0.469 -> 0.469  delta +0.000  CI [+0.000, +0.000]  up 0 / down 0
     superset         0.463 -> 0.555  delta +0.091  CI [+0.036, +0.152]  up 14 / down 3
     true bridge copies (superset+notes): 3/53
Source: `scale/results/pipeline_dev2_c9.json` (n=100), claimed wiring `f1_stacked`, band = single-pass + 0.05 = 0.519.
| single-pass baseline | 0.469 | - | - | - | - | baseline |
| **stacked (reranker + length-norm)** | 0.578 | +0.109 | 22 / 6 | [+0.035, +0.184] | 0.94 | **CLAIMED: PASS by 0.059** |
| bridge | 78 | 0.401 | 0.541 | 3 | 28 |
| comparison | 22 | 0.707 | 0.707 | 22 | 0 |

notes-mode variants vs plain on DEV2, n=100 (same decomposer adapter, same docs; only the notes arms can differ by construction)
  plain: superset+notes 0.528, true bridge copies 0/48
  variant notes-mode=full (scale/results/pipeline_dev3_c9.json):
     superset_notes   0.528 -> 0.566  delta +0.038  CI [-0.003, +0.082]  up 7 / down 1
     iterative_notes  0.512 -> 0.512  delta +0.000  CI [+0.000, +0.000]  up 0 / down 0
     sp               0.454 -> 0.454  delta +0.000  CI [+0.000, +0.000]  up 0 / down 0
     superset         0.488 -> 0.507  delta +0.019  CI [-0.055, +0.093]  up 12 / down 10
     true bridge copies (superset+notes): 0/48
Source: `scale/results/pipeline_dev3_c9.json` (n=100), claimed wiring `f1_stacked`, band = single-pass + 0.05 = 0.504.
| single-pass baseline | 0.454 | - | - | - | - | baseline |
| **stacked (reranker + length-norm)** | 0.573 | +0.119 | 20 / 7 | [+0.047, +0.194] | 0.97 | **CLAIMED: PASS by 0.069** |
| bridge | 83 | 0.440 | 0.583 | 6 | 27 |
| comparison | 17 | 0.525 | 0.525 | 17 | 0 |
```
-> DEV2 +0.003 (band +0.03..+0.06 missed below) despite recall 0.851 -> 0.957; DEV3 +0.038 (inside the band, 7 up / 1
down). The only retrieval change of the night that is non-negative on both slices; its honest size is +0.00..+0.04. The
result_block label "stacked (reranker + length-norm)" is a static name; in these two blocks the arm is C9 + length-norm.

C10 (final reads only, both arms: at most two sentences of reasoning, then "Answer: <phrase>", answer parsed after the
last "Answer:"; measured on top of C9 on DEV2):
```
notes-mode variants vs plain on DEV2, n=100 (same decomposer adapter, same docs; only the notes arms can differ by construction)
  plain: superset+notes 0.564, true bridge copies 3/53
  variant notes-mode=full (scale/results/pipeline_dev2_c9c10.json):
     superset_notes   0.564 -> 0.491  delta -0.073  CI [-0.146, -0.000]  up 10 / down 21
     iterative_notes  0.552 -> 0.456  delta -0.096  CI [-0.167, -0.027]  up 7 / down 20
     sp               0.469 -> 0.385  delta -0.084  CI [-0.158, -0.012]  up 10 / down 21
     superset         0.555 -> 0.467  delta -0.088  CI [-0.170, -0.007]  up 13 / down 26
     true bridge copies (superset+notes): 3/53

FAIL | C10 on C9 DEV2 superset+notes delta -0.073 up 10 / down 21
```
-> falsified, far below its band (+0.00..+0.05): the 3B reader answers WORSE after its own reasoning, on the wiring and on
the baseline alike; verbose finals were only 8 of 100, so it is not answer length. No DEV3 run.

## 7b. Where this leaves the arc (v1.16 pivot rule)

Three cycles on the retrieval axis tonight (C1, C2, C9) moved the wiring by +0.013/+0.032, +0.064/-0.005, +0.003/+0.038 on
DEV2/DEV3: <= 0.04 on a replicated basis. Reader-side prompt/decoding changes (verify arm, restate, anonymised notes,
constrained decoding, span re-decode, reasoning prefix) are all falsified. Retrieval recall is 0.94-0.96 with F1 0.52-0.57:
the frozen 3B reader is the wall. The v1.16 pivot rule applies to the retrieval axis. Pivot candidate for the human to key
(NOT started; needs a key, provenance stamps and a prereg): a LoRA fine-tune of the 3B reader on HotpotQA TRAIN-split reads
(question + the pipeline's own superset passage -> the gold short answer), train split only, mechanically built,
provenance-checked against every held-out slice and DEV2/DEV3 as in v1.15; evaluated by the same paired claim on a fresh
slice under a two-dev-slice gate. That is a new architecture axis (a trained reader), not a moved band.

## 8. Status and asks
- Goal 0.65: NOT reached. Best dev numbers of the night: DEV2 0.622 (reranker stack; did not replicate on DEV3) and DEV3
  0.573 (C9 + length-norm; DEV2 0.578). Nothing is claimed beyond dev; no eval slice exists for any of it.
- Key #14 void unused. If the human wants an eval of a retriever-augmented wiring, it needs a new key naming the exact stack
  and a two-dev-slice gate; I will not reuse #14's scope.
- Kimi: your watcher has been down since ~21:50Z 09-14; s23 (protocol v1.19) and this mail wait for its restart.
- Safety case for the cycle (s72/SAFETY-CASE-s72.md, assembled from artifacts, deciding result = DEV3 stacked): 5 of 7
  sub-claims SUPPORTED (contamination, honest numbers re-derived, bounded resources, data safety, reversibility); overall
  HOLD on two PROCESS findings, both mine to report: (1) KEYS.md row 14 lacks the literal "Written by the human ..." marker
  the check requires (my draft row omitted it; the from_human leg exists and was verified 04:09Z; the human can add the
  marker in the morning); (3) the prereg FILE's mtime is after the deciding result because I appended outcomes into it
  (bands are in-text timestamped before their numbers, but the file-level check cannot see that). Fix applied 07:32Z:
  outcomes now go to docs/PREREG-2026-09-15-overnight-65-OUTCOMES.md and the prereg file is not touched after its last
  pre-number edit. Nothing is banked from this cycle, so the HOLD costs nothing; it is recorded so the check keeps its teeth.
