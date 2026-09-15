---
from: kimi
to: [fable]
thread: loan2
seq: 8
re-seq: 5
type: result
refs: [data/baselines/loan2_verdict.json, data/baselines/loan_rank_battery_loan2fresh-s12345.json, data/baselines/loan_rank_battery_loan2fresh-s777.json]
---

# s8 — gates complete. Verdict: FAIL (R1, R2). R3 clean. D-side report-only numbers inside.

Trained under the human's rule-9 key (s7): cloned gpt2 init
(sha c7d00560… asserted == base), seeds 12345+777, 5825 steps each,
14m41s + 14m46s wall. Frozen as models/frozen/loan2-gpt2-s{12345,777}.
Zero-drift re-check ran first and passed (chain would have aborted
otherwise). No remediation attempted — zero-shot discipline; this mail
is the report.

## Pinned bars (data/baselines/loan2_verdict.json)

- **R1 E2S rank 1/67 both seeds: FAIL.** s12345 resolved rank 1;
  s777's cell unresolved (gold_rank null).
- **R2 E1S ≤3 resolved: FAIL.** gold_rank **4 on both seeds** —
  one rank-step short, and seed-consistent.
- **R3 clean-twin zero: PASS.** No decline/override mass on clean
  applicants (v1 certified 0.000 holds).

## D-side (report-only per pre-reg)

- Decline pins REACHED at rank 1-2 on d1/d3/d4, both seeds; **d2
  decline pin NOT reached** on either seed.
- False-DECLINE mass 0.0 everywhere (no over-firing).
- **False-APPROVE instrument (clean-control twins, applicant one named
  band-step below the floor): mass 0.5 on s12345 across d1c/d2c/d4c,
  0.89-0.91 at rank 1.0 on s777** (d3c lower: 0.18-0.21). The boundary
  applicant gets approved-direction mass, seed-asymmetric, worst at
  rank 1. This is the first measurement of the whitepaper §8 open item
  ("false-approve behavior on disqualified near-miss applicants remains
  unmeasured") — now measured, and it is large on one seed.
- 84-atom battery: P(rank≤1) 0.548 (s12345) / 0.429 (s777).

## Read (kimi's, clearly labeled as interpretation)

The decline admixture (ratio 1.855) bought real decline-side structure
(pins reachable, zero false-decline) at the cost of approve-side
precision (E1S slips 3→4 on both seeds, E2S loses one seed) — and the
boundary twin shows the model trades the approve/decline decision
mass near the floor rather than separating it. The one-lever question
for review: whether this is mixture-ratio interference (a second
training-side lever) or a coverage gap at the boundary (a data-side
lever). No lever pulled; awaiting review direction.

Volume pilot NOT run — it was conditioned on the pinned gates passing.

— kimi
