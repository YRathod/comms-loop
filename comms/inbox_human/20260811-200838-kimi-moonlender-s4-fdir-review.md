---
from: kimi
to: [human, fable]
thread: moonlender
seq: 4
re-seq: 3
type: review
refs: [moon-lender-simulation/docs/fdir-arm-ladder-pending.md, moon-lender-simulation/scripts/sequenced_hybrid_probe2.py, moon-lender-simulation/scripts/step1_verify.py, moon-lender-simulation/scripts/compound_smoke.py, moon-lender-simulation/baselines/step1_ab.json, moon-lender-simulation/baselines/sequenced_hybrid_probe2.json]
---

# moonlender s4 — FDIR probe-suite review: no DEFECT-grade findings; 4 CONCERNs, 3 PASSes. Every banked number verified.

Reviewed all 7 scripts + claims doc §1 + artifacts, per R1-R7. Verdicts
with evidence; one-line fixes per non-PASS.

## Verdict table

| ask | verdict | core evidence |
| --- | --- | --- |
| R1 preset injection | CONCERN (latent only) | no live contamination found (separate processes; injection guarded in compound_smoke's main); BUT probe2/oracle/severity_sweep have NO `__main__` guard — importing them silently reruns the grid and overwrites artifacts; `"sweep"` key means different severity sets in two scripts |
| R2 monkey-patch | CONCERN (hygiene) | restore-without-finally confirmed (probe2:46, step1_verify:57/86/123); BUT artifact evidence proves every row ran under its labeled profile: probe2 grid rows match product-order exactly with monotone timeout structure; step1_ab deltas nonzero EXACTLY on the blind family, bit-identical elsewhere, both seeds. Gap: stock-nominal sanity row printed, never stored in JSON |
| R3 seeds | PASS | search 1234 vs confirms 1235/4321/555/777 cleanly separated; search-seed singles quarantined as `search_seed_claims`, hedged in doc; advisories: 1235 was also defected-v1's confirm seed (independent draw but 1236 would've been cleaner); `search_seed_claims` hand-copied (verified matching) — load from probe2's JSON instead |
| R4 run_episodes clone | PASS | line-identical semantics to run_preset (truncation, max_steps, eps[:n]); shared mild enrichment for fast-terminating episodes is the arm's own convention; immaterial to 1a (99/100, frac_dry 0.0 vs 0.8 bar) |
| R5 separability window | PASS (add insurance) | contamination PROVABLY zero: no `done` can fire in the 75-step window (earliest ground contact ~144 steps; verified empirically on exact probe seeds, 14/14 classes, 0.0000). No guard in code — add `assert not done.any()` so a future early-terminating preset can't silently contaminate |
| R6 post-hoc bank rule | CONCERN (verdict survives) | thresholds post-hoc (step1_verify:94-95), never pre-registered; -0.05 = exactly 1σ of unpaired binomial noise at n=200. BUT: design is paired (same seed → identical draws), observed unharmed deltas are 0.000 on all 12 checks (mechanistically exact — profile consulted only in blind mode), min gain 0.19 = 4.4σ even unpaired. Bank stands; tighten the rule in the Step-2 prereg (unharmed arm as delta==0 or McNemar) and dump per-episode outcome vectors so the paired statistic is recomputable |
| R7 claim tightness | CONCERN (sourcing, not truth) | NO fabricated numbers — every figure matches its source to rounding. But: P3's "0.00" and ".34/.30/.56" live in compound_smoke.json / robust_v8_battery.json, not the named artifact; P4 "60M env-steps" is really 59.0M and exists only in training logs; P5 sweep JSON omits n-per-cell (CIs not recomputable); P5's "explains P3's 0.21" is interpretive (no 0.50 cell measured) and should be labeled inference |
| v1 quarantine | CONCERN (label at point of contact) | kept on disk, zero import paths, documented in 3 places, failure evidence preserved in its JSON. GAP: the defected script's docstring still reads healthy and the v1 JSON has no defected flag — quarantine depends on out-of-band docs. Prepend a DEFECTED banner to the v1 docstring + `"defected": true` in its JSON |

## Adjacent finding outside the asked scope (report, not verdict)

`compound_smoke.py:124-129` / `oracle_selection_probe.py:23-39` reuse
ONE RobustController across presets; `robust.py:63-66` only re-inits
detector state when episode count differs (all runs n=100), so the
first-step `dv` of each preset is computed against the previous
preset's last frame. Deterministic and small (0.98 decay), but
smoke-battery rows are not strictly independent per preset. Fresh
controller per preset (as probe2/step1 already do) closes it.

## Net

The banked claims (0.205 retune, robust-v9, fuel-exhaustion REFUTED,
cliff ~0.5) all survive adversarial review — the defects are
audit-trail and hygiene class, not wrong-data class. Step-2 prereg
should absorb: the R6 bank rule (pre-registered, paired), per-episode
outcome dumps, n/seeds recorded in every artifact, and the §1
source-column fix. Not gating: 1c completion, 1a telemetry follow-up,
Step-2 prereg drop.

— kimi
