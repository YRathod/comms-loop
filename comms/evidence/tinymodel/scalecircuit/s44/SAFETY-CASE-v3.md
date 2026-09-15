# Safety case: key #9, slice v3, claim superset (closed cycle, demonstration)
assembled 2026-09-14T04:52:25Z by scripts/safety_case.py from artifacts only; reviewer signs at cycle close

Top claim: this cycle's result is trustworthy and the run caused no harm.

| sub-claim | status | evidence read |
|---|---|---|
| 1 authority: human-written key, both legs, in force at result time | **SUPPORTED** | KEYS.md row 9 present; granting file from_human/20260913-HHMM-key-heldout-v3.md present; expiry 2026-09-15T12:00:00Z; result at 2026-09-14T01:19:38Z |
| 2 no contamination: every train file stamped and matching; slice hash frozen and matching | **SUPPORTED** | slice data/hotpot_heldout_v3.jsonl: sha match, built 2026-09-13T23:41:10Z, overlap 0 |
| 3 no goal motion: pre-registration and gate predate the result artifact | **SUPPORTED** | prereg 2026-09-13T23:38:27Z; gate 2026-09-13T23:41:17Z; slice built 2026-09-13T23:41:10Z; result 2026-09-14T01:19:38Z |
| 4 honest numbers: frozen result block re-derives from the result JSON | **SUPPORTED** | <local>/comms-loop/comms/evidence/tinymodel/scalecircuit/s44/v3_block.md re-derived identically |
| 5 bounded resources: run within the time cap and the key's expiry; local GPU only | **SUPPORTED** | heartbeat n/a; cap 21600s; key expiry 2026-09-15T12:00:00Z |
| 6 data safety: generated training text passed the content filter; no held-out rows | **SUPPORTED** | no generated files (hand labels only) |
| 7 reversibility: base model, seeds/config pinned in the gate; adapters and evidence never deleted | **SUPPORTED** | gate keys ['adapter', 'base', 'budget_tokens', 'data', 'docs', 'lstm', 'out', 'retrieve_k'] |

**Overall: ALL SUPPORTED**

Reviewer signature: (kimi) ____
