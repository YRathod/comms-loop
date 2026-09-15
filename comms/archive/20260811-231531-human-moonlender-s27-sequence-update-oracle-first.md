---
from: human
to: [kimi, muse, fable]
thread: moonlender
seq: 27
re-seq: 26
type: key
refs: [moon-lender-simulation/docs/oracle-diagnosis-value-measurement.md, moon-lender-simulation/docs/prereg-fdir-schedule-v0.md, moon-lender-simulation/docs/fdir-arm-execution-plan.md]
---

# moonlender s27 — SEQUENCE UPDATE (amends s26, does NOT revoke it): oracle first, model second. New deliverable D-1 lands before Rung A.

s26's GO stands. This changes the **order and the primary deliverable**, not
the authorization. New doc: `docs/oracle-diagnosis-value-measurement.md`.

## What changed and why

The arm's publishable result was implicitly the model arm (Rungs A–C). That
is backwards. The **model-independent** measurement is the one neither
adjacent field publishes, and it is a **byproduct of Stage 1 you are already
generating**:

```
DV(cell) = surv(oracle-best schedule)  −  surv(robust-v9 fixed schedule)
```

Both terms come straight out of the labeler. `oracle-best` is its search
result; robust-v9 is one point in the same candidate space. **The
measurement is a subtraction on existing output — no additional rollouts.**

**It needs none of the machinery that can break:** no detector, no `t_dec`,
no NO-FAULT path, no telemetry capture, no training, no activation choice,
no select/eval split, no PVSG. Everything hard from the last five review
rounds serves the *model* arm. This cannot fail for an uninteresting reason.

**And it is a CEILING test, which is why it goes first.** `oracle-best` is
handed true severity for free and searches every candidate — unachievable by
any real system, therefore an upper bound on what perfect diagnosis could
ever buy.

- **`DV ≈ 0` ⇒ no diagnoser, however good, is worth building here. The model
  arm is dead before it starts** — and that is the result, not a failure.
- **`DV` large ⇒** the information exists and Rungs A–C have *earned* the
  right to ask whether a model can recover it.

One measurement licenses or kills everything downstream. That asymmetry is
the whole argument for reordering.

## Updated sequence

1. Fresh-seed FAR confirm → freeze v6 (**unchanged from s26**; the detector
   still gates the model arm even though DVM does not need it).
2. 1a pilot + two-stage validation + determinism check (**unchanged** — the
   labeler is DVM's only dependency, see integrity note below).
3. On green: 1b/1c as planned.
4. **NEW — D-1 deliverable, before Rung A:** emit the DVM curve.
   `DV` vs severity, **per family**, with `oracle-severity+state` alongside
   `severity-only` (their gap = how much value is state-conditioning rather
   than fault identity, muse R-A). Bank as
   `baselines/diagnosis_value_curve.json`. **Report the curve, not a
   verdict.**
5. **STOP after D-1 and report.** If `DV ≈ 0` across families, the honest
   action is to **stop the model arm and publish the DVM** — not to run
   Rungs A–C for completeness. That call is mine; bring me the curve.
6. Rungs A–C only after that decision.

If schedule pressure ever forces a choice, the **floor version** is a 1-D
severity sweep per family (~9 × 40 cells, **5–10 min**) and it is publishable
on its own.

## The one way this measurement can lie — guard unchanged

**The labeler is DVM's only dependency.** A coarse or jagged search
understates `oracle-best` and would **manufacture a false negative** — the
single failure mode. So the two-stage validation guard stays exactly as
pinned (regret ≤0.02 on ≥95% of pilot cells, argmax identical ≥90%; escalate
`n_search` 20→25→50 on failure). Determinism check, cell-derived seeds,
`OMP_NUM_THREADS=1`, robust-v9 from committed code+hash: all unchanged.

**LOW-AUTHORITY cells must be marked, never averaged in.** Where
`oracle-best − oracle-worst < 0.05` the schedule has no authority (late-`t_dec`
slim-single geometry), so those cells carry no diagnosis value *by
construction* and would drag the curve toward zero for a reason that is not
the finding.

## Prior on record, before the run

The banked evidence points to a **small** `DV`: robust-v9 doubled
blind-family survivability from three hand-tuned knobs (`step1_b.json`), and
oracle *selection* over existing controllers bought only **+0.08** mean
(`oracle_selection_probe.json`). We expect a modest curve, plausibly ~0 on
several families. **Recorded now so a null cannot later be dressed up as a
surprise — and so a positive cannot be quietly re-framed as expected.**

Ceiling language is mandatory in any write-up: a positive `DV` is an upper
bound, not an achievable performance claim.

Standing stops from s26 unchanged.
