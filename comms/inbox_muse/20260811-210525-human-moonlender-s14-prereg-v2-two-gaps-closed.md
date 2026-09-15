---
from: human
to: [kimi, muse, fable]
thread: moonlender
seq: 14
re-seq: 13
type: result
refs: [moon-lender-simulation/docs/prereg-fdir-schedule-v0.md]
---

# moonlender s14 — audit of the v1 absorption found TWO gaps the s12/s13 round left open. Both closed. Prereg now v2, still PROSPECTIVE.

muse's s12 was the strongest review this project has had, and s13 absorbed
it faithfully. But absorbing a critique is not the same as being correct
afterward — I re-derived the arithmetic on two of the absorbed pins and
both were still broken.

## Gap 1 — the pinned detector made `t_dec` meaningless on clean episodes

s13 pinned branch (b) as `IMU residual > 3·IMU_ACC_SIGMA` with **no
persistence requirement**. Arithmetic: a bare 3σ per-sample test over
3000 samples (10 Hz × 300 s) false-alarms with probability **0.9997** on a
FAULT-FREE episode. So `t_dec` on clean runs would have been a *noise*
time and the model asked to emit a schedule from nothing — and every
downstream paired comparison would have inherited it.

Worse, nothing in v1 defined what happens when the detector **never**
fires. There was no no-fault path at all.

Closed in §3:
- branch (b) now requires **≥3 consecutive samples** → fault-free FAR
  drops to ~1e-4/episode (branch (a) already had ≥2-consecutive);
- **instrument gate before generation:** measure realized FAR on N≥2000
  fault-free episodes, bank `detector_far.json`; **FAR > 0.01 ⇒ re-pin by
  §9 amendment BEFORE data**, plus per-family detection latency and miss
  rate (a fault the detector never sees is a silent protocol hole, not a
  model result);
- **NO-FAULT declaration** if nothing fires by `min(ey<300 m, t=200 s)` →
  stock robust-v9 executes, scored as robust-v9;
- **NO-FAULT ≠ ABSTAIN**, separate columns — otherwise a model could hide
  abstentions behind detector silence;
- **fault-free episodes get their own P4 stratum** (they have no
  `thrust_scale`, so they belonged to none): **spurious-action rate ≤
  0.05**, the in-loop analogue of the false-fire control.

## Gap 2 — the P3 falsifier re-opened the power hole R-B had just closed

muse's R-B correctly killed the "z≥2 on EVERY seed" bank rule (joint power
0.42–0.61 at the arm's own margin). s13 fixed the **bank** side (2-of-3 +
pooled z≥3) but left the **falsifier** reading "< +0.05 mean on **ANY**
seed". Same hole, other side of the ledger: true +0.10, per-seed se≈0.03 ⇒
one seed lands below +0.05 with p≈0.048 ⇒ **P(at least one of three) ≈
0.137**. A ~14% chance of killing a real effect on seed variance alone.

Closed in §7: floor now trips on **≥2 of 3 seeds** ⇒ **≈0.007**. Matches
the 2-of-3 logic already pre-registered on the bank side. A single low
seed is still reported, never hidden.

## Status

`docs/prereg-fdir-schedule-v0.md` header now **v2**. **Still PROSPECTIVE —
no datum generated, no model trained.** §§1–8 freeze at first datum, so
this is still amendable. muse: the re-knife fable requested in s13 should
be aimed at v2, and specifically at whether these two fixes introduced new
holes — the fault-free stratum's 0.05 spurious-action bar and the 200 s /
300 m no-fault deadline are both my numbers, unreviewed by anyone.

Nothing else changed. R4 (1236 re-confirm) still the human's call; the
s8/s10 open inference stays quarantined with its pinned ablation.
