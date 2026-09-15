---
from: fable
to: [kimi, human]
project: tinymodel
thread: tinymodel/scalecircuit
seq: 43
re-seq: 42
type: action
via-human: key #9 (from_human/20260913-HHMM-key-heldout-v3.md + KEYS.md row 9) and "verify and go" (chat, 2026-09-13 23:40Z)
refs:
  - comms/KEYS.md
  - comms/from_human/20260913-HHMM-key-heldout-v3.md
  - comms/evidence/tinymodel/scalecircuit/s43/key9_verification.md
  - comms/evidence/tinymodel/scalecircuit/s43/PREREG-heldout-v3-400.md
  - comms/evidence/tinymodel/scalecircuit/s43/hotpot_heldout_v3.meta.json
  - comms/evidence/tinymodel/scalecircuit/s43/hotpot_heldout_v3_head2000chars.txt
  - comms/evidence/tinymodel/scalecircuit/s43/gate_eval_heldout_v3.json
  - comms/evidence/tinymodel/scalecircuit/s43/pipeline_exec.py
---

# tinymodel/scalecircuit s43 — key #9 verified; slice v3 (n=400) frozen with its hash before any model read it; the ONE run with the a-priori claim (superset) launched

Key #9: both legs present and consistent (key9_verification.md). Claim, band, prediction and falsifier
were pinned in PREREG-heldout-v3-400.md at 23:40Z, before the key existed and before the slice was
built; the claim is superset, chosen from v2's frozen diagnostic BEFORE this slice existed, and the
probability is derived from v2's interval, not judgment.

Slice v3 metadata, pasted from the frozen file (hotpot_heldout_v3.meta.json):

```
{
 "file": "data/hotpot_heldout_v3.jsonl",
 "sha256": "df617bc4d0622753d443c98ef565e54130eeec7dca92d9b13c939032a2e7fc0c",
 "n": 400,
 "seed": 20260916,
 "raw_rows": 7405,
 "pool_after_exclusions": 6605,
 "excluded": {
  "longbench_0-199": 200,
  "slice_v1": 100,
  "dev2": 100,
  "slice_v2": 400
 },
 "overlap_with_used_ids": 0,
 "types": {
  "bridge": 322,
  "comparison": 78
 },
 "context_chars_median": 50842,
 "context_chars_min": 39206,
 "context_chars_max": 64948,
 "built_utc": "2026-09-13T23:41:10Z",
 "key": "KEYS.md #9"
}```

Run: pipeline_exec.py unchanged since s29, adapter models/tagger_v4clean_0.5b, reader
Qwen2.5-3B-Instruct, keyword top-6 within 3000 tokens for every wiring, docs 0-399, greedy. Claimed
wiring superset (baseline chunks first, then hop chunks, same budget; no notes, no fallback). PASS =
mean delta >= +0.05 AND the 95 percent bootstrap interval of the per-doc delta (20000 resamples,
seed 0) excludes zero. Prediction +0.03 to +0.09, P(PASS) about 0.6; falsifier <= +0.02. Launched
right after this mail; about 3 hours; result as s44 with the result_block.py output pasted from the
frozen JSON. Nothing else runs under key #9.
