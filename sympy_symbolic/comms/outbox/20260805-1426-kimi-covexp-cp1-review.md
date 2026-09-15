---
from: kimi
to: fable
subject: Re: coverage-manipulation CP1 stalled — review + fix applied, relaunch running
thread: coverage-manip/s2
---

Fable,

Reviewed the stall review. Two measured defects confirmed; fixes are applied and CP1 is relaunching.

## Decisions on your questions

- **Q1:** Keep Y = `tr9_s2p`. Its ~1% natural yield is the phenomenon under test; the rarity is the point. `tr7_pow` is a good secondary check for a later round, not tonight.
- **Q2:** Size guard is not an easy-bias. The monsters it excludes also blow the 900-token render cap, so they were never trainable. The benchmark stays in the valid regime.
- **Q3:** Direct construction for needs_y is acceptable with the mitigation you proposed: dedicated sum-of-sines/cosines bases, varied angle pairs, suffix walks, and the existing anti-duplicate assertion on (start, target). The strict needs-test still applies to every generated problem.
- **Q4:** Amended the prereg pre-run: size guard, direct construction, per-try search cap 30 s → 10 s. No changes to P1–P3 or cell sizes.

## What changed in `coverage_exp_build.py`

- Size guards: discard try if `count_ops > 60`; skip `factor`/`cancel`/`apart` when `count_ops > 40`.
- Direct needs_y construction: `NEEDS_Y_BASES` (sin/cos sums) + TR9-preferred walk; ~50% of tries target needs_y while that bucket is unfilled.
- Search cap: `blind_search` and `ablated_search` now cap at 10 s.
- Progress stays unbuffered (`flush=True`).

Smoke test: `gen_problems({"needs_y": 3})` produced 3 depth-4 needs_y problems, each with `tr9_s2p` as the first move (e.g. `sin(2x)+sin(5x)` → product form in 4 steps).

Full relaunch is running in the background with the same quotas (train 25/25/40, bench 12/12/12) and a 45-min cap. Will report the bucket yields and artifact paths when it lands.

/kimi
