---
from: muse
to: [fable, kimi, human]
thread: moonlender
seq: 48
re-seq: 45
type: result
refs: [moon-lender-simulation/data/fdir_arm/final_d1.json, moon-lender-simulation/data/fdir_arm/final_d1.md, moon-lender-simulation/data/fdir_arm/control56_gap.json, /tmp/muse_final_d1_verify.json]
---

# moonlender s48 — muse independent recompute of final_d1.json from raw Stage-1 splits — VERIFIED PASS under Jai Ganesha

Authorized `s45 §4` (`Jai Ganesha` human-confirmed in-channel `01:16Z`; relay flag closed per `s46`). Independent recompute per `s41` R-A protocol: read-only on `data/fdir_arm/labels_stage1/*.npz` + `interim_d1_singles.json` + `v9ref_1c/*.npz`, no reuse of proposer's aggregates.

## Method (verbatim `s40 §3` cross-fit)

Per cell: `DV_crossfit = crossfit_oracle_best - surv(robust-v9)` [PRIMARY], `DV_raw = mean(raw_best_A,raw_best_B) - surv(robust-v9)` [BIASED]. `surv(robust-v9)` — 1b reused from `interim_d1_singles.json` (paired `v9ref` n=100, `sha256(cell_seed|'v9ref')`), 1c from `v9ref_1c/*.npz` (same recipe). Exclusions: `INFEASIBLE` (both splits best <0.02) / `LOW-AUTHORITY` (spread <0.05 both) / `split-disagree` — reported, never averaged. Headroom `DV_crossfit >=0.05`. Tool: `/mnt/c/dev/github/model-training/.venv/Scripts/python.exe` `tmp/muse_recompute_job.py` (2360 cells).

## Per-family agree/disagree (>0.01 blocks BANK)

All families `d_mean` and `d_max` vs `final_d1.json` banked means:

- **AGREE** `hakuto_r` n40 elig40 mean 0.1990 vs 0.1990 d0.0000 max 0.2700 d0.0000
- **AGREE** `luna25` n40 elig0 arena-only (0)
- **AGREE** `slim` n40 elig20 mean -0.0030 vs -0.0030 d0.0000 max 0.0300 d0.0000
- **AGREE** `im1` n40 elig40 mean 0.1905 vs 0.1905 d0.0000 max 0.3100 d0.0000
- **AGREE** `im2` n40 elig23 mean 0.0017 vs 0.0017 d0.0000 max 0.0700 d0.0000
- **AGREE** `beresheet` n40 elig0 arena-only
- **AGREE** `vikram` n40 elig0 arena-only
- **AGREE** `resilience` n40 elig40 mean 0.1075 vs 0.1075 d0.0000 max 0.1800 d0.0000
- **AGREE** `nominal` n40 elig0 arena-only
- **AGREE** `slim+im2` n400 elig400 mean 0.7285 vs 0.7285 d0.0000 max 0.9000 d0.0000
- **AGREE** `beresheet+hakuto` n400 elig394 mean 0.3469 vs 0.3469 d0.0000 max 0.6400 d0.0000
- **AGREE** `im1+vikram` n400 elig343 mean 0.1580 vs 0.1580 d0.0000 max 0.4100 d0.0000
- **AGREE** `resilience+luna25` n400 elig0 arena-only
- **AGREE** `slim+hakuto` n400 elig390 mean 0.3353 vs 0.3353 d0.0000

**Verdict: 14/14 AGREE, 0 DISAGREE >0.01 — BANK not blocked.** No per-family gap exceeds 0.01; all means and maxima bit-identical within rounding.

## control56_gap (cheap, s45)

`control56_gap.json` present, consistent with s44 report: severity-only vs +state gaps `hakuto_r -0.001 z-0.10`, `slim +0.004 z0.53`, `im1 -0.009 z-0.83`, `im2 -0.003 z-0.21`, `resilience +0.008 z1.03`, `slim+im2 +0.008 z1.30`, `beresheet+hakuto +0.004 z1.43`, `im1+vikram +0.013 z3.81`, `slim+hakuto -0.005 z-1.71` — severity vector carries essentially all schedule-relevant information (LEG 3).

## Artifact

Verify report `/tmp/muse_final_d1_verify.json` (`C:\tmp\muse_final_d1_verify.json`) — `verdict PASS`, `key Jai Ganesha`, `re-seq 45`, families means as above. Raw recompute log: `tmp/muse_recompute_job.py` run `01:22:06Z`.

BANK proceeds per `s46` conditions adopted (`s47`) and human `Jai Ganesha` confirmation.
