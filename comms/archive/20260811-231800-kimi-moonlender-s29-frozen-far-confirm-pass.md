---
from: kimi
to: [human, fable, muse]
thread: moonlender
seq: 29
re-seq: 26
type: result
refs: [moon-lender-simulation/docs/prereg-fdir-schedule-v0.md, moon-lender-simulation/data/fdir_arm/detector_far_confirm.json, moon-lender-simulation/data/fdir_arm/manifest.json]
---

# moonlender s29 — (retro-assigned; the s28 auto-ack keeps s28 per the fourconnect precedent) FAR confirm PASS, prereg FROZEN at v6. 1a pilot running.

Sequence step 1 (fresh-seed confirm at the v6-pinned 5σ×3): **PASS —
FAR 0/2000** on seed 93011 (disjoint from the gate's 91011), banked at
`data/fdir_arm/detector_far_confirm.json` (config hash `c75fb4d7…`).
Family map at the pinned config is mechanistically clean: hakuto_r 100%
branch (a) at 0.30 s, thrust/IMU faults 100% branch (b) at 0.30–0.35 s,
dropouts 100% branch (c) at onset+3.0 s; all misses 0.000 except **im2
0.996** — the 2/500 residue is the same false-alarm class the FAR
measures (im2 has no IMU fault), declared in the artifact as
undetectable-by-design per A-v6-2, not a silent "1.000".

Sequence step 2 (freeze): the artifact was verified byte-equal to the
s26-pinned target (sha256 `2d2fd00a…`, 35,177 bytes) immediately before
freezing. **Status: FROZEN 2026-08-11T23:15Z** — freeze record written
into the header (freeze sha + UTC + key reference + pre-freeze
confirmations). §§1–8 immutable from that timestamp.

Sequence step 3: **1a pilot is running now** under the s22-pinned recipe
(3,003 candidates, n=20 search / top-50 n=50 confirm on disjoint passes,
cell-derived seeds). Two-stage validation (full n=50 reference vs
two-stage; acceptance regret ≤0.02 on ≥95% + argmax ≥90%) and the 2%
bit-identical determinism check run with it. Green/red per s26: both
pass ⇒ 1b/1c + audits proceed; either fails ⇒ n_search escalation
20→25→50, then STOP and report.

Build-time disclosures (queued from the labeler build, pre-freeze, no
§§1–8 impact): (i) the creep grid's top value is 3.9 (1.5:0.2:4.0 ⇒ 13
values) — consistent with the pinned 3,003-candidate count; (ii) the
full-inventory severity-axis table for 1b/1c follows the preset-default
ranges for components §3 does not name (the zero-judgment reading;
nominal contributes a single no-fault cell) — flagged for ratification
in the pilot report; (iii) full Stage 1 measures ~55 min at 1,560 eps/s
(width 3,003), not the plan's 24 min at width 2,250 — compute only, no
design impact.

— kimi (arm owner, execution)
