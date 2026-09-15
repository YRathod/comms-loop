# probe-tailprune — pre-registration for the banked session [Fable → Kimi]

**Date:** 2026-08-02 · **Status:** pinned BEFORE any state is read;
run when you pick this up. Frozen weights only, no training, sealed
episodes read-only (rank instrument on existing states — the probe-7
precedent). Origin: human proposal (session, 2026-08-02): "prune
already-evaluated old theorems at the tail step."

---

## Hypothesis

**H-tailprune:** the reuse-tail failure is partly carried by the
rendered derived-list — the visible record of the pattern-so-far. A
tail state re-rendered with already-evaluated theorems pruned (see
Pruning rule) lifts the reuse move's rank on the same frozen student.

**Prior, declared honestly:** LOW. Probe 8 banked "pruned render fails
identically" (crowding eliminated) and B′ banked pattern-continuation
(used tools PREFERRED in-distribution) — both point against. This
probe earns its run only because the proposed pruning is narrower than
the banked cell: used-theorems-only, tail-states-only, dependency-
aware. If the banked nulls hold, expect F1.

## Pruning rule (pinned)

At a tail state, remove from the DERIVED block every theorem that is
(i) not the newest, (ii) not a declared parent of the current rung
(K3 multi-parent guard), and (iii) not referenced by the goal test.
Everything else in the render is byte-identical. Two variants:
- **V1 (full prune):** all non-exempt evaluated theorems removed.
- **V2 (half prune):** oldest half removed — the dose row, so a
  positive result carries a gradient, not just an endpoint.

## Design

- **States:** the exact banked death states — S7 and S10 reuse-tail
  rungs (composite run, arclen batteries) + A5 alternating-tail rungs.
  All already-read states; no fresh sealed material consumed.
- **Students:** v15d2-gpt2 both seeds + ctrl N=4@750 both seeds
  (the walker cohort; per-scale rule — report qwen05 separately if
  run, never averaged in).
- **Instrument:** banked `rank_actions` — rank of the gold reuse move
  among ALL legal actions, n_legal recorded per state, chance derived
  per state. Baseline column = unpruned rank on the identical state
  (already banked; re-run in-session for same-code comparability).
- **Conditions:** baseline / V2 / V1 per state per student.

## Pins

- **PASS:** median reuse rank ≤ 5 under V1 (from banked 23–71) on
  ≥ 2 students × both tail worlds, with V2 intermediate (dose
  consistency). Consequence: ships as a DECLARED harness term
  ("tail-prune reader"), engineering shelf, pivot-assist precedent —
  NEW READER = NEW LINEAGE, never compared to banked rows; arm-tail
  (weights arm) still runs, unchanged, on its own question.
- **F1 (falsifier, expected):** median rank shift < 3 positions vs
  baseline ⇒ derived-list is not load-bearing for the tail; pattern-
  continuation confirmed by a third instrument; proposal RETIRED;
  arm-tail proceeds with this null appended to its justification.
- **F2 (inversion):** rank WORSENS ≥ 3 under V1 ⇒ derived-list is
  load-bearing context; banked as a render constraint (no pruning in
  any future reader); arm-tail unchanged.
- **Anti-postdiction:** predictions per condition may be filed by
  either agent before the run; anything filed after first read is
  labeled postdiction per C-rider.

## Rails

- No training, no render changes to any training pool or sealed
  battery file — pruned variants are in-memory probe renders only.
- Dependency exemptions (Pruning rule ii–iii) computed from world
  metas, logged per state in the artifact.
- Artifact: `data/baselines/tailprune_probe.json` — per state:
  n_legal, baseline/V2/V1 gold ranks, exemption list, student, seed.
- One session; if PASS, the composite re-run on S7/S10 under the
  tail-prune reader is a SEPARATE registration (do not bundle).

## Why this is worth one session (context for the record)

S7 and S10 are the composite's only predicted-and-confirmed deaths;
both died at this exact rung class. A zero-training reader rule that
flips them would complete the composite's coverage of the arclen
ladder at inference cost — and even the expected F1 is a third
independent confirmation of pattern-continuation, the sharpest
characterization yet of the one lesion arm-tail must fix.
