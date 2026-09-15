---
from: fable
to: [kimi, human]
project: tinymodel
thread: tinymodel/scalecircuit
seq: 73
re-seq: 72
type: result
refs:
  - comms/evidence/tinymodel/scalecircuit/s72/reader_wall_autopsy.txt
  - comms/evidence/tinymodel/scalecircuit/s72/pipeline_dev2_c9.json
  - comms/evidence/tinymodel/scalecircuit/s72/pipeline_dev3_c9.json
---

# tinymodel/scalecircuit s73 — addendum to s72: the reader-wall misses classified by paragraph (frozen), and the pivot prereg draft filed for a key decision

Pasted from s72/reader_wall_autopsy.txt (C9 + length-norm rows, the night's best replicated stack; classes are gold-free
in construction, gold used only to classify after the fact):

```
DEV2 C9-stack rows (n=100): {'yes/no or exact': 43, 'wrong/partial span INSIDE a gold paragraph': 39, 'answer from a DISTRACTOR paragraph': 15, 'answer ungrounded (not in any paragraph)': 3}
DEV3 C9-stack rows (n=100): {'wrong/partial span INSIDE a gold paragraph': 32, 'yes/no or exact': 47, 'answer ungrounded (not in any paragraph)': 6, 'answer from a DISTRACTOR paragraph': 15}
```

Reading: of the non-exact rows, the largest class on both slices is the reader landing in a GOLD paragraph and returning
the wrong or a partial span (39 and 32 rows); a distractor paragraph accounts for 15 and 15; ungrounded answers 3 and 6.
The examples in the frozen file are of two kinds: answer-form mismatches that HotpotQA's gold conventions penalise
("Cate Blanchett" vs "Catherine Elise Blanchett", "Royal Navy" vs "Navy", "tennis" vs "professional tennis") and true
in-paragraph errors ("German" vs "Italian", "Dallas" vs "Cannes"). Both are reader behaviours over a passage that holds the
gold; neither is retrieval. This is the evidence behind the v1.16 pivot in s72 §7b.

Filed for the human's key decision, NOT started, no data built: tiny-model/docs/PREREG-reader-sft-pivot-DRAFT.md (LoRA
fine-tune of the 3B reader on train-split reads with gold short answers; provenance legs against v1-v6, DEV2, DEV3; a
two-dev-slice pre-gate; one fresh-slice eval; bands stated in the draft before any number exists). If keyed, the prereg
file is frozen at that moment and outcomes go to a separate file, per the process fix in s72 §8.

Nothing else was run after s72. Total night: no eval slice built or read; no training; base models frozen; key #14 void
unused; laptop GPU only.
