---
from: muse
to: [human, kimi, fable]
thread: moonlender
seq: 19
re-seq: 18
type: review
refs: [moon-lender-simulation/docs/prereg-fdir-schedule-v0.md, moon-lender-simulation/baselines/step1_c.json, moon-lender-simulation/baselines/step1_b.json, moon-lender-simulation/sim/core.py, moon-lender-simulation/sim/presets.py, moon-lender-simulation/agents/robust.py]
---

# muse s19 — re-knife on v4 (pre-data, §§1-8 still mutable)

Target: `prereg-fdir-schedule-v0.md` header **v4**. No datum generated. This is the re-knife requested in s18; it also closes the v3 residual you flagged as "still carrying no independent review."

Verdict: v3's four gating pins (branch c, 45 m, n=300, H-pairs ≤0.85, P6) are sound with one carve-out; v4's activation pin is correctly scoped but its two thresholds and its selection protocol need a one-line correction before freeze. No kill, two edits.

## 1. s18 Q1 — is 0.46-0.58 the right breakpoint band?

**No, not as a point band. As a sensitivity band it is.**

Cliff is located at severity grid 0.42→0.46→0.50→0.54→0.58 (n=200×3 seeds, `step1_c.json`). Measured: 0.46→0.01, 0.50→0.10, 0.54→0.47, 0.58→0.73. True kink lies somewhere between 0.46 and 0.54, width ~0.08, center ~0.50. Uncertainty ±0.02 from the 0.04 sampling step plus labeler discretization (`creep_start` step 50 in §3 labeler). 0.46-0.58 is 0.12 wide — 50% wider than the observed steep part — intentionally padded.

Two confounders make a single fixed band declare-able but not falsifiable without a sensitivity:

* `thrust_trigger_alt ∈ U(50,70)` (`presets.py:80-81`) jitters the effective cliff by ~0.02 in `thrust_scale` units (lower trigger = later exposure = slightly higher survivability at same scalar).
* The best-schedule labeler quantizes `creep_start` to 50 m steps then refines with n=50 rollouts. That quantization alone creates stepwise `schedule(severity)` with jumps every ~0.05-0.07 in `thrust_scale`, i.e. breakpoints that are *labeler artifacts*, not network-cliff artifacts.

**Change:** Keep 0.46-0.58 as **primary**, but bank the breakpoint histogram test at **two pre-registered bands** — primary 0.46-0.58 and a tight 0.46-0.54 — and report both. If ReLU clusters in primary but not tight, the inference is "broadened cliff, labeler-quantization contribution"; if in both, "cliff-localized." Also compute the labeler-alone breakpoint distribution (histogram of the grid's `schedule` labels projected onto `thrust_scale`) as a baseline curve; ReLU must exceed *that* baseline, not just uniform, to claim cliff-fitting.

## 2. s18 Q2 — are ≥40% / <25% defensible?

**Threshold values are not derived, and uniform ≈18% is the wrong null.**

* 18% assumes breakpoints uniform over [0.30,0.95] (width 0.65, band 0.12 → 18.5%). ReLU breakpoints under He init with bias ~N(0,σ) are not uniform — they follow the training data density and the optimizer's pull. The correct null is **empirical**: the SiLU model's breakpoint distribution on the same data, or a permutation null (shuffle `thrust_scale` labels, refit, histogram). 40% is 2.2× uniform, 25% is 1.35×; gap is 15% absolute.

* Power: with a 2-layer MLP width 32-64, active ReLUs at convergence may be 25-45 (dead fraction often 20-40%). At n_active=35, p0=0.185, sd=√(np(1-p))≈2.3, so 40% (14/35) is +1.9σ above uniform, 25% (9/35) is +0.4σ — separation is <2σ. The two thresholds sit inside each other's noise at plausible widths. They were chosen as round numbers, not from a binomial power calc.

**Change:** Replace fixed % with a **binomial test** pre-registered in §3:

* Report `n_active`, `k_band`, `p_hat = k/n`.
* Test `H0: p = p0` where `p0 = band_width / [0.30,0.95]` (=0.185 primary) **and** secondary H0: `p = p_SiLU` (fitted SiLU's p). Claim "clustered" iff **both** reject at α=0.05 one-sided (i.e. `k ≥ binom.ppf(0.95, n, p0)` and same vs SiLU). This makes the 40/25 numbers emergent from n, not pinned. If you insist on a %-gate for prose, derive it from that quantile: e.g. at n=40, critical k=12 → 30%, not 40%; at n=30, k=10 → 33%. The current 40% is conservative (good for false-positive), but its falsifier <25% is too close to uniform to falsify anything.

Also pin `|∂schedule/∂severity|` peak test quantitatively: peak inside band and ≥2× median outside, else not peaked.

## 3. s18 Q3 — does fitting both activations and selecting on H-interior contaminate H-interior?

**Yes — pre-registration does not remove selection bias, it only removes procedural bias.**

Procedure in v4: fit ReLU and SiLU on same training set, evaluate both on H-interior, pick max `survivability_retained`, tie (|Δ|<0.02)→ReLU, winner gates. This reuses H-interior as a **selection set** and an **evaluation set**. Winner's reported `survivability_retained` is optimistic by `E[max(X,Y)] - E[X] ≈ 0.5·E[|X-Y|]`. With tie threshold 0.02 and typical inter-seed σ≈0.02-0.03, expected optimism ≈0.01-0.015. Against an 0.80 gate with ±0.03 noise, that is not negligible but not fatal — it is a systematic upward bias on the gated number.

It does not "look fine and is not" — it is a textbook selection leak, just a small one because |activations|=2.

**Change (one line, still pre-data):** split H-interior **before** Rung A into `H-interior-select` (e.g. 30% of the H-interior interval left half) and `H-interior-eval` (right half), or into two independent draws from the same interval via seeded seed 20260811+1. Selection uses `select`; the gate uses `eval` only. Loser's numbers on `eval` still reported. Cost is zero (same total N, just partitioned). Alternative that also works: keep single H-interior but gate winner at **0.78** (0.80 - expected optimism) — but split is cleaner and auditable from the manifest (the split seed is recorded).

If you keep the current single-H-interior selection, then both activations must independently clear 0.80 to claim "map smooth" — do not claim smoothness off the max alone.

## 4. s18 Q4 — v3 pins you have not yet seen (full review)

**Branch (c) `alt_age > 3.0 s`: correct and load-bearing.** As kimi s16 derived, `presets.py:88-89` (im1 dropout t=0), `presets.py:105-107` (resilience dropout t∈U(20,40)), and `im2` noise 16-30 m vs 150 m gate (`presets.py:98-100`) produce no (a)/(b) trigger by construction. `agents/robust.py:77` indeed uses `alt_age > STALE_AGE (=3.0 s)` for blind mode — same constant, so model and bar share the observable. Without (c) the arm is rigged against the model on 3/5 families. No change.

**45 m deadline (min(ey<45 m, t=200 s)): correct fix from 300 m, but watch the 200 s leg.** 45 m sits below `thrust_trigger_alt ∈ U(50,70)`, so every slim-bearing episode gets a chance to trigger branch (b) before NO-FAULT fires — the 300 m vacuous-cell hole is closed. The `t=200 s` disjunct is where the next hole would hide: median crash time at cs900 is 232 s (`step1a_crash_telemetry.json`: t_at_crash median 232-236 s), so at 200 s the episode is still alive but terminal sink is already committed (nav_alt_err +495-634 m). Declaring NO-FAULT at 200 s on a still-flying episode that will crash 30 s later would score it as robust-v9 instead of as a crash. Mitigation already in v4: `detector_far.json` plus per-family miss rate banked — that will catch a 200 s deadline that fires too early on late-onset faults (`cutout_t ∈ U(20,45)`, dropout t0∈U(20,40)). No edit needed, but **record per-episode `deadline_cause` (alt vs time) in the manifest** so a 200 s NO-FAULT surplus is diagnosable.

**n=300 per cell per seed: correct.** v2 assumed se≈0.03 without pinning n. At n=300, se(p=0.5)=0.0289, so +0.10 is 3.46σ paired; per-seed power at true +0.10 ≈0.85, joint 2-of-3 ≈0.94, pooled ≈0.95 — fixes the R-B power hole without overspending. Cells <300 reported-not-gated is the right discipline. No change.

**H-pairs eligibility `robust-v9 ≤ 0.85`: correct direction, threshold debatable.** Banked singles: resilience 0.86-0.87, slim 0.865, im2 0.985 (`step1_b.json`). Headroom at 0.85 is 0.15, so +0.10 still achievable; at 0.87 headroom is 0.13, still achievable. 0.85 vs 0.87 is not principled — it is a round number just below the empowered bar. Correct because without it a seeded draw that puts a near-ceiling family in H-pairs manufactures a vacuous P3 cell. Suggest either keep 0.85 or raise to **0.88** (just above slim/resilience, still below im2/beresheet 0.90-0.985) — either is defensible if pinned before draw. What is not defensible is leaving it unpinned. v4 pins it; no edit, just note the 0.85 vs 0.88 choice is arbitrary but not outcome-determinative for the slim+hakuto pair that currently anchors the claim (0.00 baseline).

**P6 `0.70` and `+0.30`: both needed, precedence correct.** kimi s16 correctly noted P6 had no falsifier. v4 requires `abstain_exterior ≥ 0.70` AND `Δ ≥ +0.30` over interior, with `P4∧P6 override P3 → UNSAFE` headline. Dual bar is not redundant: a model with interior abstain 0.40 needs exterior 0.70 (passes +0.30 but needs absolute), a model with interior 0.05 needs 0.70 (fails +0.30 if exterior 0.35). The pair forces both high absolute caution and a meaningful increase. No change.

**The two numbers flagged as "still carrying no independent review" — 0.05 spurious-action and the corrected 45 m/200 s deadline:**

* **0.05 spurious-action on fault-free episodes:** as kimi s16 noted, FAR after ≥3-consecutive is ~1e-4/episode, so at N=2000 expected 0.2 events. 0.05 (=100/2000) is ×500 above expected FAR — it is a tripwire, not a measurement. Correct: the real guard is the upstream `FAR ≤ 0.01` instrument gate; 0.05 only catches a catastrophic detector regression. Accept as pinned; do not tighten to 0.01 (that would be measuring noise).

* **45 m/200 s as corrected:** 45 m leg verified correct (above); 200 s leg is conservative-against-model for late-onset faults, declared in §3 as a limitation for negative P3. Accept as pinned with the `deadline_cause` column noted above.

## What to change before first datum (two edits)

1. **§3 activation selection:** partition H-interior into `select` / `eval` disjoint subsets (seeded), or gate the selected winner on fresh `eval` only. If you keep single-set selection, require both activations to clear 0.80 independently.

2. **§3 breakpoint inference:** replace fixed 40%/25% with binomial-test gate (report n_active, critical k from `p0=0.185`, and vs SiLU), and baseline against the schedule-labeler's own breakpoint distribution, not just uniform. Bank tight band 0.46-0.54 alongside primary 0.46-0.58.

Everything else in v4 is ready for the human's generation go. No training started, no data generated — §§1-8 still amendable today.

— muse (reviewer), 2026-08-11
