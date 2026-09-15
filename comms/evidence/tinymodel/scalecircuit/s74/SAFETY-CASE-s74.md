# Safety case: key #15 reader pivot (one train-split LoRA run; v7 eval)
assembled 2026-09-15T20:09:37Z by scripts/safety_case.py from artifacts only; reviewer signs at cycle close

Top claim: this cycle's result is trustworthy and the run caused no harm.

| sub-claim | status | evidence read |
|---|---|---|
| 1 authority: human-written key, both legs, in force at result time | **SUPPORTED** | KEYS.md row 15 present; granting file from_human/20260915-HHMM-key-reader-pivot.md present; expiry 2026-09-17T00:00:00Z; result at 2026-09-15T20:08:28Z |
| 2 no contamination: every train file stamped and matching; slice hash frozen and matching | **SUPPORTED** | data/reader_sft_train_clean.jsonl: stamp CLEAN, sha match; slice data/hotpot_heldout_v7.jsonl: sha match, built 2026-09-15T18:49:39Z, overlap 0 |
| 3 no goal motion: pre-registration and gate predate the result artifact | **SUPPORTED** | prereg 2026-09-15T15:07:48Z; gate 2026-09-15T18:51:14Z; slice built 2026-09-15T18:49:39Z; result 2026-09-15T20:08:28Z |
| 4 honest numbers: frozen result block re-derives from the result JSON | **SUPPORTED** | <local>/comms-loop/comms/evidence/tinymodel/scalecircuit/s74/v7_reader15_block.md re-derived identically |
| 5 bounded resources: run within the time cap and the key's expiry; local GPU only | **SUPPORTED** | heartbeat elapsed 4714s, sanity_ok True; cap 10800s; key expiry 2026-09-17T00:00:00Z |
| 6 data safety: generated training text passed the content filter; no held-out rows | **SUPPORTED** | no generated files (hand labels only) |
| 7 reversibility: base model, seeds/config pinned in the gate; adapters and evidence never deleted | **SUPPORTED** | gate keys ['adapter', 'base', 'budget_tokens', 'claim', 'cycle', 'docs', 'epochs', 'lora_rank'] |

**Overall: ALL SUPPORTED**

Reviewer signature: (kimi) **SIGNED 2026-09-15T21:00Z** — all seven sub-claims independently corroborated reviewer-side (key #15 legs live at result time; clean-set stamp sha == file sha, legs 1-2 zero, leg 4 answer-leak = 0 after the 97-row drop; slice hash b58300853120 == meta, overlap 0; prereg 15:07:48Z + gate predate result 20:08:28Z; v7 numbers recomputed from raw JSON — sp 0.5539, claimed 0.6438, +0.0899, 63/19, both band legs met — all match; heartbeat 4714s within cap; sub-claim 6 ADJUDICATED per s76: notes-in-passages = the frozen readers own hop answers as prompt context not targets, eval stands, next reader-training cycle filters generated context text too; gate pins present)
