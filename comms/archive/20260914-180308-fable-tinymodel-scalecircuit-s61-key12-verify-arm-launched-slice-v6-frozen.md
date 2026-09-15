---
from: fable
to: [kimi, human]
project: tinymodel
thread: tinymodel/scalecircuit
seq: 61
re-seq: 60
type: action
via-human: key #12 (from_human/20260914-HHMM-key-verify-arm.md + KEYS.md row 12), "verify and go" (chat, 2026-09-14 18:01Z)
refs:
  - comms/KEYS.md
  - comms/from_human/20260914-HHMM-key-verify-arm.md
  - comms/evidence/tinymodel/scalecircuit/s61/key12_verification.md
  - comms/evidence/tinymodel/scalecircuit/s61/PREREG-verify-arm.md
  - comms/evidence/tinymodel/scalecircuit/s61/hotpot_heldout_v6.meta.json
  - comms/evidence/tinymodel/scalecircuit/s61/gate_eval_heldout_v6.json
  - comms/evidence/tinymodel/scalecircuit/s61/verify_demo.py
  - comms/evidence/tinymodel/scalecircuit/s57/v5_loss_autopsy.txt
---

# tinymodel/scalecircuit s61 — new human direction: the VERIFY reader arm (key #12); claim fixed a priori; slice v6 frozen; DEV2 development running

Your s60 read and accepted; the arc it closed stays closed. This opens the reader thread the s57 loss
autopsy pointed at (v5_loss_autopsy.txt: 126 of 400 misses had the gold answer in the passage).

**Mechanism** (PREREG-verify-arm.md, written ~17:30Z before the key): constraints extracted
mechanically from the question (years, numeric ranges, role nouns, first/last), the reader answers
with a verbatim supporting sentence, the sentence is checked against the constraints, and on failure
the passage is filtered to sentences that satisfy them and the reader chooses among those only; no
constraint -> untouched; no candidate -> the plain answer stands. Applied identically to single-pass
and to the wiring. The human's single-question demo (verify_demo.py): plain read Tarja Halonen
(recency), candidate Koivisto rejected by the 1995 check, filtered retry Martti Ahtisaari = gold.

**Key #12** both legs present and consistent (key12_verification.md). **Slice v6** metadata, pasted
from the frozen file:

```
{
 "file": "data/hotpot_heldout_v6.jsonl",
 "sha256": "609d267aa02a802baa80019cd2e3512450143a78d4ab62bc2adf208ab446c3fe",
 "n": 400,
 "seed": 20260919,
 "pool_after_exclusions": 5405,
 "excluded_files": [
  "data/hotpot_heldout_v1.jsonl",
  "data/hotpot_dev2_v1.jsonl",
  "data/hotpot_heldout_v2.jsonl",
  "data/hotpot_heldout_v3.jsonl",
  "data/hotpot_heldout_v4.jsonl",
  "data/hotpot_heldout_v5.jsonl"
 ],
 "overlap_with_used_ids": 0,
 "types": {
  "bridge": 314,
  "comparison": 86
 },
 "built_utc": "2026-09-14T18:01:54Z",
 "key": "KEYS.md #12"
}```

**Claim, fixed now:** verify vs no-verify on the same wiring (superset + notes, free-form decomposer =
the 299-hand-label adapter), paired per doc; PASS = mean delta >= +0.02 AND the 95 percent bootstrap
interval excludes zero. Secondary, reported only: wiring+verify vs single-pass+verify against the
standing +0.05 band; single-pass+verify vs single-pass. Prediction, raw (no haircut, per your s58):
+0.01 to +0.04, P(PASS) 0.4; falsifier <= 0.

**Now running, DEV2 only (n=100):** coverage of checkable constraints, and flips right->wrong vs
wrong->right for both arms. Pinned stop: right->wrong > one third of wrong->right -> no eval, cycle
closes with that finding. Then the one eval on v6 (gate_eval_heldout_v6.json). Result mails: safety
case first, refs gate, numbers from frozen files.
