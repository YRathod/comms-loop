# The tagger inner loop (pre-registered 2026-09-13)

Instantiates the self-improving loop of trainkey/docs/LOOP.md section 2 for the 0.5B LoRA tagger
(thread tinymodel/scalecircuit). It is the eval-driven curriculum loop, Skill-it / MATES family,
not a self-training loop.

## Pins

1. **Labels are human-written.** Every real question that enters training carries a tag written
   by a person from scratch. The model's own outputs never enter training data, not even
   correctness-filtered, not even as a draft to correct. (LOOP.md pin; collapse at this scale.)
2. **The eval slice is fixed and never trained on.** HotpotQA docs 3-39 minus the ten few-shot
   docs, 30 questions, the same key used since s1. `tagger_lora.py` asserts no eval question is in
   any training file.
3. **Rounds consume train-side batches only**: docs 40-69 (used by s6), then 70-99, 100-129,
   130-159, labelled 30 at a time, in order.
4. **A round fires only when the newest batch has at least 10 failures** at the structure, anchor
   or filter level. Fewer means the class is not worth a training run; the batch still joins the
   accumulated labels.
5. **R1 autopsy, then R2 pause.** Each round writes `autopsy_r<N>.json` (every failure on the new batch, per doc, with its class). The loop then stops until `why_r<N>.md` exists: rung 0 (is the key right for each failing doc), the 5-why on the largest fixable class with doc ids, the named missing mechanism, and the route. Written by a person; `--auto` skips the pause and is off by default.
6. **Route by dominant failure class** on the new batch, into the synthetic generator's knobs:
   hops_dropped -> deeper chains; hops_extra -> fewer OOV-to-attribute cases; anchor -> more
   descriptor anchors; filter -> more filter phrasings; na_wrong -> more NA cases.
   Amendment 2026-09-13 (round 2, pre-registered in scalecircuit s11): generator v3 adds two knobs,
   hops_dropped -> also TAGGER_CLAUSE_FRAC (clause-shaped relation wrappers), anchor -> also
   TAGGER_LEADIN_FRAC (date/number lead-ins before the anchor); make_na gained comparison forms.
7. **Train on accumulated real labels** (all batches so far, 5x) plus the reweighted synthetic set
   plus a 10 percent plain-synthetic replay, one epoch, continued from the previous adapter.
8. **Stop**: hard cap 3 rounds; or the eval slice moves by less than 1 point for 2 rounds; or the
   eval slice drops by more than 2 points after a round, in which case the previous adapter is
   kept and the loop halts. Never "until the eval passes".
9. **Every round is a ledger row** with the round's loop_log.json entry frozen as evidence; the
   loop runs under key #6 (or its renewal) and stops at key expiry.

## What counts as success

The s3 full-run bands on the eval slice, unchanged: structure >= 20/30, anchor >= 24/30,
synthetic held-out >= 0.95. If three rounds do not reach them, the negative result is banked and
the next lever is the descriptor-anchor class, which capitalisation-based anchoring cannot reach.

## Command

```
<local>/model-training/.venv/Scripts/python.exe scripts/tagger_loop.py --start models/tagger_lora_0.5b \
    --batches data/tagger_real_70-99.jsonl data/tagger_real_100-129.jsonl data/tagger_real_130-159.jsonl \
    --out models/tagger_loop
```
