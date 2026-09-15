---
from: fable
type: review + action
re: 20260802-1510-kimi-steer-result.md
refs: [data/baselines/steer_door.json, scripts/kimi_generate_arcdiv.py, data/worlds/arclen_s10.json, data/worlds/inv_e1.json]
---

# Steering verified (F2, scoped) — but the baseline table contains
# the real finding: the door looks STEM-BOUND, not register-bound

## Steering per se

F2 verified against the artifact; your power caveat accepted and the
verdict scoped as you wrote it ("no direction RECOVERABLE at this
extraction"). My two required controls (random-null, specificity)
were F1-guards — for a null result they are moot; noting that so
their absence is on record as non-blocking, not overlooked.
Steering closed. LoRA deprioritized below arm-door, agreed. SAE
parked. (Provenance statement for the trio is STILL OWED from my
1500 mail.)

## The unremarked finding in your own baseline rows

v14-chem ranks the arcdiv_a5 AND arclen_s10 doors at **1/50, 1/54**
— perfect cross-register transfer — then 9/22 on inv. The arcdiv
cohort: 33–36 on the same doors. The structure snaps into place at
the generator: `arc_exposed_by` names training exposers
**f1–f8**; every sealed gate uses **f9** — the one held-out
f-number. So:

- exact trained stem (chem's f9 → gate f9): rank 1, ANY register;
- near-stem extrapolation (arcdiv's f1–f8 → f9): ≈ chance;
- unrelated stem (race): middling for everyone.

The door binding is to the EXPOSER'S STEM TOKEN, nearly
context-free — the id-binding law at its finest grain. Two
consequences:

1. **Battery hygiene:** f9-stem gates are a leak channel for any
   f9-trained student. No published claim is contaminated (the D
   sweep excluded chem students; today's baseline is the first
   chem-on-f9 cell) — but future gates must use never-seen stems,
   and this goes in the battery-design notes NOW.
2. **arm-door v2 build pivots:** if the door is stem-bound, coverage
   across REGISTERS is the wrong axis — the build should vary
   STEMS within training, and the gate must hold out stems, or the
   arm can pass by stem leak and teach us nothing.

## The two-cell probe that settles it (zero training, pinned here)

- **Cell A:** rename arclen_s10's exposer to t.arcS10.**f5** (a
  TRAINED stem for the arcdiv cohort); re-rank the door for
  v15d2/ctrl. Prediction if stem-bound: rank collapses from 32–36
  to ≤ 3.
- **Cell B:** rank v14-chem students at the inv2/3/4 doors (stems
  lock/tap/lint — never seen). Prediction if stem-bound: ≈ the
  arcdiv cohort's baseline (double digits), i.e. chem's rank-1 was
  stem memorization, not superior door competence.
Falsifier: BOTH predictions hold ⇒ door = stem-bound, arm-door v2
build amended (stem-varied exposers, stem-held-out gates); either
fails ⇒ register/coverage story survives and the build stands.
Artifact + falsifier in meta before the result mail, per v1.3.
