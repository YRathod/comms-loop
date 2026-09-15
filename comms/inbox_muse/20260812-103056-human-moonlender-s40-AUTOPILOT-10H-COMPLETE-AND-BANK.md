---
from: human
to: [kimi, muse, fable]
thread: moonlender
seq: 40
re-seq: 39
type: key
refs: [moon-lender-simulation/docs/oracle-diagnosis-value-measurement.md, moon-lender-simulation/docs/prereg-fdir-schedule-v0.md, moon-lender-simulation/data/fdir_arm/interim_d1_singles.json]
---

# moonlender s40 — 10-HOUR AUTOPILOT. Complete the arm and BANK THE RESULT. All open s39 items adjudicated below. Expires 2026-08-12T20:30:56Z.

Human direction: *"KIMI & muse is LIVE, I authorize for auto pilot for next
10 hours, complete this project and bank a result. decide any thing by your
self and assign task to kimi & muse."* Decisions taken on that authority are
recorded here so they are auditable, not implicit.

## 0. STATE — Stage 1 is STOPPED, resume first

Last cell written `slimplushakuto__0059` at **07:28:02Z**; **2,020/2,360**;
zero writes for ~3 h. The monitoring loop stopped at the same moment, so this
reads as a **machine suspend, not a labeler fault**. The labeler is
per-cell-checkpointed and restart skips existing cells.

**Action: RESUME, do not restart.** Report the resume point and confirm no
completed cell was rewritten. 340 cells remain (~75 min).

## 1. ADJUDICATED — the three open s39 items

**(a) robust-v9 bar — RATIFIED AS BUILT.** Your dedicated paired reference
rollout measures the *actual pinned baseline*; a grid neighbour would measure
an approximation of it. Yours is the more correct instrument. **No
regeneration.** Record that `(15.0, 2.0, 650.0)` is off-grid as a permanent
note so nobody "fixes" it later.

**(b) `oracle-severity+state` gap — AUTHORIZED, run it.** This is muse's R-A
point and it is load-bearing: without it, the +0.19 cannot be attributed to
*fault knowledge* rather than *initial-state conditioning*. Fit control-6
(true severities ∪ `(y0,x0,vx0,vy0,fuel0,nav_init_bias_y)`) and control-5
(severity-only), same regressor family, evaluate by rollout, and **bank the
gap per family**. If the gap is large, the headline is state-conditioning,
not diagnosis — and we must say so.

**(c) 1c grid interpretation — KEEP AS BUILT, but MEASURE whether it
mattered.** Do NOT regenerate 1,600 cells to test an interpretation. Instead
run a **degeneracy diagnostic** on banked data (free): per family, compute
the variance of `crossfit_oracle_best` **along the pinned-activator axis**.
- variance ≈ 0 ⇒ the second axis is **inert**; report that family's surface
  as effectively 1-D, with the inert axis declared. That converts an
  unresolved interpretation into a measured fact.
- variance material ⇒ the axis is live and the pinned activator was benign.
Either way it is reported, never quietly averaged.

**(d) `resilience+luna25` — apply the s25 achievable-headroom rule.** Once
labelled, if `oracle-best − robust-v9 < 0.05`, it is **excluded from the P3
primary set** and reported as **arena evidence** (candidate region-(c):
a compound no schedule can recover). That exclusion is itself a finding —
bank it as one.

## 2. RUNG B/C ARE BLOCKED — a finding, not a failure

I verified the Stage-1 npz: keys are `surface_A/B, argmax_A/B, raw_best_A/B,
surv_B_at_argmax_A, surv_A_at_argmax_B, crossfit_oracle_best, spread, tie`.
**No telemetry tensors were retained.** The execution plan's DESIGN
DEPENDENCY was not honoured, so **Rung B (telemetry→severity) cannot run
without regenerating all 2,360 cells (~13 h).**

**Decision: do NOT regenerate. Rungs B and C do not run in this window.**
Record it plainly in the results doc: *the model arm is blocked on an input
that was not captured; the model-independent measurement is unaffected.*

## 3. THE DELIVERABLE — what "bank a result" means

**The banked result is the DVM**, not the model arm.

1. Finish Stage 1 → determinism check (2%, serial, bit-identical) → 1d
   leakage audits → 1e feasibility flags.
2. **FINAL D-1**: `DV_crossfit` PRIMARY, `DV_raw` labelled BIASED-UP,
   winner's-curse gap per family, per-family severity **spans**,
   LOW-AUTHORITY marked and never averaged, control-5 vs control-6 gap,
   degeneracy diagnostic, achievable-headroom exclusions.
3. **RUNG A is authorized** (it needs only clean severities → schedule, which
   we have): RBF / MLP-ReLU / MLP-SiLU, select on `H-interior-select`, gate
   on `H-interior-eval`, binomial breakpoint test, profile banked-not-gated.
   It is a real kill point — report the verdict either way.
4. **Results document** (`docs/dvm-results.md`): the curve, the method, the
   honest framing. **Ceiling language is mandatory** — a positive DV is an
   upper bound, not achievable performance. State the prior we recorded
   (expected ~0) and that it was **rejected for nav-deception families only**.
   Carry every limitation: singles vs compounds, LOW-AUTHORITY exclusions,
   inert axes, blocked Rungs B/C, single sim, no real telemetry.

## 4. TASK SPLIT

**kimi (execution):** resume Stage 1 → audits → control-5/6 → degeneracy
diagnostic → final D-1 → Rung A → draft `docs/dvm-results.md`.

**muse (independent verification — the proposer does not grade its own
result):** recompute the final D-1 **from the raw npz**, independently of
kimi's pipeline, and confirm or refute every headline number. Then
adversarially critique the results doc: overclaims, missing limitations,
ceiling language, any figure not recomputable from a named artifact. **Your
verdict gates the bank.** If you and kimi disagree on a number, the artifact
wins and both readings are recorded.

## 5. STANDING STOPS — still binding

- **No cloud spend. No 124M.** Local only. If either becomes necessary,
  STOP and report — that needs a fresh key from me regardless of this window.
- **§§1–8 stay frozen** (`2d2fd00a…`); post-freeze changes are dated §9
  amendments with affected numbers marked INSTRUMENT-SUSPECT.
- **Instrument defect ⇒ disclose and stop.** The 0d gate is the precedent: a
  gate firing is the good outcome.
- **PVSG battery** on any prior-violating PASS.
- Per-seed unsmoothed, search ≠ confirm seeds, no artifact retro-edits, no
  seed-shopping, n/seeds/config-hash in every artifact.

## 6. REPORTING

Report at: Stage-1 complete → final D-1 → Rung A verdict → results doc ready
for muse → muse verdict → BANKED. And at the end, **list every decision you
took under this key that you would otherwise have escalated.**

If the window expires mid-leg: finish the leg, write the artifact, report
state. **This key does not renew itself.**
