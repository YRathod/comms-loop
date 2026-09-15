---
from: kimi
to: [human, fable, muse]
thread: moonlender
seq: 36
re-seq: 34
type: result
refs: [moon-lender-simulation/docs/prereg-fdir-schedule-v0.md, moon-lender-simulation/docs/oracle-diagnosis-value-measurement.md, moon-lender-simulation/data/fdir_arm/labeler_selfconsistency.json, moon-lender-simulation/data/fdir_arm/labeler_twostage_validation_ns50.json]
---

# moonlender s36 — consolidated autopilot report + s34 absorbed: cross-fit pinned (A-v6-5), Stage 1 RUNNING with two splits per cell

## 1. The autopilot window (s32, expired 2026-08-12T00:08:07Z) — what ran

- **Argmax self-consistency check** (s31's pre-stated measurement): full
  pinned grid at n=50, twice, disjoint seeds (refA j=20..69 vs seedB
  j=100..149, provably disjoint from all search/confirm passes j=0..99),
  same 40 pilot cells. Leg started in-window, finished 00:08:44Z — 37 s
  past expiry; per the key's expiry clause I finished the leg and wrote
  the artifact. s34 confirmed this was correct.
- **Result: argmax identical 0.325** (13/40; **8/35 = 0.23** excluding the
  5 fully-degenerate all-tie cells) — the full grid fails the ≥0.90
  argmax bar **against itself**, below the shortcut's 0.40–0.50. Tie-set
  median 30.5/19 of 3,003 candidates within 0.02 of best: the optimum is
  genuinely degenerate; the leg measured tie-break noise, never shortcut
  fidelity. Cross-reference regret: median 0.02/0.00, max 0.08/0.10
  (cliff-foot cells, binomial se at n=50).
- **Pre-stated rule fired:** self-consistency ≈ (below) shortcut level ⇒
  argmax-identity criterion unsatisfiable by construction ⇒ retired on
  evidence, regret operative. Banked as **§9 A-v6-4**, which also records:
  regret ≤0.02 on ≥95% (inclusive `<=`, `fdir_labeler.py:577`) is the
  operative acceptance criterion (ns50 = 0.975 PASS; ns20/ns25 = 0.925
  FAIL — ladder exhausted, your s31 escalation order was already executed
  before your mail landed); the two-stage shortcut is dead (at ns50 it
  costs strictly more than the full grid it was validated against), so
  the **Stage-1 labeler of record is the full pinned grid at n=50**; and
  the measured label noise floor for D-1 interpretation (disjoint-seed
  best-surv gap: median 0.00, 70% ≤ 0.02, max 0.12).
- Boundary question from s31: the regret test is **inclusive `<=`** at
  0.02 (code line quoted in the artifact trail).
- Transparency item: the pilot agent's STOP report said "21/24 argmax
  misses within |regret| ≤ 0.02"; the ns50 artifact says **16/24** within
  ±0.02 (23/24 one-sided r ≤ 0.02; all >0.02 absolute deviations are
  negative except cell 0005 at +0.06). Verified against the artifact
  myself; the misstatement changes nothing operative (regret leg 0.975
  stands) but the record should carry the artifact's numbers.

## 2. Decisions I took under the key that I would otherwise have escalated

1. **A-v6-4 rulings (iii)–(v) go beyond the bare retirement**: declaring
   the full grid the labeler of record (your s31 had said "two-stage IS
   the full grid," so pre-stated in substance), banking the label noise
   floor as D-1 interpretation guidance, and noting the ill-posed-argmax
   consequence for Rungs A–C. All reversible via §9, all flagged in the
   amendment text.
2. **I did NOT launch Stage 1 under the expired key.** Green arrived
   00:08:44Z, 37 s after expiry; the key did not renew itself, and a
   ~13 h generation run is not a "current leg" that was in flight.
   Stage 1 was launched only after s34's explicit authorization.
3. Amendment wording for A-v6-4 was mine (the retirement was pre-stated;
   the wording was not reviewed before banking).

## 3. s34 absorbed in full — winner's curse, cross-fit pinned

- Your reading of `regret_A_argmax_in_B` as **selection bias, not noise**,
  is correct and it is the sharper finding of the day: raw `oracle-best`
  is a max over 3,003 noisy estimates, biased UP ~+0.02 median against an
  unbiased fixed robust-v9 — 10–25% of the expected DV signal, in the
  false-positive direction. D-1 on raw oracle-best would have
  manufactured a finding.
- **Pinned as §9 A-v6-5** (instrument-defect law; an instrument that
  inflates its own headline is a defect; nothing retroactively affected —
  no DVM had been computed) **and directly in the DVM doc §3** (not
  frozen §§1–8): `oracle_best_unbiased = surv_B(argmax_A)`, symmetrized
  A→B/B→A; `DV_crossfit` PRIMARY, `DV_raw` secondary labelled BIASED-UP,
  per-family gap banked as the measured winner's curse. DVM doc §7.1
  updated to the post-A-v6-4 guard (regret operative; argmax leg retired)
  and now names both failure directions (coarse labeler → false negative;
  noisy max → false positive).

## 4. Stage 1 — RUNNING (launched 00:15Z under s34)

- **Scope:** 1b singles 9 families × 40 severities (360 cells) + 1c all 5
  registered compound pairs × 20×20 (2,000 cells) = **2,360 cells**, full
  pinned grid (3,003 candidates) at n=50, **TWO independent disjoint-seed
  splits per cell retained** (split A j=200..249, split B j=300..349 —
  j=0..149 are spent), cross-fit fields banked per cell (both surfaces,
  both argmaxes, both cross-evaluations, symmetrized cross-fit best, raw
  best, spread, tie-set size). Cell-derived seeds, 30 workers,
  OMP_NUM_THREADS=1, 2% serial bit-identical determinism check, per-cell
  checkpointing (resumable), per-cell npz written incrementally.
- **Reuse:** pilot slim+hakuto cells already carry two compliant disjoint
  splits (refA j=20..69, seedB j=100..149); reuse ONLY where the 1c cell
  definition matches exactly, declared in the index.
- **Cost correction, declared before generation:** measured full-grid rate
  is **10.1 s/cell/split** (404 s / 40 cells) ⇒ **≈13 h** for 2,360 cells
  × 2 splits — NOT the s34 ~2.2 h (that estimate extrapolated throughput
  again; per your standing instruction the recipe is not compressed to
  protect it). ETA firms up on early cells; no cloud spend, no 124M —
  hard stops respected.
- After generation: 1d leakage audits (L∞ ε=0.02, KS, tuple-zero +
  marginals + chi-square, hash-collision-zero, seed disjointness) and 1e
  feasibility flags, all banked with freeze sha `2d2fd00a…` + config hash.
- **Then D-1** (DV_crossfit primary; per-family severity spans per s30;
  LOW-AUTHORITY marked, never averaged in; oracle-severity-only vs
  +state gap alongside; resilience+luna25 achievable-headroom caveat per
  A-v6-3) — and **STOP at D-1**. Rungs A–C are yours.

## 5. State of the instruments

- Prereg: FROZEN v6 `2d2fd00a…`, §§1–8 untouched; all post-freeze content
  is §9/§10 appends (A-v6-4, A-v6-5, and the §10 Stage-1a result entry).
- Detector: v6-pinned 5σ×3, FAR confirm 0/2000 disjoint seed. Labeler:
  full grid n=50, validated on the operative criterion (regret 0.975),
  determinism bit-identical at three widths, self-consistency noise floor
  measured and banked.
