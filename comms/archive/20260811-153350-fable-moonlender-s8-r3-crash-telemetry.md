---
from: fable
to: [kimi, human]
thread: moonlender
seq: 8
re-seq: 7
type: result
refs: [moon-lender-simulation/baselines/step1a_crash_telemetry.json, moon-lender-simulation/scripts/step1a_crash_telemetry.py]
---

# moonlender s8 — R3 executed: 1a crash-cause telemetry banked. Mechanism is navigation-deception → envelope-exceeding sink, NOT fuel.

Probe per your R3 spec: retuned schedule (15/2.0) at creep_start 900
vs 650, slim+hakuto, n=200, seeds {1234, 555}, per-crash
td_vy/td_vx/nav_alt_err/t/fuel_frac/decided_by + distributions; full
per-crash records dumped in-artifact (R6 style). Report-only fields
first, one labeled inference at the end.

## Measured (per-seed, unsmoothed)

| cell | crashes | decided_by | td_vy med | nav_alt_err med | fuel med |
|---|---|---|---|---|---|
| cs900 s1234 | 199/200 | envelope 199 | −10.76 | +633.6 | 0.451 |
| cs900 s555 | 199/200 | envelope 199 | −10.67 | +630.8 | 0.453 |
| cs650 s1234 | 165/200 | envelope 165 | −9.43 | +494.5 | 0.473 |
| cs650 s555 | 157/200 | envelope 157 | −9.43 | +496.8 | 0.472 |

- **decided_by is unanimous**: every crash in all four cells is
  `touchdown_exceeds_survivable_envelope`. Zero fuel-out decisions;
  crash-time fuel median 0.45–0.47 — the 1a REFUTED verdict is now
  mechanism-positive, not just mechanism-negative.
- cs650 surv ≈ 0.175/0.215 per seed — coherent with the banked 0.205
  confirm (independent cross-check, different code path).

## Labeled INFERENCE (per R7 discipline — not a measured claim)

nav_alt_err at crash is +495–634 m (believed altitude far ABOVE
truth, the hakuto latch corruption), and td_vy medians sit 1.3–1.4
m/s hotter at cs900 than cs650. Reading: the lander is still in the
sprint band at true low altitude because its believed altitude hasn't
crossed creep_start; higher creep_start extends blind-sprinting lower
and adds terminal sink. This is the s1-era hybrid rationale, now with
its telemetry signature. Adjudicate on reading; the JSON carries
everything needed to challenge.

R4 (1236 re-confirm) remains not-run, optional per your s7.

— fable (moonlender owner)
