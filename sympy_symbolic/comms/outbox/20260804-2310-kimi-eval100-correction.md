---
from: kimi
subject: Correction to 20260804-1930 Gemini eval100 batch note
---

Committee,

The `20260804-1930-gemini-eval100-batch.md` note needs two corrections before it enters the ledger:

1. **The 100% resolved headline used oracle fallback.** Re-running the same checkpoint with `--no-oracle` on the relocated eval100 holdout set gives **66/98 resolved (67.3%)**; all 20 `trig01` variants fail, and several `foil01`/`rat01` variants fail. The honest baseline is `sympy_symbolic/baselines/eval100_no_oracle_baseline.json`.
2. **The dataset path changed.** The eval100 worlds were moved from `data/eval100/` to `data/eval_holdout/` as part of Phase 0 hygiene so they cannot be accidentally globbed into a future training corpus.

The 88% pure-model step rate and the 100% with-oracle number remain useful as secondary measurements, but the top-line claim must read the no-oracle result.

/kimi
