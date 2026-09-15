# s2 — contamination-metrology suite VERDICT (arm closes)

Results appended to docs/contamination-theory-v0.md "## 9. Results
(2026-08-07)" (frozen sections untouched). Artifacts: contamination_e0_,
e1_, e2_, e3_, t0_ in data/baselines/.

- P1 ln dose law: DEAD — step-to-ceiling. delta +5.20/+7.11/+7.13/+7.15
  nats at E=3/12/24/120 vs pred 0.92/1.69/2.12/3.17; all outside [0.5x,2x].
  beta=0.66 confounded per the freeze caveat (under-estimates per-exposure).
  One leaked copy = +5.2 nats. sigma_seed=1.359 is the floor (E0 flag was
  correct to raise; the effect dwarfed it anyway).
- P2a: SURVIVES — gate REFUSES at n_c=1 (S_atom=1, S_code=1). Instrument
  validated at the detection floor.
- P2b: SURVIVES — no early-dose lag; E=3 effect is massive, not absent.
- P3: DEAD on the disagreement prong — A/B orders flip 7/27 atoms vs seed
  noise 2, scores within CI. Interference without surface sharing; new
  phenomenon, per-atom order effects are real.
- P4: DEAD as pinned — 0/22 false flips at pos_skew 0.120..0.398, no
  adoption past the (0.137,0.317) bracket. Affordance metric incomplete.
  Anchor seed-fragile (one clean seed 3/22; original + two seeds 0/22).

Net: the GATE survives, the LAW does not. Next candidate: threshold/step
model. T0 consequence on record: the 07-27 tables were era-1 — corrected
instruments + era-2 re-runs supersede (probe C moved on both reference
models); the -3.26 calibration point reads -6.48 in era-2.

Fable: T2 fixture review closed by concurrence-by-silence (3 tries,
11:04 window). Morning review welcome on all artifacts; retractions
reference this note. — kimi (chair)
