---
from: kimi
to: [human, fable, muse]
thread: moonlender
seq: 39
re-seq: 37
type: result
refs: [moon-lender-simulation/data/fdir_arm/interim_d1_singles.json, moon-lender-simulation/data/fdir_arm/interim_d1_singles.md]
---

# moonlender s39 — INTERIM D-1 (1b singles): diagnosis value is REAL and family-concentrated. +0.11…+0.20 on nav-deception families, ≈0 on actuation. 1c continues.

Per s37: 1b completed (~01:55Z, all 9 families × 40), interim D-1 computed,
banked, and **independently verified by me against the npz before this
mail** (per-cell cross-fit recomputed from raw splits — matches; family
means reproduced from the json rows — match; the robust-v9 grid claim
checked programmatically — holds). 1c continues untouched (~500/2,360
cells at banking time). Labelled **INTERIM — singles only, 1c pending;
1b determinism check pending at Stage-1 job completion**.

## The curve (DV_crossfit, PRIMARY; non-LOW-AUTHORITY cells only)

| family | severity span | n elig | mean DV_cf | max DV_cf @ sev | DV_raw (BIASED-UP) | winner's-curse gap |
|---|---|---|---|---|---|---|
| hakuto_r | alt_offset_mag [1000, 4500] | 40 | **+0.199** | +0.270 @ 3243.6 | +0.242 | 0.043 |
| im1 | t_dec-adjacent [60, 140] | 40 | **+0.190** | +0.310 @ 113.3 | +0.251 | 0.061 |
| resilience | dropout [20, 40] | 40 | **+0.107** | +0.180 @ 21.5 | +0.133 | 0.025 |
| slim | thrust_scale [0.30, 0.95] | 20* | −0.003 | +0.030 | +0.058 | 0.061 |
| im2 | [8, 15] | 23* | +0.002 | +0.070 | +0.103 | 0.101 |
| luna25 / beresheet / vikram / nominal | narrow preset bands | 0 | — (all LOW-AUTHORITY) | — | — | — |

\* eligible counts exclude 12 further cells where the two splits disagree
on the LOW-AUTHORITY flag (conservative exclusion; they are listed, never
averaged in). LOW-AUTHORITY total: 176 flagged + 12 split-disagree = 188
of 360 marked. The four all-LA families are exactly the mechanism v6/s25
named: time-triggered cutout, throttle floor, accel under-read, and
fault-free give the schedule no authority — their flat curves mean "the
schedule can't act on this fault", NOT "diagnosis is worthless", and the
narrow spans (s30) are reported alongside.

## Reading (ceiling language per DVM §7.6 — these are UPPER BOUNDS)

- **The null prior is rejected for the nav-deception families.** Perfect
  severity-knowledge buys +0.11…+0.20 mean survivability there (peaks
  +0.27/+0.31), every eligible cell above the ±0.02 label noise floor —
  vs the banked prior of +0.08 mean for oracle *selection*. The schedule
  space does carry recoverable diagnosis value.
- **It is family-concentrated.** Actuation faults (slim thrust, im2)
  show ≈0; four more families carry no schedule authority at all. A
  diagnoser is worth building *for the nav-deception class* — or the
  honest finding is that value lives in exactly one mechanism.
- **Winner's curse measured, not assumed:** gap 0.025–0.101 per family,
  consistent with the A-v6-4 estimate; raw would have overstated the
  headline by ~20–30% on hakuto_r/im1. The cross-fit pin earned its cost.

## s37 deviation — disclosed (guard caught a real error)

**robust-v9 (15.0, 2.0, 650.0) is NOT a grid point** — the creep grid
1.5:0.2:4.0 yields 1.9/2.1, never 2.0 (verified programmatically). My
brief had assumed it was readable off the candidate surface; wrong.
Workaround executed instead of bar-moving: surv(robust-v9) measured by a
**dedicated paired reference rollout** of the exact pinned profile, n=100
per cell (same cell seeds as the splits, env-seed domain
`sha256(cell_seed|"v9ref")`, disjoint from all integer passes). Grid
neighbors (15,1.9,650)=idx 1958 and (15,2.1,650)=idx 1979 banked per cell
as context. If you rule the bar should be a grid neighbor instead,
regeneration is ~8 min and 1c is unaffected (its npz are untouched by
this). **Flagging for your adjudication.**

## PENDING item

**oracle-severity-only vs +state gap:** not computable from banked data —
the npz retain per-candidate pass *means*, and the +state reference
(prereg §4 control 6) needs per-episode outcomes or the control-6
regressor + eval rollouts. Not improvised; exact cost reason recorded in
both artifacts. This is the one s37 requirement the interim does not
carry; it needs new compute and your go.

## Also disclosed (from the Stage-1 launch, unmailed until now per turn rule)

Agent-12's 1c interpretation, flagged for adjudication: the pinned
thrust_scale × alt_offset_mag grid is only physically live on both axes
for slim+hakuto; the other four merged presets lack `thrust_trigger_alt`
and/or `alt_offset_t`. It pinned the missing activators at the pilot's
sweep values (60.0 / 14.0) where absent — recorded per cell, each family
independently regenerable if you rule the literal reading (which yields
degenerate replicate surfaces on 3 of 5 families).

## State

1c running, ETA ~11–13 h from 00:26Z launch, per-cell checkpointed.
At job completion: 1b+1c determinism (serial, bit-identical), 1d leakage
audits, 1e feasibility — then final D-1, then STOP. Rungs A–C untouched.
