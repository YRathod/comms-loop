---
from: human
to: [kimi]
thread: moonlender
seq: 3
re-seq: 2
type: review-request
refs: [moon-lender-simulation/docs/fdir-arm-ladder-pending.md, moon-lender-simulation/scripts/compound_smoke.py, moon-lender-simulation/scripts/oracle_selection_probe.py, moon-lender-simulation/scripts/sequenced_hybrid_probe.py, moon-lender-simulation/scripts/sequenced_hybrid_probe2.py, moon-lender-simulation/scripts/train_compound_spec.py, moon-lender-simulation/scripts/eval_compound_spec.py, moon-lender-simulation/scripts/severity_sweep_probe.py, moon-lender-simulation/scripts/step1_verify.py]
---

# moonlender s3 — CODE REVIEW REQUEST: FDIR compound-fault probe suite (7 scripts + 1 defected)

## What was built (2026-08-11, all local, $0)

Probe suite for the FDIR compound-fault arm (ladder + results:
`docs/fdir-arm-ladder-pending.md`; findings P1–P5 + step-1 verdicts
inside). Scripts under `moon-lender-simulation/scripts/`, artifacts under
`baselines/`. Results these scripts back: arena real (3/5 compounds
<=0.11 for robust-v8), schedule retune 0.00→0.205 on slim+hakuto, RL
compound specialist 0.00×3 (hover-haven), feasibility cliff ~0.5 thrust,
**robust-v9 banked** (fresh-seed ×2 reproduced), fuel-exhaustion
mechanism **REFUTED** (crashes retain 44.5% median fuel).

## Files to review

1. `compound_smoke.py` — compound injection + battery + linear
   separability probe (softmax GD, numpy).
2. `oracle_selection_probe.py` — best-existing-controller-per-compound.
3. `sequenced_hybrid_probe.py` — **KNOWN DEFECTED** (v1 hybrid failed
   nominal sanity 0.00; kept on disk per instrument-defect law). Review
   only that its defect is correctly documented and quarantined.
4. `sequenced_hybrid_probe2.py` — monkey-patches
   `agents.robust.blind_sink_profile`; source of the 0.205 + robust-v9.
5. `train_compound_spec.py` / `eval_compound_spec.py` — compound
   specialist training wrapper (stock train_ppo.main) + held-out eval.
6. `severity_sweep_probe.py` — 1D severity sweep (cliff finding).
7. `step1_verify.py` — 1a fuel check (REFUTED verdict), 1b robust-v9
   bank (BANKED), 1c cliff firming (running at drop time,
   `baselines/step1_c.json` when done).

## Specific review asks (where I most expect defects)

- **R1 — runtime preset injection**: `inject_compounds()` mutates the
  global `PRESETS` dict; `step1_verify`/`severity_sweep` also write a
  `"sweep"` key. Check for cross-contamination between probes in the
  same process and whether any script can silently run a stale preset.
- **R2 — monkey-patch hygiene** (`probe2`, `step1_verify`): module-global
  `blind_sink_profile` swap with try/finally-less restore. If any
  run_preset raises mid-grid, ORIG may not be restored. Confirm each
  result row was produced under the intended profile.
- **R3 — seed discipline**: grid searches select on seed 1234; confirms
  run on fresh seeds (compound n=200 seed 1235/4321; 1b seeds 555/777).
  Check for any place a search-seed number is reported as a banked
  result (the singles rows in probe2's own JSON are search-seed — the
  banked ones are only in `step1_ab.json`).
- **R4 — `run_episodes` duplication** in `step1_verify.py` clones
  `run_preset`'s loop. Check truncation semantics match (`eps[:n]`,
  max_steps) so 1a's crash population is not biased toward early-enders.
- **R5 — separability probe features** (`compound_smoke.py`): 75-step
  (~15 s) window under one controller; episodes that reset mid-window
  contaminate features. Quantify or bound that contamination.
- **R6 — 1b bank rule**: gains threshold (+0.10 both seeds, blind family)
  and unharmed threshold (−0.05) were chosen by me, post-hoc. Challenge
  whether they should have been pre-registered and whether −0.05 on
  n=200 is inside binomial noise.
- **R7 — claim-code tightness**: every number in
  `docs/fdir-arm-ladder-pending.md` §1 should be reproducible from the
  named artifact. Flag any claim whose artifact does not contain it.

## Open items the review does NOT gate

1c completion (cliff ±seeds), the 1a crash-cause telemetry follow-up
(open item — mechanism now unknown), Step 2 prereg (will come to you as
its own drop before any data generation).

## Standing discipline

Probe-before-training; sanity rows mandatory; search-seed results
unbanked; mechanisms unverified until telemetry-read; proposer never
grades its own reversal (PVSG applies to any prior-violating pass).
