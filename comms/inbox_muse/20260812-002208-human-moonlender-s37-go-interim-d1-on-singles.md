---
from: human
to: [kimi, muse, fable]
thread: moonlender
seq: 37
re-seq: 36
type: key
refs: [moon-lender-simulation/docs/oracle-diagnosis-value-measurement.md]
---

# moonlender s37 — GO confirmed, Stage 1 continues. ONE ADDITION: emit an INTERIM D-1 on the singles (1b) before entering 1c's ~11 h.

Human direction: **"Go"**. Stage 1 proceeds as launched. s36 accepted in
full — the report is exemplary and three things in it deserve saying:

- **You declined to launch under the expired key** (green landed 37 s past
  expiry; a 13 h run is not a "leg in flight"). That was the right call and
  the correct reading of the key.
- **You corrected the pilot agent's misstatement against the artifact**
  (21/24 → 16/24) even though it changed nothing operative. Self-reporting a
  discrepancy that nobody would have caught is the behaviour that makes the
  rest of the record trustworthy.
- **You declared the 13 h cost before generating** rather than compressing
  the recipe to protect my 2.2 h estimate. My estimate was wrong for the
  fourth time today, in the same way each time — extrapolating a measured
  throughput into a regime I had not measured. Yours is the number of record.

## The addition — interim D-1 at the 1b boundary

1b (360 single cells, ~2 h) completes long before 1c (2,000 compound cells,
~11 h). **When 1b finishes, compute and report an INTERIM D-1 on the singles
alone, then continue into 1c without waiting for me.**

Rationale: 13 h is a long blind wait for a measurement whose expected answer
is "small". The singles curve is a real, publishable DVM in its own right —
the floor version I costed at s27 — and it arrives at ~2 h. If `DV_crossfit`
≈ 0 across the singles, that is early evidence bearing on whether 1c's 11 h
is worth spending, and **that call is mine to make with the interim curve in
hand.**

Interim D-1 carries the same requirements as the final: `DV_crossfit`
primary, `DV_raw` labelled BIASED-UP, per-family severity **spans** (s30),
LOW-AUTHORITY cells marked and never averaged in, `oracle-severity-only` vs
`+state` gap alongside, and the measured winner's-curse gap per family.
**Label it INTERIM — singles only, 1c pending** so it can never be mistaken
for the full result.

## Unchanged

- **STOP at D-1** (the final one). Rungs A–C are mine to authorize.
- Hard stops: no cloud spend, no 124M, no §§1–8 changes (FROZEN
  `2d2fd00a…`; §9/§10 appends only).
- If an instrument defect surfaces mid-run: disclose and stop. Today's 0d
  gate is the precedent — a gate firing is the good outcome.
- Resumability matters more at 13 h than at 2 h: keep the per-cell
  checkpointing honest, and if the run is interrupted, report where it
  stopped rather than silently restarting.

Report at: 1b complete (interim D-1) → 1c complete → final D-1 → STOP.
