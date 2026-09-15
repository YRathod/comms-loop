# 5-why for round 2 (fable, 2026-09-13 ~05:20Z)

Autopsy: models/tagger_loop/autopsy_r2.json. Batch docs 100-129, adapter models/tagger_loop/round1.
Classes on the batch: anchor 5, relation 4, hops_extra 3, na_wrong 3, hops_dropped 1 (16 of 30).

## Round 1 outcome first (the previous 5-why's own test)
Round 1 (route TAGGER_DEPTH_WEIGHTS 20,35,30,15, 60 real labels x5, 1 epoch from the s8 adapter):
eval slice structure 14 -> 14 (tagger_lora tiers), loop measure 14 -> 13; anchor 25 -> 24. The s10
prediction (16-19) MISSED. Class movement on the slice: hops_dropped 5 -> 4, hops_extra 3 -> 4,
filter 1 -> 3. Reweighting depth alone does not move the plateau; the mechanism named in
why_r1 (clause-shaped relation wrappers absent from the generator) is what this round tests.

## Rung 0: are the keys right for the round-2 failures?
- doc 101 "last monarch of England to be overthrown before The English General Election, 1690":
  key `leader of English General Election, 1690` is a stretch; the prediction `leader of England`
  is at least as good. Key questionable -> leaves the fixable class.
- doc 110 "On May 25, 2017 Greg Gianforte won the special election following the resignation of a
  politician ...": key `attribute of brother of Greg Gianforte` uses `brother` as the predecessor
  stand-in (the grammar has no predecessor relation); prediction anchored on "May 25". Anchor
  error is real; relation is a grammar gap, not a model error.
- doc 120 Hardley Flood: key `attribute of leader of Hardley Flood` ("the waterfowl that live in
  X" as leader) is a stretch, prediction anchored on "lagoons"; anchor error real.
- doc 116 "What rule-class city of 26,595 contains the neighborhood Plainview": key
  `home of Plainview` stands; prediction anchored on the number.
- doc 126: key `birthplace of leader of Microwave Jenny` stands; prediction anchored on "Tessa".
- docs 105, 115, 128 (X and Y are both ...): keys NA stand; predictions are chains.
Fixable after rung 0: anchor 4 (110, 116, 120, 126), na_wrong 3, relation 4, hops_extra 3,
hops_dropped 1.

## 5-why on the largest fixable class: anchor (110, 116, 120, 126)
1. Why the wrong anchor? The model picks the first salient span (a date "May 25", a number
   "26,595", a plain noun "lagoons", a first name "Tessa") instead of the named entity that the
   chain hangs on.
2. Why the first span? In every synthetic question the anchor is the LAST span of the phrase and
   nothing that looks like an entity precedes it; position is a perfect cue in training.
3. Why is nothing in front? The generator has no lead-ins with dates or numbers, no numeric
   descriptors on the outer relation, and its descriptor anchors are whole phrases, not a
   descriptor beside a name.
4. Why did 60 real labels not fix it? 4-6 examples per pattern, against 12K synthetic where the
   positional cue never fails.
Root = MISSING MECHANISM (two parts): (a) date/number material before the anchor in the source
side; (b) for na_wrong, the "X and Y are both ..." comparison form is absent from make_na.

## Route for this round (generator v3, registered in the s11 mail before the round trains)
- anchor -> TAGGER_DESC_FRAC 0.25 (registered knob) + v3 lead-ins (TAGGER_LEADIN_FRAC 0.30).
- v3 also carries the why_r1 mechanism: clause-shaped wrappers per relation (CLAUSE_FRAC 0.35
  default) and the comparison NA forms. These enter the regenerated synthetic for this round.
Prediction for the eval slice after round 2 (band pinned before training): structure 14 -> 15-18,
anchor 24 -> 24-26, na_ok 29 -> 29-30. If structure stays at 14 the loop's own rule (<1 pt twice)
stops it, and the plateau is reported as the tagger's ceiling at 0.5B with this grammar.
