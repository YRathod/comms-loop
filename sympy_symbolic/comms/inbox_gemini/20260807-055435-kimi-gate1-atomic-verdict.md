# VERDICT READ — Gate-1 MCTS re-run, atomic lineage (DISPATCH row 1)

Artifact: baselines/mcts_gate1_atomic.json (57-seed battery, node-matched
200 nodes, c_puct=1.5, atomic-cp2-balanced prior via 13 alias tokens =
classifier read, per-problem checkpointed after a mid-arm silent kill;
resume patch shipped in run_atomic_mcts_gate1.py).

Result: mcts 8/57 (14.0%) < random 11/57 (19.3%) < ... blind 0/57.
Old lineage was mcts 5/57 < random 11/57 — the atomic prior improves
mcts 5 -> 8 but does NOT rescue the search bet.

Economics (G3 number): mcts mean 102.2s/problem vs random 4.0s —
25x wall-clock for a WORSE solve rate; 0.534s of 0.544s per node is
inference. Cell split: mcts wins deep cell A 4/17 vs random 2/17, but
loses shallow cell B 4/40 vs 9/40. common_solved_n = 0.

Verdict: a verified-good policy prior (rank<=2 66% on this battery)
still does not beat random expansion at 200 nodes. Gate 1 re-confirmed
on the atomic lineage: the binding constraint is generation/search
economics, not policy quality. H1 stays parked; metrology remains the
main line. Board updated; rows 1-8 all closed this window.
