# Safety case: overnight 2026-09-15 stacked wiring (key #14 void unused; dev only)
assembled 2026-09-15T07:27:00Z by scripts/safety_case.py from artifacts only; reviewer signs at cycle close

Top claim: this cycle's result is trustworthy and the run caused no harm.

| sub-claim | status | evidence read |
|---|---|---|
| 1 authority: human-written key, both legs, in force at result time | **UNSUPPORTED** | KEYS.md row 14 present; granting file from_human/20260915-HHMM-key-stacked-v7.md present; expiry 2026-09-16T00:00:00Z; result at 2026-09-15T06:57:36Z |
| 2 no contamination: every train file stamped and matching; slice hash frozen and matching | **SUPPORTED** | slice data/hotpot_dev3_v1.jsonl: sha match, built 2026-09-15T03:55:49Z, overlap 0 |
| 3 no goal motion: pre-registration and gate predate the result artifact | **UNSUPPORTED** | prereg 2026-09-15T07:22:28Z; gate 2026-09-15T07:26:55Z; slice built 2026-09-15T03:55:49Z; result 2026-09-15T06:57:36Z |
| 4 honest numbers: frozen result block re-derives from the result JSON | **SUPPORTED** | <local>/comms-loop/comms/evidence/tinymodel/scalecircuit/s72/dev3_stacked_block.md re-derived identically |
| 5 bounded resources: run within the time cap and the key's expiry; local GPU only | **SUPPORTED** | heartbeat n/a; cap 21600s; key expiry 2026-09-16T00:00:00Z |
| 6 data safety: generated training text passed the content filter; no held-out rows | **SUPPORTED** | no generated files (hand labels only) |
| 7 reversibility: base model, seeds/config pinned in the gate; adapters and evidence never deleted | **SUPPORTED** | gate keys ['base', 'budget_tokens', 'cycle', 'decomposer', 'decomposer_base', 'docs', 'eval_slice_read', 'key14_gate'] |

**Overall: UNSUPPORTED CLAIMS PRESENT -> HOLD**

Reviewer signature: (kimi) ____
