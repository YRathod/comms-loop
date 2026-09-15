---
from: human
to: [kimi, muse, fable]
thread: moonlender
seq: 30
re-seq: 29
type: review
refs: [moon-lender-simulation/docs/prereg-fdir-schedule-v0.md]
---

# moonlender s30 — freeze accepted; three build-time disclosures RATIFIED, one with a scope note. Proceed.

Freeze accepted. You verified byte-equality to the s26-pinned sha
(`2d2fd00a…`, 35,177 bytes) before freezing — that was the one instruction
I most wanted honoured, given how often this artifact moved under
concurrent edits. FAR confirm on a disjoint seed, 0/2000, accepted.
Reporting im2 as **0.996 rather than a tidy 1.000** is the right call and
the kind of thing that keeps an artifact trustworthy.

## Ratified

**(i) creep grid top = 3.9.** `1.5:0.2:4.0` yields 13 values ending 3.9;
consistent with the pinned 3,003. Correct as built, no action.

**(iii) Stage 1 ≈ 55 min at 1,560 eps/s (width 3,003), not my 24 min at
width 2,250.** Accepted, and my estimate is again the thing that was
wrong — I extrapolated from a width I measured to a width I did not.
Throughput evidently does not keep scaling with vector width. Compute-only,
no design impact. **Do not compress the recipe to hit my number**; 55 min at
the pinned resolution is the correct trade.

**(ii) severity ranges for components §3 does not name → preset-default
ranges.** RATIFIED as the zero-judgment reading. Inventing ranges post-hoc
would be exactly the unpinned-degree failure this prereg spent five rounds
closing.

> **Scope note to carry into the D-1 curve (not a change, a disclosure).**
> Preset defaults are *narrow historical bands* — e.g. luna25
> `accel_scale ∈ (0.55, 0.75)`, beresheet `cutout_t ∈ (20, 45)` — whereas
> the §3-named axes are wide (`thrust_scale ∈ [0.30, 0.95]`). So the
> continuous-severity axis is **wide for the named families and narrow for
> the rest**. Consequence: the "only continuous severity justifies a
> learned component" argument is carried mainly by the named axes, and the
> DVM curve will have **different severity spans per family**. Report the
> span alongside each family's curve so a flat curve over a narrow band is
> never read as "diagnosis buys nothing" when it may mean "we barely varied
> the severity." Narrow-span families are evidence about that family, not
> about the general question.

## Proceed

Green/red rule unchanged. On green: 1b/1c + audits, then **D-1 (the
diagnosis-value curve) and STOP**. Bring me the curve with per-family spans
and LOW-AUTHORITY cells marked; the decision on whether Rungs A–C ever run
is mine and rests on it.
