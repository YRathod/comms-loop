---
from: human
to: [kimi, muse, fable]
thread: moonlender
seq: 22
re-seq: 21
type: handover
refs: [moon-lender-simulation/docs/fdir-arm-execution-plan.md, moon-lender-simulation/docs/prereg-fdir-schedule-v0.md]
---

# moonlender s22 — s21 BLOCKER resolved with measurements, not compromises. Stage 1 target ~26 min at FULL pinned resolution. kimi owns the build.

The s21 blocker is closed and my own 4 h estimate is **withdrawn as
wrong**. It used 544 eps/s, which was measured on n=200 batteries — but the
labeler runs at the *candidate* vector width. Measured on this machine:

| vector width | eps/s |
|---|---|
| n=50 (one candidate, unbatched) | **338** |
| n=200 | 1,082 |
| n=1,000 | 2,769 |
| n=2,250 (candidates batched) | **4,058** |

Unbatched the labeler is **6.4 h** — worse than I told you. Three levers get
it to ~26 min **without coarsening anything**.

## Pinned technique (build to this)

**1. BATCH candidates into the vector dimension (~12×).** Make
`sprint / creep / creep_start` **per-env arrays** instead of scalars. The
profile is `np.where(y > creep_start, sprint, creep)` — it already
broadcasts. All 3,003 candidates fly in one vectorized call. Nothing about
what is computed changes.

**2. PARALLELIZE across cells (~25×; 32 cores ⇒ 30 workers).** Cells are
independent. **Three mandatory conditions — these are the integrity, not
the optimization:**
- **Seeds MUST be cell-derived, never stream-derived.** Each cell's seed is
  a deterministic function of its own severity vector (stable hash), NOT a
  running counter or shared RNG. Otherwise the label set changes with
  worker count and the artifact stops being recomputable — which would
  quietly void every downstream number.
- **`OMP_NUM_THREADS=1` per worker.** Stops BLAS oversubscription (slower)
  and removes multithreaded-reduction float drift.
- **Determinism check, required:** re-run a random **2% of cells serially,
  single worker**, require **bit-identical** labels. Bank
  `labeler_determinism.json`. Fails ⇒ the seed rule is wrong ⇒ STOP.

**3. TWO-STAGE search — VALIDATED, not assumed.** All **3,003 pinned
candidates at n=20**, then **top-50 confirmed at the pinned n=50**. Full
grid coverage preserved; only search-pass rollout noise is reduced; the
final label still comes from an n=50 confirm.

> **The integrity guard is the point of this whole message.** Do NOT assume
> two-stage ≡ full-grid. On the 40-cell 1-D pilot run **both** recipes —
> the full n=50 grid costs **1.0 min** parallel, so measuring is cheaper
> than arguing. **Acceptance: regret ≤ 0.02 survivability on ≥95% of pilot
> cells AND identical argmax on ≥90%.** Bank
> `labeler_twostage_validation.json`. **Fail ⇒ escalate n_search 20→25→50
> until it passes. Do not proceed on an unvalidated shortcut.**
> muse s19 warned a coarse labeler can make the map look jagged when it is
> the *labeler* that is jagged. This measures that instead of hoping — and
> if it fails at Rung A afterwards, we will know which one was jagged.

## Costed

| recipe | eps/cell | s/cell | 2,400 cells / 30 workers |
|---|---|---|---|
| full pinned grid n=50 | 150,150 | 37.0 | 58 min |
| **n=20 search + top-50 confirm (PINNED)** | **62,560** | **15.4** | **24 min** |
| n=15 + top-50 (fallback) | 47,545 | 11.7 | 18 min |

**Stage 1 ≈ 24 min + ~2 min validation ≈ 26 min.** Cell grid unchanged
(20×20), candidate coverage unchanged (all 3,003), final labels still n=50.
**Nothing was traded away to hit the target** — the speed came from
batching and cores, which change *how* the same work runs, not *what* is
computed. That distinction is the whole reason this is acceptable.

Whole-arm compute now ~45 min; wall stays dev-dominated (~18 h).

## Order of operations

1. Stage 0 (0a–0e) — robust-v9 as code+hash, seeded draws, detector, FAR
   gate. **KILL/RE-PIN if FAR > 0.01, before any generation.**
2. **1a pilot ONLY, then STOP and report** — pilot labels + two-stage
   validation + determinism check. Do not start 1b/1c until the validation
   artifact passes and I have seen it.
3. On green: 1b, 1c, audits.
4. Rung A. It is a real kill point — report the verdict, do not push past it.

## Unchanged authority

Local CPU/GPU only. **STOP and return for:** any cloud spend or 124M
escalation (fresh rule-9 key; only on a failed smaller-rung gate, never
preference), any post-freeze §§1–8 change, any prior-violating PASS (PVSG
first), any P3-pass-with-P4/P6-fail (reported UNSAFE, headline says so).
**Freeze at 0e on the human's go, not before.**

Also: cloud GPU was considered and rejected — Stage 1 is numpy/CPU so a GPU
would idle, porting the sim risks the instrument every banked number rests
on, and a different CPU/BLAS threatens exact recomputability. Cores, not
GPUs.
