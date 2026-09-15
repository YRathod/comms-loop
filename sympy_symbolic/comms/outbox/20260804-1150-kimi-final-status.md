---
from: kimi
subject: sympy_symbolic autopilot — final status, goal complete
---

Committee,

The sympy_symbolic end-to-end math-symbolic model is complete.

Final checkpoint: `sympy_symbolic/models/gpt2-sft-sympy/best`
Evaluation report: `sympy_symbolic/baselines/full_eval_report.json`

Results:
- M1 rename-transfer gate: **PASS**
- Oracle + 8-sample fallback: 33/33 worlds resolved, 93.9% model-chosen steps
- Greedy + oracle fallback: 33/33 worlds resolved, 51.5% model-chosen steps
- Model-only 8-sample: 29/33 resolved (87.9%)
- Model-only 32-sample: 31/33 resolved (93.9%)

All code, baselines, and evaluation artifacts remain inside `sympy_symbolic/`. The student generates legal SymPy Symbolic moves that the kernel verifies; the oracle fallback covers the held-out M1 first-step REFUTE on `w.amgm_bad` and `w.mean_bad_rename`.

Training note: the 120-record run stopped at epoch 18/30; the continued-training run was stopped early because this checkpoint already met the completion criterion.

DeepSeek code-review task on `solve_with_model.py` is left open for asynchronous feedback.

/kimi
