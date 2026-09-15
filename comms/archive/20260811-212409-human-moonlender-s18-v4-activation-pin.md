---
from: human
to: [muse, kimi, fable]
thread: moonlender
seq: 18
re-seq: 17
type: review-request
refs: [moon-lender-simulation/docs/prereg-fdir-schedule-v0.md, moon-lender-simulation/baselines/step1_c.json]
---

# moonlender s18 — v4: activation pinned (ReLU vs SiLU) + falsifiable cliff-breakpoint prediction. Still PROSPECTIVE. Re-knife target is now v4.

One more unpinned degree found and closed before freeze — this one by the
human, not by review.

## The hole

§6 specified the Rung-A model as "RBF / ≤2-layer MLP" and **never fixed the
activation**. That is a live knob that would otherwise be chosen after
seeing Rung-A results: the R-E failure class, sitting in the artifact
through three review rounds.

## The pin (§3, v4)

- **Both ReLU and SiLU fitted at Rung A**, identical in every other respect
  (width, depth, init seed set, optimizer, epochs, early-stop, same labels).
  Neither is the designated default.
- **Selection rule pre-registered:** gate is evaluated with whichever scores
  higher on H-interior survivability-retained, averaged over ≥3 init seeds.
  **Ties (|Δ| < 0.02) resolve to ReLU** — fixed in advance so the tie-break
  cannot be picked later. Loser's numbers reported in full, never dropped.
- **Winner carries forward** to Rungs B/C; re-selecting activation at a
  later rung is barred as a post-hoc dial.

## Why this is not a generic architecture bake-off

The target carries a **measured cliff** (`step1_c.json`): survivability
0.01 → 0.12 → 0.47 → 0.73 across `thrust_scale` 0.46 → 0.58. ReLU is
piecewise-linear and can put breakpoints exactly at a kink; SiLU is smooth
and smears sharp transitions. **Smearing predicts survival on the DEAD side
of the cliff — precisely the false-confidence P4 gates on.** So the
activation can decide a SAFETY gate, not just an accuracy number.

**Pre-registered, falsifiable:** if ReLU wins, its first-layer breakpoints
must **cluster in 0.46–0.58 (≥40% of active breakpoints, vs ~18% expected
under uniform over [0.30,0.95])**, and `|∂schedule/∂severity|` must peak
there. **FALSIFIED IF ReLU wins with uniform breakpoints (<25% in band)** —
the cliff story would then be wrong and the advantage must be re-attributed
before being repeated anywhere.

## The profiler, and the anti-decoration rule attached to it

A weight-propagation profile is banked per model (breakpoint histogram,
dead/saturated fraction, per-layer activation mean/variance, Jacobian curve)
— but it is **BANKED, NOT GATED**. It exists solely to adjudicate the
prediction above. A profile that merely *describes* a network without
testing a stated prediction is decoration and does not enter the record.

**Prior stated in advance so a null cannot be retro-framed as a finding:**
on a smooth low-dimensional map both activations are expected to clear
Rung A, and **a null (|Δ| < 0.02) is the EXPECTED outcome.** This project's
own history is the reason for the caution — every real finding here came
from ablations and controls (order-flip, gloss-swap, nonce, no-model, the
crash-telemetry read), never from introspecting a network.

## What I want knifed

muse: your re-knife target is now **v4**, not v2. Specifically:
1. Is the 0.46–0.58 band the right one, given the labeler grids
   `creep_start` in steps of 50 and the cliff was located only to ±0.05?
2. Are **≥40% / <25%** defensible, or reverse-engineered to be passable?
   The uniform baseline ~18% assumes breakpoints spread over [0.30,0.95] —
   challenge that assumption directly.
3. Does fitting two activations and selecting on H-interior **contaminate**
   H-interior as an evaluation set? I believe not (selection is pre-declared
   and the same split gates both), but this is exactly the kind of
   selection-leak that looks fine and is not.
4. Everything in v3 you have not yet seen: 45 m deadline, branch (c),
   n=300, H-pairs ≤0.85 eligibility, P6 0.70/+0.30, and the two numbers
   still carrying no independent review — the 0.05 spurious-action bar and
   the corrected deadline.

Still PROSPECTIVE. No datum. Generation waits on your report and the
human's explicit go.
