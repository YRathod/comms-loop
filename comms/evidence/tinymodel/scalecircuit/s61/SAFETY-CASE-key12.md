# Safety case: key #12 VERIFY arm (closed at the DEV2 pinned stop; no eval run)
assembled 2026-09-14T18:26:03Z by scripts/safety_case.py from artifacts only; reviewer signs at cycle close

Top claim: this cycle's result is trustworthy and the run caused no harm.

| sub-claim | status | evidence read |
|---|---|---|
| 1 authority: human-written key, both legs, in force at result time | **SUPPORTED** | KEYS.md row 12 present; granting file from_human/20260914-HHMM-key-verify-arm.md present; expiry 2026-09-17T00:00:00Z; result at 2026-09-14T18:24:29Z |
| 2 no contamination: every train file stamped and matching; slice hash frozen and matching | **SUPPORTED** | slice data/hotpot_heldout_v6.jsonl: sha match, built 2026-09-14T18:01:54Z, overlap 0 |
| 3 no goal motion: pre-registration and gate predate the result artifact | **SUPPORTED** | prereg 2026-09-14T17:58:45Z; gate 2026-09-14T18:01:54Z; slice built 2026-09-14T18:01:54Z; result 2026-09-14T18:24:29Z |
| 4 honest numbers: frozen result block re-derives from the result JSON | **SUPPORTED** | <local>/comms-loop/comms/evidence/tinymodel/scalecircuit/s61/dev2_verify_block.md re-derived identically |
| 5 bounded resources: run within the time cap and the key's expiry; local GPU only | **SUPPORTED** | heartbeat n/a; cap 21600s; key expiry 2026-09-17T00:00:00Z |
| 6 data safety: generated training text passed the content filter; no held-out rows | **SUPPORTED** | no generated files (hand labels only) |
| 7 reversibility: base model, seeds/config pinned in the gate; adapters and evidence never deleted | **SUPPORTED** | gate keys ['adapter', 'band', 'base', 'budget_tokens', 'claim', 'data', 'decomposer', 'decomposer_base'] |

**Overall: ALL SUPPORTED**

Reviewer signature: (kimi) **SIGNED 2026-09-14T19:00Z** — all seven sub-claims independently corroborated reviewer-side (key #12 legs live; slice hash 609d267aa02a recomputed == meta AND STILL UNREAD; prereg + gate predate the DEV result; block deltas recomputed from raw dev2_verify.json — sp 0.4687->0.4307, wiring 0.5607->0.5417, flips 7/1 and 3/1, stop arithmetic correct — all match; resources within cap; data safety vacuous (no training); reversibility pins present)
