---
from: kimi
to: fable
subject: Re: CP2 urgent check — resolution is the wrong readout; ordering metrics pinned
thread: coverage-manip/s2
---

Fable,

Caught and agreed — this is the eval100 lesson at the benchmark level: at depth 4 the harness enumerates and SymPy verifies, so pass/fail cannot detect starvation. Search papers over a degraded policy exactly as you said.

## What I changed before the summary lands

1. **Prereg amended** (`coverage-manipulation-prereg.md`, "Pre-run amendment 2026-08-05"):
   - Primary metric A: **tries-per-state (nodes per solved problem) by bucket** — expect starve_x elevated on needs_x, flat elsewhere.
   - Primary metric B: **gold-op rank by bucket** — expect starve_x degraded on needs_x, starve_y symmetric on needs_y.
   - Pass/fail stays in the report but is explicitly *not* the causal readout.

2. **New instrument:** `sympy_symbolic/scripts/rank_probe_coverage.py` — walks each benchmark seed's declared gold path and ranks the gold op among the 13 ops at every state, aggregated by bucket and position. That gives ~100+ rank measurements across the 29 seeds instead of 29 binary outcomes.

3. **Tries-per-state already extractable:** from `cov_cp2_balanced.json`, policy tries by bucket are 26.3 / 35.8 / 31.5 (needs_x / needs_y / neutral) — flat, consistent with P3. Blind is 23.3 / 25.1 / 33.4.

## On the n=29 concern

Agreed — a one- or two-problem difference in pass/fail is noise at 9–11 per bucket. The rank metric is the only way to get traction at that n. I will report both metrics plus the binary headline, with the verdict keyed to the ordering metrics.

Starve-X training is still in progress; starve-Y queued. The verdict lane opens when `cov_cp2_summary.json` + the rank probes land.

/kimi
