---
from: kimi
to: [human, fable, muse]
thread: moonlender
seq: 42
re-seq: 41
type: result
refs: [moon-lender-simulation/data/fdir_arm/labels_stage1/labels_stage1_index.json, moon-lender-simulation/data/fdir_arm/labels_stage1/labeler_determinism_1c.json, moon-lender-simulation/data/fdir_arm/labels_stage1/labeler_leakage_audit.json, moon-lender-simulation/data/fdir_arm/labels_stage1/labeler_feasibility.json]
---

# moonlender s42 — MILESTONE per s40 §6: Stage 1 COMPLETE, verified. 2,360/2,360 cells, determinism PASS 47/47 bit-identical, audits clean. Analysis legs now running.

## Stage-1 completion (resume leg)

- Resumed 10:42Z, completed ~12:10Z: the remaining 340 cells (all
  `slim+hakuto` — the family in flight at the reboot) in 1.36 h.
- **No-rewrite confirmation (s40 §0):** exactly 340 npz carry post-reboot
  mtimes, all slimplushakuto; the 2,020 pre-reboot cells are untouched
  (last pre-reboot write 07:28Z). Checkpoint contract held end to end.
- **Determinism (2% serial, both splits): PASS** — 7/7 (1b) + 40/40 (1c)
  BIT-IDENTICAL surfaces + scalars (`labeler_determinism_1b/1c.json`).
- **1d leakage audits clean:** seed disjointness proven (j=0..149 spent by
  1a/references; Stage-1 splits j=200..249/300..349; telemetry a distinct
  KDF domain); dedup 156,000 train + 80,600 test IC hashes, **0
  collisions**; H-pairs tuple-zero + marginals present + chi-square
  computed (the resilience+luna25 chi-square entry states the
  no-correspondence fact explicitly, as pre-declared); H-interior audit
  shows min-gap 0.0 with the pinned "not an interpolation claim" note —
  **Rung A must exclude or drop near-boundary points**, carried into the
  Rung-A plan.
- **1e feasibility:** 520 infeasible (80 singles incl. deep-thrust-loss
  cells, 440 compound), 636 LOW-AUTHORITY — all marked per cell, never
  averaged.

## Now running (same window)

Three legs on the completed set, per s40: (1) **degeneracy diagnostic**
(banked-data, free — variance of crossfit_oracle_best along each grid
axis per family; inert axes declared, not argued); (2) **FINAL D-1**
(interim method extended to all 2,360 cells; robust-v9 1c bars measured
by the same ratified paired-reference instrument, new disjoint files);
(3) **control-5 vs control-6 gap** (authorized rollouts, disjoint pass
domain j=400..449 or named KDF domain — j=0..349 spent). Then Rung A per
pin, then `docs/dvm-results.md` to muse.

Correction of record from my side: the interim-D-1 agent id changed
(agent-13 now runs; agent-12's instance did not survive the reboot) —
the brief to agent-13 carried the full pins verbatim; nothing about the
instruments changed.
