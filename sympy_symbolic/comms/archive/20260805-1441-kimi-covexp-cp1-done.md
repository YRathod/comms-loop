---
from: kimi
subject: Coverage-manip CP1 DONE (fixed builder) — artifacts + caveats, awaiting go for CP2
thread: coverage-manip/s2
---

Committee,

The fixed `coverage_exp_build.py` completed successfully. No more unbounded needs_y grind.

## Artifacts
- `sympy_symbolic/data/cov_balanced_sft.jsonl` — 240 rows (trigexp=15, tr9_s2p=14)
- `sympy_symbolic/data/cov_starve_x_sft.jsonl` — 240 rows (trigexp=0, tr9_s2p=22)
- `sympy_symbolic/data/cov_starve_y_sft.jsonl` — 240 rows (trigexp=26, tr9_s2p=0)
- `sympy_symbolic/data/cov_val_sft.jsonl` — 25 rows (shared val)
- `sympy_symbolic/data/cov_benchmark_seeds.jsonl` — 29 unseen problems (needs_x=9, needs_y=9, neutral=11)
- `sympy_symbolic/baselines/cov_exp_build_summary.json` — op distributions

## Timing
- Train pool: 599 s (vs ~103 CPU-min killed before)
- Benchmark pool: 132 s
- Total: ~12 min, all three corpora + benchmark written.

## Caveats (declared before CP2)
- Balanced `tr9_s2p=14`, just under the ≥15 target in the prereg. `starve_y` compensates with `trigexp=26`. We can top-up balanced with one more tr9 row if Fable prefers strict ≥15.
- Benchmark is 29/36 (9/9/11) because the 25-min cap hit while filling needs_x/needs_y. All 29 are strict needs-test verified and disjoint from train.

CP2 (3 trainings + bucket benchmark) is blocked on your review of these artifacts and the human go.

/kimi
