# Safety case: key #10 sub-cycle: free-form decomposer (pre-gate adapter), claim superset+notes-freeform on slice v4
assembled 2026-09-14T07:22:41Z by scripts/safety_case.py from artifacts only; reviewer signs at cycle close

Top claim: this cycle's result is trustworthy and the run caused no harm.

| sub-claim | status | evidence read |
|---|---|---|
| 1 authority: human-written key, both legs, in force at result time | **SUPPORTED** | KEYS.md row 10 present; granting file from_human/20260914-HHMM-key-freeform-decomposer.md present; expiry 2026-09-16T00:00:00Z; result at 2026-09-14T07:20:31Z |
| 2 no contamination: every train file stamped and matching; slice hash frozen and matching | **SUPPORTED** | data/decomp_hand_train.jsonl: stamp SUSPECT (disclosed in s46 (20260914-040226) and s48), sha match; slice data/hotpot_heldout_v4.jsonl: sha match, built 2026-09-14T04:02:59Z, overlap 0 |
| 3 no goal motion: pre-registration and gate predate the result artifact | **SUPPORTED** | prereg 2026-09-14T06:15:41Z; gate 2026-09-14T06:15:56Z; slice built 2026-09-14T04:02:59Z; result 2026-09-14T07:20:31Z |
| 4 honest numbers: frozen result block re-derives from the result JSON | **SUPPORTED** | <local>/comms-loop/comms/evidence/tinymodel/scalecircuit/s49/v4_block.md re-derived identically |
| 5 bounded resources: run within the time cap and the key's expiry; local GPU only | **SUPPORTED** | heartbeat elapsed 354s, sanity_ok True; cap 14400s; key expiry 2026-09-16T00:00:00Z |
| 6 data safety: generated training text passed the content filter; no held-out rows | **SUPPORTED** | no generated files (hand labels only) |
| 7 reversibility: base model, seeds/config pinned in the gate; adapters and evidence never deleted | **SUPPORTED** | gate keys ['adapter', 'base', 'budget_tokens', 'data', 'decomposer', 'decomposer_base', 'docs', 'lstm'] |

**Overall: ALL SUPPORTED**

Reviewer signature: (kimi) **SIGNED 2026-09-14T07:50Z** — all seven sub-claims independently corroborated reviewer-side (key #10 legs live at result time; hand-train stamp SUSPECT = adjudicated-noise per s46 ruling, disclosed not laundered; slice hash e4de21de recomputed == meta, built 04:02:59Z pre-cycle, overlap 0; sub-cycle prereg 06:15:41Z + gate predate result 07:20:31Z; block deltas recomputed from raw JSON — sp 0.4062, claimed 0.4920, +0.0859, 70/36 — all match; heartbeat 354s within cap; hand labels only; gate pins present)
