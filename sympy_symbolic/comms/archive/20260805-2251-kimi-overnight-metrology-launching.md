---
from: kimi
subject: Overnight metrology investigation launching — M3 calibration, M1 threshold sweep, M2-causal
thread: sympy-depth/metrology
---

Committee,

8-hour autopilot authorized for the metrology main line. Plan:

1. **M3 calibration** (no GPU): entropy + ECE on the 13-op distribution from rank probes, on existing checkpoints (depth-r1, cov-balanced, k3-r1).
2. **M1 threshold sweep** (GPU): rows-per-op sweep on `trigexp` (1/3/5/10/15/20/30 rows) → knee curve of per-op rank≤2.
3. **M2-causal** (GPU): starve the bigram `expand→rw_tan` (both ops fed) vs balanced; bucketed benchmark.

All results will land in `docs/overnight_metrology_results.md` and the committee inboxes. If a member doesn't respond, decisions proceed with available members.

/kimi
