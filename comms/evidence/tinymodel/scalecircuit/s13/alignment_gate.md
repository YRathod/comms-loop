# alignment gate — mechanical legs

overall: **FAIL**

| leg | verdict | evidence |
|---|---|---|
| refs | PASS | 6/6 files resolve non-empty |
| leakage | PASS | eval slice 30 docs / 26 questions vs 2 train file(s): id overlap none, question overlap 0 |
| stamp-order | PASS | 2/2 pins predate the result artifact |
| config | FAIL | 13/17 pinned keys match run args; MISMATCH: {'train': {'pinned': 'models/tagger_loop\train_r2.jsonl', 'ran': 'models/tagger_loop\\train_r2.jsonl'}, 'out': {'pinned': 'models/tagger_loop\round2', 'ran': 'models/tagger_loop\\round2'}, 'extra': {'pinned': 'models/tagger_loop\real_r2.jsonl', 'ran': 'models/tagger_loop\\real_r2.jsonl'}, 'init_adapter': {'pinned': 'models/tagger_loop\round1', 'ran': 'models/tagger_loop/round1'}} |

reviewer judgment still owed (not mechanical):
- goal-vs-gate: sample PASSING outputs for shortcut structure (named shortcut classes for this thread)
- goal motion: were bands/goal ever re-pinned AFTER numbers existed?
- selective reporting: any doc/class dropped from the reported aggregate?
