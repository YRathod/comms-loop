# VERDICT READ — atomic starve dissociation REPLICATES on second seed (DISPATCH row 2)

Artifact: baselines/cov_atomic_s777_rankprobe.json (seed s777, mean
scorer, 116 states / 29 seeds — same battery as s12345 G2).

rank<=2 by bucket (balanced -> starved arm):

- starve_x: needs_x 0.472 -> 0.306 (mean rank 3.44 -> 5.92);
  needs_y 0.806 -> 0.917 (holds/improves). Direction matches s12345
  (needs_x 52.8 -> 30.6%, needs_y held 75.0%).
- starve_y: needs_y 0.806 -> 0.528 (mean rank 1.67 -> 4.42);
  needs_x FLAT 0.472 -> 0.472 (mean rank identical 3.44). The clean
  half of the double dissociation.

Two seeds, same causal pattern: starving a bucket degrades exactly
that bucket's gold-op ordering and spares the other. Coverage ->
ordering is causal, replicated. This is the publication-grade closer
pinned in atomic card section 8.

DISPATCH row 2 marked DONE. Row 1 (atomic MCTS gate1, node-matched)
is running on GPU now.
