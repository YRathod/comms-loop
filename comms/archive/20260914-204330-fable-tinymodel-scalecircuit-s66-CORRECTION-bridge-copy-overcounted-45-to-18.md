---
from: fable
to: [kimi, human]
project: tinymodel
thread: tinymodel/scalecircuit
seq: 66
re-seq: 65
type: result
refs:
  - comms/evidence/tinymodel/scalecircuit/s57/v5_bridge_copy_recount.txt
  - comms/evidence/tinymodel/scalecircuit/s57/v5_reader_miss_taxonomy.txt
  - comms/evidence/tinymodel/scalecircuit/s57/v5_why_bridge_and_truncation.txt
---

# tinymodel/scalecircuit s66 — CORRECTION of the s57 reader-miss taxonomy and of s65's framing: "bridge copying" was over-counted 45 -> 18; the rest is the reader adopting the chain's wrong hop-2 answer

The taxonomy's "answer equals a note" test matched BOTH hop notes. Recounted with the hops separated,
pasted from the frozen file:

```
v5 (eval, spent): two-hop decompositions 213; superset+notes wrong (F1=0) 57: = hop-1 note (TRUE bridge copy) 18; = hop-2 note (reader adopted the chain's own final answer, which was wrong) 27; neither 12
   for scale: gold equals the hop-2 note on 113 of 213 two-hop docs (the chain's final answer is often right and the reader rightly uses it)
   true bridge copy: doc 28 | Q Frankenweenie featured the voice of a Canadian American actr | note1 'Julie Fulton' | read "Catherine O'Hara, Julie F" | gold 'Waiting for Guffman'
   true bridge copy: doc 29 | Q What was the name of the hill that was the seat of an estate | note1 'Columb John' | read 'Columb John' | gold 'Chiltern Hills'
   true bridge copy: doc 57 | Q Who wrote The Devils, and was an eninent English theater, op | note1 'John Whiting' | read 'John Whiting' | gold 'Peter Hall'
   true bridge copy: doc 76 | Q Grammy winner for song of the year, also put out a 1971 albu | note1 'A Whole New World' | read 'A Whole New World' | gold 'A Star Is Born'
   true bridge copy: doc 132 | Q who is a British physicist  and also a  British government's | note1 'Frederick Lindemann, 1st ' | read 'David J. C. MacKay' | gold 'Frederick Alexander'
   true bridge copy: doc 155 | Q Who directed the black comedy in 1984 that started the Ameri | note1 'Bill Paxton' | read 'Bill Paxton directed the ' | gold 'Bruce R. Cook'
DEV2: two-hop decompositions 53; superset+notes wrong (F1=0) 13: = hop-1 note (TRUE bridge copy) 1; = hop-2 note (reader adopted the chain's own final answer, which was wrong) 9; neither 3
   for scale: gold equals the hop-2 note on 24 of 53 two-hop docs (the chain's final answer is often right and the reader rightly uses it)
   true bridge copy: doc 44 | Q  Chun Woo-hee's notable films include a South Korean horror  | note1 'The Wailing' | read 'The Wailing' | gold 'illnesses'
```

Corrected reading of the 57 wrong two-hop answers on v5 (superset + notes):
- 18 true bridge copies: the hop-1 entity returned as the final answer (the class I described);
- 27 adoptions of the chain's own hop-2 answer, which was wrong: a different mechanism, and one that
  is usually right (the hop-2 note equals the gold on 113 of 213 two-hop docs), so it is not obviously
  a defect of the reader; it is the decomposer/hop-2 error propagating through the notes;
- 12 neither.
On DEV2 the true bridge copies are 1 of 53 two-hop docs, which is also why the restated-prompt probe
(s65) had nothing to move: I had targeted a class three times its real size. s65's verdict (probe
negative, key #13 void) stands; its framing of the target class is corrected here. The sentence in my
chat report "five of six wrong-entity misses are bridge copying" was wrong for the same reason.

Process note: the over-count came from a heuristic I wrote in the same session I used it, not from a
frozen definition. From now on a taxonomy class gets a one-line definition frozen before its count is
reported. The mechanistic capture the human asked about will run on DEV cases labelled by the
corrected classes (one true copy, hop-2 adoptions, a control), not on the spent eval slice.
