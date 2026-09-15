# Pre-registration: fresh full run of the tagger on generator v3 (R3 round 4)

Written 2026-09-13 ~05:50Z by fable, under the human autopilot window (GOAL-2026-09-13.md, NO CHEATING
rules 1-6), before any number from this run exists. Thread tinymodel/scalecircuit; key KEYS.md #6.

## Why a new registration (GOAL rule 6)
The curriculum loop (LOOP-tagger.md) stopped after round 2 by its own pin 8 (loop measure 13 -> 13).
Its rounds continued a fully-fitted adapter (s8, loss 1e-4) for ONE epoch each; that is the loop's
registered form, not a test of the generator mechanism itself. This run tests generator v3 the way
s8 tested v2: from the base model, two epochs, all hand labels.

## 5-why on the plateau (structure 14-16 of 30 across s5-s8, rounds 1-2)
1. Why does structure stay at 14-16? Half the misses are extra or dropped hops on clause-shaped
   wrappers and anchors chosen by position (why_r1, why_r2).
2. Why did round 2 move structure only +2 with v3 present? 12K v3 pairs entered on top of an adapter
   that already fit 20K v2 pairs to loss 1e-4 for one epoch; the v2 prior dominates.
3. Why did anchor and NA give back a doc each? The v3 lead-ins (30 percent under the anchor route)
   put dates and numbers before the anchor at a rate the real batches do not have (real ~10
   percent), and the continued adapter over-corrected toward "skip the first span".
4. Why not simply run round 3? Pin 8 fired; running past it is the band-moving GOAL rule 6 forbids.
5. Why will a fresh run be different? Default v3 knobs (CLAUSE 0.35, LEADIN 0.15, NA 0.12 with the
   comparison forms) at 20K pairs from the base model give the clause and lead-in mechanisms the
   same footing v2's phrasings had in s8, with 120 labels x5 (docs 40-159) instead of 30.
Root = MECHANISM UNDER-WEIGHTED: v3 phrasings were a 1-epoch minority on a v2-saturated adapter.

## Run (gate.json pinned alongside, keys as tagger_lora records them)
- base Qwen/Qwen2.5-0.5B-Instruct, LoRA r16, bs 4 x accum 4, lr 2e-4, seed 0, 2 epochs
- train data/tagger_train_v3.jsonl (20000, seed 3, default knobs; last 500 = synthetic held-out)
- extra data/tagger_real_40-159.jsonl (120 hand labels, x5); few-shot docs x5 as in every run
- sanity bands 50:1.0,100:0.4,200:0.15; heartbeat every 25 steps; drift alerts on
- eval slice docs 3-39 minus few-shot (n=30), asserted absent from --extra
- out models/tagger_v3full_0.5b
- pre-gate: none separate; the run is ~35 min and its first 200 steps are the pre-gate (bands above)

## Prediction, banded (falsifiable)
- structure 16-19 of 30 (from 16 at round 2; the PASS band 20 is NOT predicted to be reached)
- anchor 23-26; na_ok 28-30; synth held-out >= 0.95
- Falsifier: structure <= 15 -> the generator-v3 mechanism is dead at 0.5B and the plateau is the
  grammar's ceiling; no further tagger runs today.
- If structure >= 17, the end-to-end eval (second and last eval run of the day) uses this adapter.
