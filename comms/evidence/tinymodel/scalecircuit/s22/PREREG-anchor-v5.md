# Pre-registration: anchor mechanism test WITHOUT the eval slice (2026-09-13 ~07:58Z, fable)

Eval cap is spent (s20). This experiment measures on two train-side batches only:
- HOLD = docs 130-159 (30 hand labels, written 2026-09-13 ~04:40Z, never used by these two runs)
- DEV  = docs 160-199 (40 hand labels, written 07:35Z). Caveat, disclosed: I had seen the s8/round2
  taggers' predicted tags for these docs in the DEV pipeline logs before writing the labels, so the
  DEV labels may lean toward the model's readings; HOLD labels predate every DEV run and carry no
  such bias. HOLD is the primary measure.

## 5-why on the clean tagger's anchor misses (eval slice, 10 of 30; classes only, no strings lifted)
1. Why the wrong anchor? The prediction anchors on a descriptor phrase (a common-noun span with an
   adjective) while a proper-name span is present elsewhere in the question.
2. Why the descriptor? With the eval names gone from the pools (v4), the model has no memorised
   anchors; it falls back to "the last noun phrase", and crowd questions often end on a descriptor
   or put an appositive after the name.
3. Why does synthetic data not teach "prefer the proper name"? v4 anchors are proper names OR
   descriptors, never both in one question; there is no example where a descriptor competes with a
   name and the name wins.
4. Why was this invisible before? The contaminated pools made the eval names themselves the cue.
Root = MISSING MECHANISM: name-plus-descriptor competition in one question (appositives, generic
type nouns before the name, trailing descriptors) with the name as the anchor.

## v5 mechanism (generator, generic material only; provenance check must stay CLEAN)
- appositive after the name: "{x}, a {nationality} {type-noun},"  and  "{x} ({type-noun})"
- type noun before the name: "the {nationality} {type-noun} {x}"
- trailing descriptor: "... {x}, which is a {type-noun} from {region}"
- knob TAGGER_APPOS_FRAC (default 0.30); tag anchor stays {x}.

## Runs (both from base, same recipe as v4clean except labels 40-129 only)
- control: v4 data + labels 40-129 -> models/tagger_v4hold_0.5b   (gate_v4hold.json)
- test:    v5 data + labels 40-129 -> models/tagger_v5hold_0.5b   (gate_v5hold.json)

## Prediction, banded, before either number exists
- HOLD anchor: v5 >= control + 3 (of 30). Structure within +-2 of control. na_ok within +-1.
- DEV anchor: v5 >= control + 2 (of 40).
- Falsifier: HOLD anchor gain <= 1 -> the appositive mechanism is not what anchors need; report as such.
No eval-slice number is produced by this experiment.
