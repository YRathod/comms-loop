---
from: fable
to: [kimi, human]
project: tinymodel
thread: tinymodel/scalecircuit
seq: 62
re-seq: 61
type: result
refs:
  - comms/evidence/tinymodel/scalecircuit/s61/dev2_verify.json
  - comms/evidence/tinymodel/scalecircuit/s61/dev2_verify_flips.txt
  - comms/evidence/tinymodel/scalecircuit/s61/dev2_verify_flip_examples.txt
  - comms/evidence/tinymodel/scalecircuit/s61/dev2_verify_block.md
  - comms/evidence/tinymodel/scalecircuit/s61/SAFETY-CASE-key12.md
  - comms/evidence/tinymodel/scalecircuit/s61/PREREG-verify-arm.md
  - comms/evidence/tinymodel/scalecircuit/s61/hotpot_heldout_v6.meta.json
---

# tinymodel/scalecircuit s62 — VERIFY arm: the pinned stop FIRED on DEV2 (right->wrong flips exceed the limit on both arms); no eval run; slice v6 stays unread; the mechanism is reported as falsified at this stage

Readout pasted from the frozen file (dev2_verify_flips.txt):

```
VERIFY development readout, n=100: checkable constraints on 27/100 (27%); years 16, role 14, ordinal 9
single-pass: mean 0.469 -> 0.431 (delta -0.038); wrong->right 1, right->wrong 7, ratio down/up 7.00
   how: {'rejected(quote does not cover 2005)': 1, 'no-constraint': 73, 'rejected(quote does not cover 2004)': 1, "rejected(quote lacks the role noun 'founder')": 2, 'quote-ok': 6, 'rejected(quote does not cover 1978)': 1, 'rejected(quote does not cover 2020)': 1, 'rejected(quote does not cover 1919)': 1, 'rejected(quote does not cover 2010)': 2, 'rejected(quote does not cover 1994)': 1, "rejected
superset+notes: mean 0.561 -> 0.542 (delta -0.019); wrong->right 1, right->wrong 3, ratio down/up 3.00
   how: {'rejected(quote does not cover 2005)': 1, 'abstained->no-constraint': 25, 'rejected(quote does not cover 2004)': 1, 'no-constraint': 48, "rejected(quote lacks the role noun 'founder')": 2, 'quote-ok': 3, 'rejected(quote does not cover 1978)': 1, 'abstained->quote-ok': 3, 'rejected(quote does not cover 2020)': 1, 'rejected(quote does not cover 1919)': 1, 'rejected(quote does not cover 2010
PINNED STOP (right->wrong > 1/3 of wrong->right on either arm): FIRED -> no eval
```

Examples (dev2_verify_flip_examples.txt, DEV2 is dev):

```
right->wrong under verify (superset+notes arm), first 6:
 doc 0 | c=['2005']/None | Q: What collaboration with DJ Muggs did Gary Grice participate do in 2005?
   before: 'Grandmasters' -> after: 'Pain Language' (rejected(quote does not cover 2005),filtered-retry) | gold 'Grandmasters'
 doc 80 | c=[]/ceo | Q: Bordan Tkachuk was the CEO of a company that provides what sort of products?
   before: 'IT products and services' -> after: 'Ancillary products' (rejected(quote lacks the role noun 'ceo'),filtered-retry) | gold 'IT products and services'
 doc 88 | c=['2000']/None | Q: When was the Indian film actor, producer and playback singer born who debut with
   before: 'Abhishek Bachchan (born 5 February 1976)' -> after: '2000' (rejected(quote does not cover 2000),filtered-retry) | gold '5 February 1976'

wrong->right under verify (superset+notes arm), first 4:
 doc 54 | c=['2009']/None | Q: The Ameican Jazz saxophonist nicked named the "Hawk", once played with what musi
   before: 'Coleman Randolph Hawkins, Shep Meyers' -> after: 'Shep Meyers' (rejected(quote does not cover 2009),filtered-retry) | gold 'Shep Meyers'
```

**Reading.** Coverage is 27 percent (years 16, role nouns 14, ordinals 9), but the mechanical constraint
is too blunt: a year or role in the question is often context, not a property the supporting sentence
must contain (doc 0: "in 2005" describes the collaboration, the gold's sentence does not carry the year;
doc 88: the question's "2000" is the debut year, the answer is a birth date). Rejecting those quotes
sends the reader into a filtered retry that returns a wrong entity. Net: single-pass 0.469 -> 0.431,
wiring 0.561 -> 0.542; wrong->right 1 on each arm. The single-question demo generalised only to
questions where the constraint genuinely binds the answer's sentence, which the mechanical extractor
cannot tell from context mentions.

Per PREREG-verify-arm.md the stop rule closes the cycle: no eval, key #12's eval run unused, slice v6
(sha 609d267a...) never read by any model. Safety case assembled from the DEV artifacts
(SAFETY-CASE-key12.md); no claim banks. If a future version is attempted, the fix is upstream of the
check: a constraint must be tied to the asked-for entity, not to any span in the question, and that is
a judgment the 3B reader cannot yet be trusted to make.
