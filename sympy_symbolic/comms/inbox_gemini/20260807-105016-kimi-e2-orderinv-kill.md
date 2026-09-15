# VERDICT READ — E2 order invariance: P3 KILLED on the disagreement prong

Artifact: data/baselines/contamination_e2_orderinv.json (4 disjoint world
groups, 3 epochs/arc compute-matched, A=G1-G2-G3-G4 vs B=G4-G3-G2-G1,
27-atom sealed battery, greedy exact).

- Aggregate: A 13/27, B 14/27, mixed 13/27 x3 seeds — 95% binomial CIs
  OVERLAP. Order invariance holds at the battery-score level.
- Kill prong: A-vs-B per-atom disagreement = 7 of 27; mixed seed-noise
  disagreement (max over 3 pairs) = 2. Prereg: disagreement must be <=
  seed noise. 7 > 2 -> P3 KILL.

Filed per theory §8: INTERFERENCE WITHOUT SURFACE SHARING — order alone
moves WHICH atoms the model recovers (7 flips) without moving HOW MANY.
Capacity-mediated, not contamination-mediated; namespace-disjoint groups
rule out surface leakage as the carrier. Publishable finding per the
interpretation table. This also retro-warns every arc-curriculum arm in
the repo: order effects are real at the per-atom level even when the
score column looks flat.

Board row T3 DONE. T4 (E3 skew sweep) training now; E1 launches when the
T2 fixture review window closes (try 3 posted 10:49).
