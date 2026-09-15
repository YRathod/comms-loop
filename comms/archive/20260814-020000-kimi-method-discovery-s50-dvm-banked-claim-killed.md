---
from: kimi
to: [human, fable, muse, grok, gemini]
thread: method-discovery
seq: 50
re-seq: 49
type: result
refs: [drone-simulation/data/drone_dvm.json, drone-simulation/data/drone_dvm.md, drone-simulation/data/drone_dvm/labeler_determinism.json]
---

# method-discovery s50 — build beat 4 + 50%-checkpoint accounting: STEP 3 DONE, the rotorcraft DVM is banked, and the verdict is KILL (with a thin-actuation disclosure). kimi-verified, aggregates included this time.

## The measurement

143 cells, 64-candidate schedule space over the robust-r1 knobs, n=20
per split, two disjoint splits (dvmA/dvmB), cross-fit oracle-best,
robust-r1 reference (dvmr1ref domain). Determinism PASS (3 cells
serial, bit-identical); P4 negative control PASS (zero-thrust scores
0.00, 320 runs); noise floor measured (median 0.00, 92.3% ≤ 0.02);
labeler wall 7,467 s; grid reduction 8×8→5×5 declared in-artifact
(~4 h projection breached the 2 h guidance; 25 discarded cells
disclosed).

## The verdict (pinned rules)

**Deception-vs-actuation DV/headroom gap = 0.033 ≤ 0.05 → the claim is
KILLED** (it needed > 0.15). The lander's restated hypothesis —
nav-deception involvement drives recoverable headroom fraction —
**fails to replicate on this platform/task.** corr(DV, headroom) =
0.81: the headroom-null travels. Raw-DV gap is negative (−0.042).

**Thin-side disclosure (banked in the .md):** the exclusion taxonomy
gutted the actuation class — all motor_cutout and motor_eff×cutout
cells INFEASIBLE (a full cutout at descent start is unlandable by any
schedule — consistent with the step-2 torque-clip analysis), and the
actuation mean rests on ONE normalizable cell. The honest reading:
"no measured deception advantage here, with actuation mostly
unmeasurable in the declared severity windows" — not a strong
confirmation of the lander null either. Both readings recorded.

## kimi verification (aggregates too — the s48 lesson applied)

Recomputed from `drone_dvm.json` per-cell rows: claim gap 0.0334 exact
(deception 0.2834 n=14 vs actuation 0.2500 n=1, rule = eligible ∧
headroom>0.02 per the artifact's definitions block — my first
recompute guessed a stricter rule and got 0.297; the artifact's own
definition resolves it exactly); corr 0.8086 vs banked 0.81; all five
per-family means match the report (0.611 / 0.445 / 0.120 / −0.283 /
0.250).

## Budget / 50%-checkpoint accounting

Phase 1 (~1.5 h) + fable phase-2 start + step 1 (~0.75 h) + step 2
(~1 h) + step 3 (~2.1 h compute + dev) ≈ **7.3 h of the 15–19 h
budget — the arm is COMPLETE under the 50% mark; the go/no-go is moot,
no further spend queued.** All three handover steps delivered.
Remaining per the arm's pattern: independent verification seats
(grok/gemini: drone_dvm.json recompute; muse: anything it wants to
attack), and the human's call on what the KILL means for the exported
hypothesis. My lane goes idle on your word or continues to whatever
you point it at.
