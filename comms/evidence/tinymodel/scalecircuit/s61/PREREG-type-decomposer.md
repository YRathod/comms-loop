# Pre-registration: TYPE-aware decomposer with the restated-question prompt (conditional key #13; nothing built)

Written 2026-09-14 ~20:45Z by fable, before the DEV2 restate probe has been read and before key #13 exists.

## Condition (from the human's conditional key)
This cycle runs ONLY IF the probe (scale/results/pipeline_dev2_restate.json vs pipeline_dev2_verify.json,
same adapter, same 100 DEV2 docs) shows superset + notes improving under the restated prompt (paired mean
delta > 0) AND the bridge-copy count (two-hop, wrong, answer == hop-1 note) falling. Otherwise the key is
void unused and this file is the record of a probe that did not justify the cycle.

## Why
On v5, 45 of 400 questions were answered with the bridge entity from the notes instead of the target
(s57 taxonomy). The probe tests a regex-derived target type restated at the end of the prompt; the regex
is not generalisable. The generalisable form is for the decomposer itself to emit the target type.

## Mechanism
- hand labels: a `TYPE:` line added to each of the 299 decompositions (question text only; e.g. "record
  label", "person", "date", "place", "number", or NA when the question abstains), train split, no teacher.
- decomposer: Qwen2.5-1.5B-Instruct + LoRA, 1 epoch on the 299 x5 (same recipe as the passing pre-gate
  adapter, plus the TYPE line); output "TYPE: ...", "H1: ...", "H2: ..." or NA.
- reader prompt: notes as today, then at the very end "Target answer type: <TYPE>", the question again, and
  "Answer (must be a <TYPE>, not an intermediate entity from the notes):". Applied to every arm, including
  single-pass (type from the decomposer even when it abstains, if it emits one).
- pre-gate (<= 15 min) on 40 DEV2 questions: parseable >= 36, anchor kept >= 30, TYPE present >= 30.
- DEV2 run with the type-restated prompt; pinned stop: right->wrong > one third of wrong->right on the
  claimed arm ends the cycle with no eval.

## Eval (ONE run, slice v7: n=400, seed 20260920, disjoint from every prior slice, hashed before any model reads it)
- claim, fixed now: type-restated prompt vs plain prompt on the same wiring (superset + notes, same
  decomposer hops), paired per doc; PASS = mean delta >= +0.02 AND the 95 percent bootstrap interval
  excludes zero. Secondary, reported only: the wiring vs single-pass under the +0.05 band, both prompts.
- prediction (raw, no haircut): +0.01 to +0.05 on the wiring; P(PASS) 0.4. Falsifier: <= 0.
- safety case assembled before the result mail; every mail through the refs gate; numbers from frozen files.
