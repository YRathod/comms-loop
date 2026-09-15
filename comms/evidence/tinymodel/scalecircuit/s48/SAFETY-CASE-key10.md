# Safety case: key #10 pivot: free-form decomposer (closed at the DEV2 discriminant, no eval run)
assembled 2026-09-14T06:14:50Z by scripts/safety_case.py from artifacts only; reviewer signs at cycle close

Top claim: this cycle's result is trustworthy and the run caused no harm.

| sub-claim | status | evidence read |
|---|---|---|
| 1 authority: human-written key, both legs, in force at result time | **SUPPORTED** | KEYS.md row 10 present; granting file from_human/20260914-HHMM-key-freeform-decomposer.md present; expiry 2026-09-16T00:00:00Z; result at 2026-09-14T06:14:07Z |
| 2 no contamination: every train file stamped and matching; slice hash frozen and matching | **SUPPORTED** | data/decomp_train_full.jsonl: stamp CLEAN, sha match; slice data/hotpot_heldout_v4.jsonl: sha match, built 2026-09-14T04:02:59Z, overlap 0 |
| 3 no goal motion: pre-registration and gate predate the result artifact | **SUPPORTED** | prereg 2026-09-14T03:44:07Z; gate 2026-09-14T05:07:23Z; slice built 2026-09-14T04:02:59Z; result 2026-09-14T06:14:07Z |
| 4 honest numbers: frozen result block re-derives from the result JSON | **SUPPORTED** | <local>/comms-loop/comms/evidence/tinymodel/scalecircuit/s48/dev2_freeform_block.md re-derived identically |
| 5 bounded resources: run within the time cap and the key's expiry; local GPU only | **SUPPORTED** | heartbeat elapsed 2747s, sanity_ok True; cap 14400s; key expiry 2026-09-16T00:00:00Z |
| 6 data safety: generated training text passed the content filter; no held-out rows | **SUPPORTED** | data/decomp_teacher_train.jsonl: 1645 in, 2 dropped {'email': 0, 'phone': 0, 'ssn_like': 0, 'card_like': 0, 'street_address': 2, 'harm_instruction': 0, 'sexual_minor': 0, 'slur_or_abuse': 0} |
| 7 reversibility: base model, seeds/config pinned in the gate; adapters and evidence never deleted | **SUPPORTED** | gate keys ['accum', 'allow_suspect', 'allow_unstamped', 'base', 'bs', 'dev', 'epochs', 'eval_only'] |

**Overall: ALL SUPPORTED**

Reviewer signature: (kimi) **SIGNED 2026-09-14T06:45Z** — all seven sub-claims independently corroborated reviewer-side (key #10 legs; train stamp CLEAN; slice hash e4de21de frozen 04:02:59Z pre-cycle; prereg 03:44Z + gate 05:07Z predate result 06:14Z; block deltas recomputed from raw JSON — chain -0.1169, superset +0.0028, notes +0.0834/+0.0891 all match; heartbeat 2747s within cap; filter 2 drops confirmed; gate pins present)
