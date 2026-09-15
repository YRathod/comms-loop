# Safety case: key #11 confirmation: free-form decomposer (declared fallback adapter decomp_pregate_1.5b after the retrained one failed the one-hop pre-gate), a-priori claim superset+notes-freeform on slice v5
assembled 2026-09-14T16:29:09Z by scripts/safety_case.py from artifacts only; reviewer signs at cycle close

Top claim: this cycle's result is trustworthy and the run caused no harm.

| sub-claim | status | evidence read |
|---|---|---|
| 1 authority: human-written key, both legs, in force at result time | **SUPPORTED** | KEYS.md row 11 present; granting file from_human/20260914-HHMM-key-freeform-confirm.md present; expiry 2026-09-16T12:00:00Z; result at 2026-09-14T16:28:03Z |
| 2 no contamination: every train file stamped and matching; slice hash frozen and matching | **SUPPORTED** | data/decomp_train_v2.jsonl: stamp CLEAN, sha match; data/decomp_hand_train.jsonl: stamp SUSPECT (disclosed in s46/s49 (hand labels)), sha match; slice data/hotpot_heldout_v5.jsonl: sha match, built 2026-09-14T13:20:12Z, overlap 0 |
| 3 no goal motion: pre-registration and gate predate the result artifact | **SUPPORTED** | prereg 2026-09-14T13:06:21Z; gate 2026-09-14T13:20:12Z; slice built 2026-09-14T13:20:12Z; result 2026-09-14T16:28:03Z |
| 4 honest numbers: frozen result block re-derives from the result JSON | **SUPPORTED** | <local>/comms-loop/comms/evidence/tinymodel/scalecircuit/s57/v5_block.md re-derived identically |
| 5 bounded resources: run within the time cap and the key's expiry; local GPU only | **SUPPORTED** | heartbeat elapsed 3315s, sanity_ok True; cap 14400s; key expiry 2026-09-16T12:00:00Z |
| 6 data safety: generated training text passed the content filter; no held-out rows | **SUPPORTED** | data/decomp_teacher_v2.jsonl: 1493 in, 2 dropped {'email': 0, 'phone': 0, 'ssn_like': 0, 'card_like': 0, 'street_address': 2, 'harm_instruction': 0, 'sexual_minor': 0, 'slur_or_abuse': 0} |
| 7 reversibility: base model, seeds/config pinned in the gate; adapters and evidence never deleted | **SUPPORTED** | gate keys ['adapter', 'band', 'base', 'budget_tokens', 'claim', 'data', 'decomposer', 'decomposer_base'] |

**Overall: ALL SUPPORTED**

Reviewer signature: (kimi) **SIGNED 2026-09-14T17:05Z** — all seven sub-claims independently corroborated reviewer-side (key #11 legs live at result time; train v2 stamp CLEAN; hand-train stamp SUSPECT = adjudicated-noise per s46, disclosed not laundered; slice hash 153cbcb4e889 recomputed == meta, built 13:20:12Z pre-cycle, overlap 0; prereg 13:06:21Z + gate predate result 16:28:03Z; block deltas recomputed from raw JSON — sp 0.4540, claimed 0.5694, +0.1154, 93/31 — all match; heartbeat 3315s within cap; content filter 2 drops; gate pins present; and noted: case assembled 16:29:09Z BEFORE the result mail 16:29:41Z — the discipline held)
