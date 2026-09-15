---
from: human
to: [kimi, muse, fable]
thread: moonlender
seq: 21
re-seq: 20
type: handover
refs: [moon-lender-simulation/docs/fdir-arm-execution-plan.md, moon-lender-simulation/docs/prereg-fdir-schedule-v0.md]
---

# moonlender s21 — END-TO-END EXECUTION PLAN, costed per leg. kimi owns execution. One BLOCKER must be resolved before freeze.

Plan: `docs/fdir-arm-execution-plan.md`. Governs prereg **v5**, sha256
`32bd49beb24f92d4320eb3fd8da8055a16d9c666b22807f11c534c363c967130`
(31,353 bytes). **Status: PROSPECTIVE — no datum, §§1–8 NOT frozen.**

kimi: you own this end to end, subject to the stop conditions below.

## BLOCKER — resolve BEFORE freeze, do not start Stage 1 without it

**The pinned labeler is computationally infeasible as literally written.**
§3 pins grid `sprint` step 1.0 × `creep` step 0.2 × `creep_start` step 50
= **3,003 candidates**, "then local refine with n=50 rollouts/candidate."
If n=50 applies to the full grid that is **150,150 eps/cell = 4.6 min/cell**
at the measured 544 eps/s:

- singles only (360 cells) → **27.6 hours**
- singles + five 2-D compound surfaces (2,360 cells) → **180.9 hours**

Recommended resolution **(A)**: coarse grid 3×3×5 = 45 candidates at n=50,
then ~20 local-refine candidates at n=50 → **6.0 s/cell**, total
**3.9 hours**, landing on the same pinned grid steps. Alternative **(B)**:
full grid searched at n=10, top-25 confirmed at n=50 → 37 h.

Either is defensible; **leaving it ambiguous is not.** Pin it as a §9 line
before freeze. Whichever you choose, the labeler's own breakpoint
distribution must still be banked — the v5 activation test baselines
against it.

## DESIGN DEPENDENCY — do not miss this or Stage 1 gets paid twice

Rung B trains **telemetry → severity**. Its inputs only exist if Stage 1
**retains per-episode telemetry tensors up to `t_dec`**. Label-only logging
forces a complete Stage-1 re-run. Enable telemetry capture in Stage 1.

## Costed stages (measured rates: 544 eps/s controller; ~17–20k env-steps/s PPO)

| stage | compute | kill point |
|---|---|---|
| 0 pre-flight + freeze (robust-v9 as code+hash, seeded draws, detector, FAR gate) | **< 1 min** | FAR > 0.01 ⇒ re-pin before data |
| 1 label generation (1-D pilot → singles → 2-D compound surfaces) | **~4 h** | pilot 1a (4 min) can end it early |
| 2 Rung A smoothness (RBF/ReLU/SiLU, select vs eval split, both oracle refs) | ~10 min | **<0.50 × ceiling ⇒ ARM DIES** |
| 3 Rung B extraction | ~30 min | **<0.50 retained ⇒ STOP** |
| 4 Rung C end-to-end (7 controls, n=300, ≥3 seeds, PVSG if prior-violating) | ~1.5 h | P3/P4/P6 verdicts |
| **total** | **~6 h compute, ~18 h wall, $0 cloud** | 3 independent kills |

Expected cost is far below the total — Stage 1's pilot or Stage 2 can end
the arm inside the first hour. Run **1a first and stop** before committing
to the 3.3 h surface.

## Your authority, and where it stops

**You may, without coming back:** run Stages 0–4 as costed, on local
CPU/GPU; resolve the labeler BLOCKER by §9 line (state which option and
why); halt on any pinned KILL and report; fix instrument defects you find,
disclosed per the instrument-defect law.

**STOP and return to the human for:**
1. **Any cloud spend, and any escalation to 124M.** The size ladder permits
   escalation ONLY on a failed gate at a smaller rung, never by preference,
   and it needs a **fresh rule-9 key**. "Solved by a 30k-parameter
   regressor" is a preferred outcome, not a shortfall.
2. **Any change to §§1–8 after freeze** — that is an amendment, dated, with
   affected numbers marked INSTRUMENT-SUSPECT.
3. **Any prior-violating PASS** — PVSG battery first, and the proposer does
   not grade its own reversal.
4. **A P3 pass with a P4 or P6 fail** — that is reported UNSAFE, and the
   headline sentence must say so. Do not soften it.

## Standing discipline (unchanged)

Per-seed, unsmoothed, never averaged. Search seed ≠ confirm seed. No
artifact retro-edits — corrections are regenerations. No seed-shopping: any
re-confirm you run reports whatever it says. Every artifact records `n`,
`seeds`, config hash. Mechanisms stay `(inference)` until a telemetry read
confirms them. **A cleanup edit is a content edit** — the human broke two
load-bearing pins during a de-duplication yesterday (§9 A-v5-0); every edit
round ends with a full pin-by-pin integrity check.

## Not in scope

R4 (1236 re-confirm) remains the human's call. The s8/s10 nav-latch
inference stays quarantined with its pinned ablation. GRU/asymmetric-critic
ladder, fourconnect closeout, PVSG backfill stay parked.

**Freeze happens at your Stage 0e, on the human's go — not before.**
