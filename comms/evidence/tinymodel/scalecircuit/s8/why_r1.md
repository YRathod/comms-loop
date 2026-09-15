# 5-why for round 1 (fable, 2026-09-13)

Autopsy: models/tagger_loop/autopsy_r1.json. Batch docs 70-99, adapter models/tagger_lora_0.5b.
Classes: hops_dropped 5, anchor 3, relation 3, unparseable 1, na_wrong 1, filter 1 (14 of 30).

## Rung 0: is the key right for each failing doc?
- doc 84 "Why did the CEO of the football team based in Denver step down": key
  `attribute of leader of leader of Denver` is a stretch; the prediction
  `attribute of CEO of employer of Denver` has the same depth and a better reading. Key
  questionable -> leaves the fixable class.
- doc 97 "first year a scientific journal published by an organization located in the Bronx":
  key anchors on Bronx; the prediction anchors on "an organization". Both defensible; key
  questionable -> leaves the fixable class.
- doc 98: the question says "American character actor" as a comparison, not a filter; key is
  right; the prediction's `[ actor ]` is a real filter error.
- All other keys stand.
Fixable after rung 0: hops_dropped 4 (71, 72, 78, 89), anchor 2 (76, 81), relation 3, unparseable 1
(86), na_wrong 1 (93), filter 1 (98).

## 5-why on the largest fixable class: hops_dropped (71, 72, 78, 89)
1. Why is a hop dropped? The middle relation is phrased as a participial or relative clause that
   wraps the inner phrase: "a 1982 film loosely adapted from a novel by", "the nursery rhyme
   inspiring", "based on the connector that is often used for", "an experiment by X and another
   man born in".
2. Why does the model collapse it? The synthetic phrasing set renders relations as "the X of Y"
   noun phrases and a few question forms; it has no "Y-participle-from Z" or "the Z that ... Y"
   wrappers, so the model reads the clause as decoration around a known hop.
3. Why has training not covered it? Depth-3 chains are 20 percent of synthetic data and every one
   of them uses the noun-phrase wrapper; the real batches' depth-3 questions almost all use clause
   wrappers.
4. Why did 30 real labels x5 not fix it? Four examples of the pattern in 2500 steps; the
   synthetic majority sets the prior.
Root = MISSING MECHANISM: clause-shaped relation wrappers ("adapted from", "inspired by", "based
on", "by X and another") at depth 2-3 in the generator, and their weight in training.

## Route for this round
hops_dropped -> TAGGER_DEPTH_WEIGHTS 20,35,30,15 (deeper chains), the registered knob. The clause
wrappers themselves are a generator change (a new R3, not a loop round); if this round does not
move hops_dropped on the eval slice, register generator v3 with clause wrappers as the next R3.
Secondary classes (anchor 2, filter 1, na_wrong 1) are below the trigger on their own; no route.
