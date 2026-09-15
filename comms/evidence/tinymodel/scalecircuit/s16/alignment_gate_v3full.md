# alignment gate — mechanical legs

overall: **FAIL**

| leg | verdict | evidence |
|---|---|---|
| refs | PASS | 6/6 files resolve non-empty |
| leakage | PASS | eval slice 30 docs / 27 questions vs 2 train file(s): id overlap none, question overlap 0 |
| distribution | FAIL | 2344/20120 train questions (11.7%) share a content 3-gram with the eval questions (FAIL>2%, SUSPECT>0.5%); e.g. ['What was the country in which the town in which Yau Ma Tei North was born is loc', 'What is the capital of the lower house of parliament?', 'What is the capital of the fourth studio album made by McLaren MP4/11?'] |
| stamp-order | PASS | 2/2 pins predate the result artifact |
| config | PASS | 17/17 pinned keys match run args |

reviewer judgment still owed (not mechanical):
- goal-vs-gate: sample PASSING outputs for shortcut structure (named shortcut classes for this thread)
- goal motion: were bands/goal ever re-pinned AFTER numbers existed?
- selective reporting: any doc/class dropped from the reported aggregate?
