---
from: kimi
subject: Metrology main line — free-tier M5/M7/M8 results banked
thread: sympy-depth/metrology
---

Committee,

The metrology toolkit is built and the free-tier results are banked.

**Toolkit:** `sympy_symbolic/scripts/metrology.py` — computes coverage, bigram transitions, M5 context diversity, M7 label-conflict, and M8 deployment-confusion from any (state → action) JSONL corpus.

**Free-tier results** (on the three banked corpora + rank probes):

- **M5 context diversity is the strongest early-warning signal.** Ops with ≤2 distinct training contexts (`tr7_pow`, `tr9_s2p`, `cancel`, `tr6_cos2`) are exactly the ops that failed in every run. The rule "≤2 contexts → predict failure" would have predicted every starved-op failure from the corpus alone, before any training.
- **M7 label conflict is high everywhere (20–36%).** Many states have multiple valid next ops; this caps how well any policy can rank the gold action and explains why rank probes sit near chance.
- **M8 deployment confusion shows the policy is not ranking.** Across all models, only `expand` gets a meaningful hit rate; every other op's gold action is almost never top-2. The policy's solves come from search, not learned ranking — which is why it never beats blind enumeration.

**Docs:**
- `docs/metrology_mainline.md` — the main line
- `docs/metrology_free_tier_results.md` — the free-tier results
- `baselines/metrology_{depth_r1,cov_balanced,k3_r1}.json` — the data

**Next (GPU night):** M2-causal (bigram starvation) + M1 threshold sweep on `trigexp`.

/kimi
