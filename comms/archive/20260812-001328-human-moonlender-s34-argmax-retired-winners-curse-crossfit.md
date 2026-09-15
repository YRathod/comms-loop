---
from: human
to: [kimi, muse, fable]
thread: moonlender
seq: 34
re-seq: 33
type: key
refs: [moon-lender-simulation/data/fdir_arm/labeler_selfconsistency.json, moon-lender-simulation/docs/oracle-diagnosis-value-measurement.md]
---

# moonlender s34 — argmax criterion RETIRED on evidence. But the same artifact exposes a WINNER'S-CURSE bias in oracle-best that would have manufactured a false POSITIVE in D-1. Cross-fit estimator pinned before any curve is computed.

Autopilot window closed 00:08:07Z; your self-consistency artifact is stamped
00:08:44Z. Leg finished, artifact written — correct behaviour at expiry.

## 1. Argmax criterion: RETIRED, on evidence, per the pre-stated rule

Two INDEPENDENT full grids at n=50 agree on argmax **0.325** of the time —
**lower than the shortcut's 0.40–0.50.** The ≥90% bar was unsatisfiable by
construction: the full grid cannot pass it against itself. It measured
tie-breaking noise, never shortcut fidelity. Retired, with 0.325 banked as
the justification. **Regret is now the operative criterion.** The rule was
pre-stated in s31 and the measurement decided it — no goalpost was moved.

Confirmed quantitatively: **median tie-set size 30** candidates within 0.02
of best (max 3003, a dead cell). The optimum is genuinely degenerate.

## 2. Escalation outcome

| n_search | regret ≤0.02 | verdict on the operative criterion |
|---|---|---|
| 20 | 0.925 | FAIL |
| 25 | 0.925 | FAIL |
| **50** | **0.975** | **PASS** |

So regret passes only at `n_search=50` — which is the full grid. **The
two-stage shortcut is dead: it never bought anything that survived
validation.** Stage 1 runs the full pinned grid at ~2.2 h. Take the 2.2 h.

## 3. THE FINDING — oracle-best is biased UP, and it would have faked a positive D-1

Your own artifact contains it: **`regret_A_argmax_in_B` median 0.0200, max
0.0800.** A's chosen best scores **0.02 lower when re-rolled on fresh
seeds**. That gap is not noise around the truth — **it is selection bias.**

`oracle-best` is a **maximum over 3,003 noisy estimates** (se ≈ 0.071 per
candidate at n=50). Taking a max over noisy estimates is biased upward —
the winner's curse. `robust-v9` is a **fixed** schedule with **no selection
step**, so it carries no such bias.

```
DV = surv(oracle-best)   −   surv(robust-v9)
        biased UP ~0.02        unbiased
```

Expected DV signal is 0.08–0.2. **A +0.02 median inflation is 10–25% of the
signal, in the direction of manufacturing a false POSITIVE.** I spent s27
warning that a coarse labeler could manufacture a false negative. The real
exposure runs the other way, and it is larger.

**Had D-1 been computed from raw `oracle-best`, its headline number would
have been inflated by construction — and it would have looked like a
finding.**

## 4. PINNED before any curve is computed: cross-fit oracle-best

```
oracle_best_unbiased(cell) = surv_B( argmax_A(cell) )
```

Choose the schedule on split A, **score it on independent split B**. This is
the standard fix and **you have already computed exactly this quantity** —
`regret_A_argmax_in_B` is its complement. Report:

- **`DV_crossfit`** (primary) using the cross-fit oracle-best;
- **`DV_raw`** (secondary, labelled BIASED-UP) using the naive max;
- **the gap between them**, per family — that gap *is* the measured winner's
  curse and is worth banking in its own right.

Symmetrize (A→B and B→A, average) since you have both directions.

**Disposition:** the DVM doc is not part of the frozen §§1–8, so this pins
there directly. To the extent it touches controls 5/6, file it as a §9
amendment under the instrument-defect law — **an instrument that inflates
its own headline is a defect.** Nothing is retroactively affected: **no DVM
has been computed yet.** This is the whole reason D-1 was placed behind a
stop.

## 5. Next

1. Pin the cross-fit estimator; amend §9; disclose.
2. Stage 1 = full pinned grid, ~2.2 h, cell-derived seeds, `OMP_NUM_THREADS=1`,
   2% determinism check. **Retain both splits per cell** — cross-fitting
   needs them, and regenerating later would cost the full 2.2 h again.
3. D-1 with `DV_crossfit` primary, `DV_raw` secondary, per-family severity
   spans (s30), LOW-AUTHORITY cells marked.
4. **STOP at D-1.** Autopilot has expired and does not renew itself. Report;
   the model-arm decision is mine.

Also owed: the consolidated autopilot report, including **any decision you
took under the key that you would otherwise have escalated**.
