---
from: kimi
to: [human, fable, muse]
thread: moonlender
seq: 44
re-seq: 43
type: result
refs: [moon-lender-simulation/data/fdir_arm/control56_gap.json, moon-lender-simulation/data/fdir_arm/final_d1.md]
---

# moonlender s44 — STATE AT WINDOW EXPIRY (s40 key expired 20:30:56Z). LEG 3 complete: the diagnosis value is fault KNOWLEDGE, not state conditioning. Rung A + results doc + muse verification + BANK NOT done — fresh key needed.

## LEG 3 result (banked 16:19Z, in-window) — control-5 vs control-6 gap

Paired rollout evaluation (RBF ridge both controls, per-episode oracle
labels, n_eval 500–10,000 per family, McNemar paired test):

| family | c5 (severity-only) | c6 (+state) | gap | z |
|---|---|---|---|---|
| hakuto_r | 0.734 | 0.733 | −0.001 | −0.10 |
| slim | 0.790 | 0.794 | +0.004 | +0.53 |
| im1 | 0.537 | 0.528 | −0.009 | −0.83 |
| im2 | 0.817 | 0.814 | −0.004 | −0.21 |
| resilience | 0.866 | 0.874 | +0.008 | +1.03 |
| slim+im2 | 0.276 | 0.284 | +0.008 | +1.30 |
| beresheet+hakuto | 0.546 | 0.549 | +0.004 | +1.43 |
| im1+vikram | 0.468 | 0.481 | **+0.013** | **+3.81** |
| slim+hakuto | 0.483 | 0.478 | −0.005 | −1.71 |

**Reading: the severity vector carries essentially all the
schedule-relevant information the oracle labels express.** The one
significant gap (im1+vikram +0.013) is at the label-noise scale
(A-v6-4 floor ~0.02). The D-1 headline (+0.19 singles / +0.34–0.73
compounds) is attributable to **fault knowledge**, not initial-state
conditioning — muse's R-A question answered in the direction that keeps
the DVM meaningful. muse: independent recompute still owed per s40 §4.

## State at expiry — honest accounting

DONE in-window: Stage 1 (2,360 cells, 2 splits, determinism 47/47, audits
clean), degeneracy diagnostic, FINAL D-1 (verified twice: by me, muse
pending), control-5/6 gap.

**NOT done: Rung A, `docs/dvm-results.md`, muse verification, BANK.**
Cause, plainly: my brief to the analysis agent ended at LEG 3 (STOP per
its scope); its completion notification reached my session only at
23:39Z — the session was suspended ~16:20Z–23:39Z, and ~4.2 h of window
(16:19→20:30Z) went unused. That is a scheduling loss owned by me, not a
blocking defect. No leg was in flight at expiry; nothing was abandoned
mid-write; all banked artifacts are complete and consistent.

## Decisions taken under the key that I would otherwise have escalated

1. **LEG-3 target construction (agent's declared choice, mine to own):**
   banked Stage-1 labels are per-cell means and cannot supervise state
   conditioning, so per-EPISODE oracle labels were generated as new
   compute (1,691 cells × 25 fresh passes, j=400..424, disjoint); the
   per-episode label is the surviving candidate nearest the robust-v9
   default under the pinned tie-break; zero-survivor episodes excluded
   from the fit (counted per family in the artifact).
2. **Regressor family:** RBF ridge for both controls (§6 "plain
   regressor" branch), closed-form/deterministic; the prereg left the
   family unpinned for these controls — simplest option chosen, declared.
3. **Conservative exclusion:** split-disagree LOW-AUTHORITY cells excluded
   from all D-1 aggregates (they are listed, never hidden).
4. **Rung A not started in-window** although authorized — the correct
   call once the session resumed post-expiry was to stop rather than
   start it on an expired key.

## What a fresh key would authorize (in order)

Rung A (RBF/MLP-ReLU/MLP-SiLU; select on H-interior-select, gate on
H-interior-eval; binomial breakpoint test; **exclude H-interior
near-boundary points** per the 1d audit note) → `docs/dvm-results.md`
(ceiling language; all limitations incl. blocked Rungs B/C) → muse
independent recompute + critique → BANK. All inputs are banked; Rung A
is the only compute leg left (~1 h class), everything else is writing
and verification.
