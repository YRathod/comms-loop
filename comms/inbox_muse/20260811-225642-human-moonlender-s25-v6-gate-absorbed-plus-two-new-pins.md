---
from: human
to: [kimi, muse, fable]
thread: moonlender
seq: 25
re-seq: 24
type: result
refs: [moon-lender-simulation/docs/prereg-fdir-schedule-v0.md]
---

# moonlender s25 — s24 absorbed (v6). 5σ×3 APPROVED. im2 + slim dispositions accepted. Two NEW pins added, one of which makes half your drawn P3 set vacuous.

kimi: the 0d gate firing is the best thing that has happened to this arm.

## The lesson, stated plainly for the record

My v2 arithmetic said FAR ≈ 1e-4. Measured: **0.0305**. The arithmetic was
**correct**; its **premise** — independent N(0,0.02) noise — was false. The
residual carries a systematic (peaks 0.03–0.05, lag-1 autocorr 0.96), so
correlated bursts manufacture ≥3-consecutive runs.

Your own s16 verified that arithmetic. **Three review rounds could not
catch this, because all three were reviewing a derivation, not a
premise. Only the instrument gate could.** That is the argument for
measuring instruments before trusting them, and it now has a number
attached to it.

## Approved

**5σ×3 (0.10 m/s²).** Reasoning accepted: 2.5σ headroom over the measured
systematic vs 1.5σ at 4σ; true-fault steps are 0.2–2 m/s² so nothing real
is lost; it zeroes the spurious branch-(b) attributions. **Your own caveat
governs — the re-pin was selected on the gate's seeds, so a FRESH-SEED
confirm is required before freeze.** High-pass fallback rejected as you
recommend (luna25 +73.6 s latency is disqualifying).

**im2 undetectable-by-design: accepted** — and it corrects *me*. My v3 text
claimed branch (c) covered im2; it does not. Noise ≠ dropout: readings keep
arriving, `alt_age` stays fresh, and σ 16–30 m passes a 150 m gate. Miss
1.000. Adding an innovation-variance branch to catch a fault that already
lands at 0.985 under robust-v9 would be new FAR exposure for no gain —
rejected as you recommend. Declared, not omitted.

**slim late `t_dec`: declared, lag NOT shortened** (shortening reopens a
reviewed fairness pin, and it biases against the model, which is the safe
direction).

## Two NEW pins — the second one matters most

**1. Schedule-sensitivity / LOW-AUTHORITY filter.** Your 273/500 finding
has a consequence you did not draw: if the decision lands at 20–45 m, the
schedule governs almost nothing, so at those cells **every candidate scores
alike and the argmax is arbitrary**. That is label noise, and it will read
as a **jagged map** at Rung A — muse's s19 hazard arriving through a second
door. Pinned: compute `spread = oracle-best − oracle-worst` per cell at
label time; **`spread < 0.05` ⇒ LOW-AUTHORITY, excluded from the Rung-A
smoothness ratio**, still reported, still feeds P4.

**2. P3 ACHIEVABLE-headroom eligibility.** Your seeded draw gave
H-pairs = {`resilience+luna25`, `slim+hakuto`}. Checked against the banked
artifacts:

| family | robust-v9 | best ever achieved | achievable headroom |
|---|---|---|---|
| slim+hakuto | 0.00 | **0.205** (schedule retune) | **+0.205 — real** |
| resilience+luna25 | 0.00 | 0.00 (oracle-selection, trust-nothing scan) | **+0.000 — nothing has ever worked** |

The v3 rule (`robust-v9 ≤ 0.85`) tests **nominal** headroom. Both pass at
0.00. But if `resilience+luna25`'s oracle-best is also ~0, that cell yields
`b01 = b10 = 0` **by construction** — **vacuous, which is precisely the
300 m failure you caught, wearing a different disguise. And it is half the
drawn P3 primary set.**

Pinned second condition: a cell enters the P3 primary set only if
**`oracle-best − robust-v9 ≥ 0.05`**, evaluated from the Stage-1 labeler
output **before any model is fitted**. Ineligible cells are run and reported
in full — as evidence about the **arena** (a possible region-(c) family),
never as a P3 result. Note this is decidable for free from Stage 1: if the
full 3,003-candidate search finds nothing above 0.05 on `resilience+luna25`,
that is itself a finding — the first real evidence that a compound can be
**unrecoverable by any schedule**, which is worth banking on its own.

## Sequence

1. Fresh-seed FAR confirm at 5σ×3 → report.
2. Then freeze 0e **on my go**, not before.
3. Then 1a pilot ONLY → two-stage validation + determinism check → STOP and
   report per s22.

Prereg is **v6**; §9 carries A-v6-1/2/3. Still PROSPECTIVE, no datum.
