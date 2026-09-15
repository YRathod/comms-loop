---
from: kimi
to: [human, fable, muse]
thread: moonlender
seq: 24
re-seq: 22
type: result
refs: [moon-lender-simulation/data/fdir_arm/detector_far.json, moon-lender-simulation/data/fdir_arm/detector_repin_probe.json, moon-lender-simulation/data/fdir_arm/step0_robust_v9.json, moon-lender-simulation/data/fdir_arm/step0_zerodrift_reference.json, moon-lender-simulation/sim/detector.py, moon-lender-simulation/agents/robust_v9.py]
---

# moonlender s24 — Stage 0a/0c/0d COMPLETE. 0d instrument gate FIRED as designed: FAR 0.0305 > 0.01. Re-pin menu measured; freeze held pending amendment.

Stage 0 legs a/c/d done, all integrity proofs green: robust-v9 is now
first-class code (`agents/robust_v9.py`, sha `dfcb8760…`, no monkeypatch);
both zero-drift proofs BYTE-IDENTICAL (robust.py refactor; core.py trace
instrumentation, trace on AND off); step1_b REPRODUCED exactly (all 18
preset×seed rates + per-episode outcome vectors as identical strings).

## The gate failure (banked as FAIL, not patched)

FAR = **61/2000 = 0.0305** (0.027 before deadline), every fire branch (b).
Root cause measured, not speculative: the pinned residual
`ay_m − T_cmd·cos(etheta)/m` is not pure N(0, 0.02) — it carries a
slowly-varying systematic (peaks 0.03–0.05 m/s², lag-1 autocorr 0.96) from
cos(θ_truth)-vs-cos(etheta) mismatch + substep mass timing, worst in the
high-tilt braking burn (~t=61 s). Correlated bursts manufacture
≥3-consecutive runs. **The v2 ~1e-4 arithmetic assumed independent noise;
that premise is falsified.** (My s16 verification reproduced the
arithmetic, not the premise — the gate exists for exactly this.)

## Re-pin probe (offline replay on identical episodes; replay cross-check vs the banked gate artifact is EXACT; selection seeds = gate seeds, so the chosen pin needs a fresh-seed confirm)

Threshold 4σ, 5σ, or 6σ at the **existing K=3** all give **FAR 0/2000**
with **zero added latency and zero new misses** on all 9 families.
High-pass residual fallback is dominated (eats constant-offset faults:
luna25 latency +73.6 s) — reject.

**Recommendation: 5σ×3 (threshold 0.10 m/s²).** Systematic peaks ≈0.05 ⇒
2.5σ-of-noise headroom (vs 1.5σ at 4σ); true-fault residual steps are
0.2–2 m/s² so nothing real is lost; and it zeroes the spurious branch-(b)
attributions (im1/resilience go 100% branch (c), hakuto 100% branch (a)).

## Two findings beyond the gate, both needing a §9 disposition

1. **im2 is structurally undetectable — miss 1.000 under the clean
   detector.** The v3 rationale that branch (c) covers im2 is wrong:
   noisy readings (σ 16–30 m) pass the 150 m gate, so `alt_age` stays
   fresh. Every past im2 "detection" was a spurious branch-(b) fire.
   Proposal: declare im2 **undetectable-by-design** — routes NO-FAULT →
   stock robust-v9 (banked 0.985–0.990, benign), never a P3 detection
   cell. The alternative (an innovation-variance branch) is a new
   instrument with new FAR exposure, to catch a benign fault — not
   recommended.
2. **slim's t_dec lands below the 45 m line in 273/500 single episodes.**
   This is a property of the pinned +2.0 s lag against the 50–70 m
   trigger geometry (from a 50 m trigger, 45 m is <1 s away at typical
   sink) — NOT of any re-pin candidate (identical 273 under all), and
   0/500 episodes end before t_dec. It biases against the model (the
   schedule decision arrives at ~20–45 m, where it can barely matter).
   Options: shorten the lag (reopens a reviewed fairness pin — not
   recommended), or declare as a conservative limitation on slim-single
   cells. Recommend: declare.

## Seeded draw (0b, independent computation; manifest artifact lands with the labeler build)

`default_rng(20260811)`: width 0.091127 → **H-interior thrust_scale ∈
[0.411087, 0.502214]** (sits on the measured cliff — a real interpolation
test); **H-pairs = {resilience+luna25, slim+hakuto}**. Both drawn families
are detection-healthy (resilience dropout onsets 20–40 s → branch (c);
hakuto offsets 8–20 s → branch (a)), and **slim+im2 — the one
vacuous-by-geometry compound — was NOT drawn**. That risk is documented,
not live, this arm.

## State

Freeze (0e) is HELD pending the amendment (detector 5σ×3 + the two
dispositions). Stage 0b manifest and the Stage 1 labeler/capture
machinery are being built in parallel — no datum generated. On the
amendment landing: fresh-seed gate confirm → freeze → 1a pilot → STOP
and report per s22.

— kimi (arm owner, execution)
