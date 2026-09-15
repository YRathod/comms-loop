# VERDICT READ — D4 rank fusion (DISPATCH rows 7/8)

Artifact: baselines/d4_rank_fusion.json (5 frozen students: cov-balanced,
m1-1-500, m1-1-2000, k3-r1, depth-r1; 116 cov_benchmark states; mean
scorer; full 13-op rankings computed fresh on CPU — banked files store
gold-rank only, so Borda/RRF from banked files alone was impossible).

- Diversity gate: mean pairwise op-rank Spearman 0.808 < 0.9 — diversity
  EXISTS (the shared-SFT-kills-diversity prior is NOT confirmed).
- But fusion LOSES to the best member: borda rank<=2 0.526, rrf 0.552
  vs best member m1-1-2000 at 0.767. Weak students (k3-r1 0.397) drag
  the ensemble below the top student.
- Verdict: D4 stays demoted to optional, per the card. Ensemble is not
  the free lunch here even with real diversity.

Row 8 (pivot probe): SPEC_UNRESOLVABLE, honest negative — DROP is not
an op in the sympy kernel and no banked DROP candidate scores exist;
evidence in baselines/pivot_probe_fleet.json.

DISPATCH rows 7/8 marked DONE. Row 1 (atomic MCTS) running on GPU.
