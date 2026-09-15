---
from: human
to: [kimi, muse, fable]
thread: moonlender
seq: 31
re-seq: 30
type: key
refs: [moon-lender-simulation/data/fdir_arm/labeler_twostage_validation.json]
---

# moonlender s31 — RED confirmed, STOP upheld. Before escalating: run the argmax SELF-CONSISTENCY check. The criterion may be untestable by construction.

Validation FAIL accepted: regret_ok 0.925 (<0.95), argmax 0.500 (<0.90).
**The stop was correct and the guard earned its cost** — without it we would
have generated 2,400 cells on an unvalidated shortcut.

## What the failure actually is

| cohort | n | argmax identical | regret ok |
|---|---|---|---|
| all (scored) | 40 | 0.500 | 0.925 |
| **live** | 35 | **0.429** | 0.914 |
| low-authority | 5 | 1.000 | 1.000 |

**The argmax misses are TIES, not errors.** Of 20 live mismatches, **median
regret = 0.0000**, max 0.0400 — the shortcut usually finds an *equally
optimal* schedule. Only **3/40** cells lose value at all (0.040, 0.040,
0.020 — the last is exactly at the boundary; confirm whether your test is
`<=` or `<`).

Diagnosis: **the schedule optimum is degenerate.** Many candidates tie.

## Next action — measure BEFORE escalating (≈1 min)

**Argmax self-consistency check.** Run the full pinned grid at n=50 **twice,
on two disjoint seeds**, on the same 40 pilot cells. Report argmax agreement
and regret between the two full-grid references.

This answers a question the current artifact cannot: **is ≥90% argmax
agreement achievable AT ALL on this landscape?**

- **If self-consistency is also ~0.5** → the criterion is measuring
  **tie-breaking noise, not shortcut fidelity**. It is unsatisfiable by
  construction, and no amount of `n_search` escalation will ever pass it.
  Retire it **on evidence** — `regret` becomes the operative criterion —
  and bank the self-consistency number as the justification.
- **If self-consistency is ~0.95+** → the shortcut genuinely degrades
  argmax. Escalate `n_search` 20→25→50 exactly as pinned.

**I am not moving the goalpost by fiat.** The criterion stays until a
measurement shows it cannot be met; if it is retired, the artifact records
why, with the number.

## Then, per the pinned path

Escalate `n_search` 20→25 and re-validate regardless — **regret is the
criterion that matters for D-1**, since DVM needs `oracle-best`'s VALUE, not
its identity. An understated `oracle-best` **manufactures a false negative**,
which is the one way the DVM can lie. 3/40 cells understating by up to 0.04
is material when the expected DV signal is ~0.08–0.2.

If `n_search=50` proves necessary, then "two-stage" IS the full grid: Stage 1
becomes ~2.2 h at your measured 1,560 eps/s. **Take the 2.2 h.** Do not
compress the recipe to protect a schedule estimate of mine — my estimates
have been wrong three times today and the labels are the one thing D-1
depends on.

## Bank this regardless of what escalation shows

**Finding: the schedule optimum is degenerate** — 20/35 live cells have an
alternative schedule with regret 0.0000. Consequences worth writing down
now, before any model exists:

1. For **D-1/DVM**: harmless. Only the value enters `DV`.
2. For **Rungs A–C**: material. Regressing to "the" argmax means **partly
   fitting tie-break noise** — the target is ill-posed wherever the optimum
   is flat. That is muse's s19 labeler-jaggedness hazard, except the source
   is the *landscape*, not the search. If Rung A ever runs, this belongs in
   its interpretation.
3. It is also a mild point **in favour of the arm's premise**: if many
   schedules are equally good, a model needs only to land in the flat basin,
   not hit a knife-edge.

Report: self-consistency result → escalation outcome → then proceed or stop.
