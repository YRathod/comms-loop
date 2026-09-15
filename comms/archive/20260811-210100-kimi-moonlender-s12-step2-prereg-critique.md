---
from: kimi
to: [human]
thread: moonlender
seq: 12
re-seq: 11
type: review
refs: [moon-lender-simulation/docs/prereg-fdir-schedule-v0.md, moon-lender-simulation/sim/core.py, moon-lender-simulation/sim/presets.py, moon-lender-simulation/agents/robust.py, moon-lender-simulation/scripts/step1_verify.py, moon-lender-simulation/scripts/battery.py, moon-lender-simulation/baselines/step1_b.json, moon-lender-simulation/baselines/step1_c.json, moon-lender-simulation/docs/fdir-arm-ladder-pending.md]
---

# moonlender s12 — STEP-2 prereg critique (R-A…R-E). Verdict: strong skeleton, 4 MUST-FIX before first datum

Code claims below were verified line-level against the cited files this
session (sim/core.py, sim/presets.py, agents/robust.py, scripts/). Baseline
numbers verified in-artifact (step1_b.json, step1_c.json). The design
instincts are right (cheap-kill-first reordering, inverted size ladder,
paired-primary §8). The problems are concentrated where the prereg meets
the actual sim.

## R-A — the oracle ceiling is NOT a ceiling as specced. MUST-FIX.

The attack the human asked for succeeds, but not via terrain — there is
**no terrain or geometry state at all**: flat plane, touchdown at y≤0
(`core.py:244`), no wind field. That specific worry dies. The ceiling
breaks on two other channels:

1. **Initial conditions.** Every episode randomizes y∈[2200,3000],
   x∈[−2600,−1800], vx∈[40,80], vy∈[−55,−30], fuel∈[440,600] kg
   (`core.py:95-101`). All of it is visible in the 11-dim telemetry vector
   (believed state + fuel fraction, `core.py:122-135`). The oracle gets
   only `(thrust_scale, alt_offset_mag)`. Near the cliff (0.46–0.54,
   `step1_c.json`) feasibility is decided by exactly these per-episode
   margins — fuel fraction and entry velocity decide whether a schedule
   fits inside the energy budget. A telemetry model conditioning on ICs
   **should** beat a severity-only oracle per-episode. Rung A's kill
   logic ("no telemetry model can beat a ceiling it sits under") is
   inverted: under this spec, the ceiling sits *under* the model.
2. **The other 14 fault parameters.** A fault instance is the full 16-key
   vector (`presets.py:31-49`): onset times (`alt_offset_t~U(8,20)`,
   `cutout_t~U(20,45)`, `alt_dropout_t0~U(20,40)`), `thrust_trigger_alt`,
   `nav_init_bias_y`, `torque_dist`, `accel/gyro_bias`, `reject_lock`, etc.
   The prereg never states whether these are frozen at point values (as
   step-1 did, `step1_verify.py:167-171`) or sampled per episode
   (`core.py:103` samples them). If sampled: onset times and biases leave
   transient signatures in the pre-t_dec telemetry window, and they are
   schedule-relevant (how much descent remains under fault; when believed
   altitude crosses creep_start). Again: signal the oracle lacks.

**Fix (pin one):** either (a) freeze all non-severity fault params and
marginalize ICs by making labels *per-episode* best-schedule (oracle gets
severity + truth ICs at t_dec), or (b) hand the oracle the full truth
fault vector + truth ICs — "oracle-truth" — and keep the severity-only
oracle as a separate diagnostic row. Until then Rung A's KILL criterion
can kill the arm for the wrong reason (or pass it for the wrong reason).

## R-B — thresholds. MUST-FIX: n is pinned nowhere; +0.10 has a headroom-by-construction failure.

- **n per cell is never stated.** Without it the power question is
  unanswerable, which is itself the finding: pin n ≥ 200 per
  cell/seed (step-1's own standard) plus the total eval episode budget.
- **+0.10 is NOT inside noise at n=200** — paired, it needs b01−b10 ≥ 20
  with b01+b10 ≤ 100 for z ≥ 2, comfortably reachable (step1_b.json got
  z = 3.88–7.41 on deltas of 0.21–0.37 at n=200). So the number is fine
  *where headroom exists*.
- **But headroom is a pinned-cell problem.** Banked robust-v9 rates:
  resilience 0.86–0.87, im2 0.985 (`step1_b.json`). On any eval cell where
  robust-v9 ≥ 0.90, +0.10 is **unachievable by construction**; if the
  claim silently aggregates only weak cells, it becomes a selected-subset
  claim. Pin: the primary H-pairs cell set, every cell with robust-v9
  headroom ≥ 0.15, and P3 must hold on **every** held-out family (not
  ANY — multiplicity is currently unpinned).
- **Ratio gates degenerate near zero.** Rung A/B's 0.80×/0.50× of
  oracle-best is noise where oracle-best ≈ 0.01 — and `step1_c.json` has
  best-cell survivabilities of 0.005–0.01 at severity 0.46 (±1 episode
  flips the ratio). Restrict ratio gates to cells with oracle-best ≥ 0.20,
  else use an additive criterion.
- **P3's ambiguous band is undeclared.** Rung A honestly declares
  0.50–0.80 AMBIGUOUS; P3 has falsifier <+0.05 and pass ≥+0.10 with the
  (+0.05, +0.10) band undefined. Pin it the same way.

## R-C — one-shot t_dec. MUST-FIX: "first-fault-detectable" does not exist in the sim.

- **There is no detector.** Detectability exists only implicitly: the nav
  filter's innovation gate (ALT_GATE=150, reject-lock after 3 consecutive
  rejections, `core.py:204-212`) and robust.py's heuristics (blind on
  `alt_age>3.0`, deficit accumulator on sustained saturation,
  `robust.py:68-77`). Detection time is therefore severity- and
  family-dependent, and "exact value fixed at generation time" (§3) is an
  unpinned post-hoc dial that can be tuned to the model's advantage. Pin:
  a frozen detector instrument (reuse the innovation-gate trip or the
  deficit accumulator — both exist), t_dec = detector-trip + 2 s, detector
  code hashed into the config like everything else in §8.
- **Category mismatch with the bar.** robust-v9 re-plans at 5 Hz,
  closed-loop, every step (`robust.py:80-115`); the (sprint, creep,
  creep_start) triple parameterizes **only the blind-mode sink cap**
  (`step1_verify.py:32-35`, consulted at `robust.py:90`). The model emits
  3 scalars once. Two consequences, one in each direction:
  - *Handicap:* faults with staggered onsets (beresheet cutout_t∈U(20,45),
    resilience dropout∈U(20,40)) can fire **after** t_dec; the model is
    structurally unable to respond, on exactly the compound families
    H-pairs will hold out. This silently caps P3.
  - *Advantage:* none found that isn't already covered by matched
    telemetry windows — provided t_dec is pinned by a frozen detector.
  Pin: either a fixed re-decision cadence (model re-emits every K s;
  decision count is the matched budget) or keep one-shot and add a
  **robust-v9-frozen-at-t_dec** control (its blind profile committed at
  t_dec, no further re-planning) so the one-shot question is measured,
  not assumed.
- **Unstated:** who flies t=0 → t_dec (presumably stock robust-v9 — pin
  it), and that the model's triple replaces only the blind profile, not
  the PD layer. Otherwise the comparison confounds decision layer with
  control layer.

## R-D — leakage audit for continuous severities: concrete statistic proposed.

Fragment = neighborhood under the Rung-A regressor's own kernel. With RBF
length scale ℓ (pinned at Rung A), for each eval episode's fault vector
θ_h compute `K_max = max_i exp(−||θ_h − θ_i||²/2ℓ²)` over the training
manifest, distances in the **full 16-param fault space** (per-component
range-normalized), not just the 2 severity axes (R-A item 2). Gate:
`K_max ≤ e^{−4.5} ≈ 0.011` (≈ min distance ≥ 3ℓ) for every H-pairs /
H-exterior episode; the joint co-occurrence check becomes "no training
episode within ℓ of a held-out draw in BOTH pair components
simultaneously" — single-ingredient proximity is the intended ZSL overlap:
allowed, but its distribution is dumped, not gated. Caveat: **H-interior
is exempt by design** (interpolation), so the withheld interval must be
wider than 3ℓ or the RBF leaks across the gap by construction — pin the
interval width against ℓ. Artifact: per-eval-episode min-distance vector
dumped like the §8 outcome vectors.

## R-E — missing entirely.

1. **Post-ABSTAIN semantics — the biggest hole in the doc.** Does an
   abstained episode score as non-survivable, or does a fallback
   (robust-v9 / safe-mode) fly it? If abstain = non-survivable, P4's
   abstain ≥ 0.90 on infeasible cells is free for an always-abstainer.
   If a fallback flies, the model can never lose a paired episode it
   abstained on — b10 ≈ 0 by construction and §8's no-harm bank rule is
   gamed. And P3's denominator is unpinned: survivable rate over ALL
   episodes or decided-only? Decided-only lets abstention cherry-pick the
   +0.10. Pin: abstain = non-survivable for scoring (or fallback outcomes
   credited to BOTH arms), P3 over all episodes.
2. **Label-search budget unpinned.** "Best-schedule labels (local
   schedule search)" defines the ceiling's height; a weak search lowers
   the ceiling and flatters the model. The step1_c 12-point grid already
   disagreed with itself across seeds at 0.46 (sprint 12 vs 15). Pin the
   search space + evaluation budget per label.
3. **Clock-guard bypass.** robust-v9's profile has a t_frac>0.85 → 8 m/s
   timeout guard (`robust.py:40`); model-emitted schedules bypass it.
   Timeout is already non-survivable (surv = soft+tipped,
   `battery.py:48-57`) — good, keep it — but pin whether the guard applies
   to model schedules, else the slow-creep corner (creep 1.5,
   creep_start 1400) invites hover-prone schedules the bar itself would
   never fly.
4. **P6 has no numeric falsifier and no precedence rule.** "Abstention
   rises" — by how much, measured on which cells? And a confident
   exterior schedule that works passes P3 but fails P6: which governs?
   Pin: safety predictions (P4, P6) override performance (P3), same as
   P4's existing override.
5. **The bar is a monkeypatch.** robust-v9 = stock RobustController with
   module-level `blind_sink_profile` patched (`step1_verify.py:32-35,123`).
   For the arm, commit v9 as code with a hash. The thing everything is
   compared against should not be a runtime patch.
6. Minor wording: P4's "a cell that then crashes" — cells don't crash,
   episodes do. Rephrase per-episode: fraction of crashed episodes with
   p̂ ≥ 0.5 must be ≤ 0.10.

## What stands (no change asked)

Six-control set incl. random-schedule floor and false-fire; cheap-kill
reordering; inverted size ladder; §8 paired-primary + per-episode dumps +
search≠confirm seeds + no retro-edit + PVSG mandatory; the s10 inference
carried with its pinned ablation. These are right and I will hold the arm
to them as written.

**Bottom line:** no data until R-A (ceiling re-spec), R-B (n + cell set +
headroom), R-C (frozen detector + t_dec + who-flies-when), R-E.1
(abstain semantics) are pinned in §§1–8 as amendments BEFORE first datum —
after that they're unpinnable. R-D's statistic and R-E.2–.6 can land in
the same amendment batch.

— kimi (thread reviewer)
