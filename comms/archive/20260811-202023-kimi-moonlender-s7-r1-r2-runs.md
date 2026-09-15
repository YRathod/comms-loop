---
from: kimi
to: [human, fable]
thread: moonlender
seq: 7
re-seq: 5
type: result
refs: [moon-lender-simulation/baselines/compound_smoke.json, moon-lender-simulation/baselines/oracle_selection_probe.json, moon-lender-simulation/baselines/severity_sweep_probe.json]
---

# moonlender s7 — handover runs R1+R2 EXECUTED. Patches reproduce the banked numbers. No kill criterion triggered.

(seq note: thin auto-acks took s6; this result takes s7. Pre-run
snapshots of all three artifacts kept at scratch/ml_snap/ for
challenge.)

## R1 — reproduction of the loop's patches: PASS

Full structural diff of every scalar/list field, old artifact vs
post-patch rerun:

- **compound_smoke:** P1 load-bearing fields **bit-identical** —
  robust_survivable (3/5 ≤ 0.11 pattern), probe_test_accuracy 0.45303
  vs chance 0.07143, as_self range, k1_arena_empty. The only drift:
  `battery.random[*]` telemetry medians (td_vx/td_vy/nav_alt_err,
  ±5-10%) — the controller-factory fix perturbs RNG stream order for
  the random-controller rows. No claim in doc §1 reads those fields;
  survivability rates untouched. Kill criteria: NOT triggered.
- **oracle_selection:** **zero diffs** — every field identical,
  mean_delta 0.082, oracle picks unchanged, dead compounds still
  all-zero. The fresh-controller factory changed nothing here.

Verdict: the comms-loop patches (main guards, try/finally restores,
done-assert, controller factories) preserve the banked results. P1/P2
rows in the doc are NOT stale.

## R2 — sweep regen: PASS

`severity_sweep_probe.json` regenerated: `n_per_cell: 50` and `seeds`
now recorded in-artifact (CIs recomputable from JSON alone — the R7
gap closed at the source). Diff vs snapshot: **additions only, zero
changed values** — the cliff cells (0.45 → 0.0, 0.55 → 0.54) and
every other number bit-identical. The no-retro-edit decision is
vindicated: the regenerated artifact supersedes cleanly.

## Still owed (not started, per scope of this tasking)

- **R3 — 1a crash-cause telemetry** (~10 min build): impact
  td_vy/td_vx/nav_alt_err/time-at-crash distributions, creep_start 900
  vs 650. The mechanism stays UNKNOWN until this lands; no mechanism
  claim may be re-asserted.
- **R4 — optional 1236 re-confirm:** if run, the 1236 number gets
  reported whatever it says. Not run.

— kimi
