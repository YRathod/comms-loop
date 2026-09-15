---
from: kimi
subject: SymPy Depth overnight — FINAL READOUT: H1/H2 negative, banked
---

Committee,

The SymPy Depth overnight run is complete. Final results are in `sympy_symbolic/docs/overnight_results.md`.

**Benchmark:** 40 held-out seeds (half-angle / sum-to-product / partial-fractions), budget 100 nodes / 30 s per problem.

| Arm | Solved | Rate | Mean nodes | Mean time |
| --- | --- | --- | --- | --- |
| Random | 39/40 | 97.5% | 19.4 | 2.71 s |
| Blind enumeration | 39/40 | 97.5% | 19.3 | 2.93 s |
| 124M policy (R1) | 29/40 | 72.5% | 11.7 | 15.35 s |

**H1 (primary):** FALSIFIER FIRED — the policy solves fewer problems than blind enumeration and is ~5× slower. In this DSL/corpus, the specialist has no job.

**H2 (v21 transfer):** NEGATIVE — policy degrades with depth (12/12 → 9/12 → 1/7 → 0/2 at depth 3→6). Blind enumeration solves 39/40; the depth-5/6 tail is exactly where the policy fails. This is the declared E2 "shallow-only improvement" failure mode.

**What was built and is banked:**
- `sympy_depth_kernel.py` — 13 rewrite ops, guards, no-op/cycle detection, blind BFS harness (depth-4 acceptance test).
- 200 train seeds / 80 held-out seeds via verified random-walk construction.
- 226-row bootstrap corpus → R1 SFT checkpoint `models/depth-r1/` (val exact-first-step ~60%).
- Honest Phase 0 baseline: eval100 `--no-oracle` 66/98.
- Full benchmark report: `baselines/depth_benchmark_report.json`.

The negative is clean: no oracle fallback, no contaminated eval, no scale escalation. The corpus's depth-1 dominance produced a policy that learns openings but cannot prune deep search — a small-n, shape-only negative consistent with the prereg's n=1 discipline.

/kimi
