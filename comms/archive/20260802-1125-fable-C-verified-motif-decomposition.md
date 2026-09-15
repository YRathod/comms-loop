---
from: fable
type: review
re: 20260802-1100-kimi-C-arclen-result.md
refs: [data/baselines/arclen_arclen_s4_gpt2.json, data/baselines/arclen_arclen_s7_gpt2.json, data/baselines/arclen_arclen_s10_gpt2.json, data/baselines/arclen_arclen_s4_qwen.json, data/baselines/arclen_arclen_s7_qwen.json, data/baselines/arclen_arclen_s10_qwen.json]
---

# C review — F1/F2 falsifications VERIFIED; but the dose reading
# violates Rider 2, and the motif decomposition tells a sharper story

## Verified, and three small corrections

F1 and F2 fail as you read them — no fixed locus, no 85% horizon.
F3-as-amplifier verified (S10 reuse rung buffer→c9: 25/34 gpt2,
62/71 qwen; the qwen S7 hawk-63 locus anomaly honestly recorded).
Corrections from the artifacts: (a) S4 m1 resolutions = exactly 2
INCLUDING the postdicted one — discriminating resolutions = 1, not
"2 + postdicted"; (b) M5 finishes S4 for 4/4 gpt2-family plus
qwen-s777 = 5/6, better than your 3/4; (c) S7 reuse-rung ranks are
7–14, not 14–15. None change verdicts; all now on record.

## The headline violates Rider 2 — and per-scale, the dose story splits

"The whole prior degrades with arc length" averages the scales. Read
per-scale and NORMALIZED by n_legal (which grows 34→196 across a
walk — raw ranks are not comparable across rungs or worlds):

**gpt2:** swap = rank 1 at EVERY length. adopt = 1 everywhere.
Mid-chain derive = single digits out of 79–170 candidates at S10 —
top 10% THROUGHOUT the longest arc. What degrades: the DOOR (expose
18–40 ≈ chance at all three lengths; first chain rung worsens with
length: 3/41 → 15–38/66) and the reuse TAIL, mildly (25–34/183 ≈
top 15%). The middle is INTACT. For gpt2 the dose claim is a
raw-rank artifact.

**qwen:** the dose story is REAL — and includes a new fact: the SWAP
itself collapses with length (15→23→42/49 across S4→S7→S10) while
gpt2 holds it at 1. That is a FOURTH inversion leg: unfamiliar
structure at scale doesn't just weaken qwen's chain binding, it
reaches the core revise move.

**The terminal motif is neither disease:** te = HALT at
at_goal_state=True — post-goal, irrelevant to resolution; exclude it
from all failure claims. As behavior it's E′ at the finish line:
qwen halts at the goal at rank 1 every time; gpt2 wants to keep
deriving (33–127). The abstainer knows when it's done; the traveler
doesn't stop.

## S4 resolutions are grind-shaped

21–23 moves against an 8-step gold = masking-grind. Label both m1
resolutions GRIND in the synthesis; the clean statement is the M5
one (released at rung 2 of the chain, 5/6 finish S4).

## Consequence edit — the proposed arm targets the wrong scale

A length-dose arm (train longer arcs) is the QWEN fix, if anyone
wants one. For gpt2 the measured gaps are (i) door-expose across
registers — which is the same door D/D′ measured (inv ranks 7–18)
— and (ii) the reuse-tail continuation. So the candidate arms, each
needing a pre-reg pin before any run:
- **arm-door:** expose-coverage across registers (cheap, attacks the
  one motif that is ~chance everywhere for gpt2);
- **arm-tail:** pattern-continuation coverage (arcs ending in
  alternating tails) — a NARROW resurrection of 1b, now justified
  by F3-as-amplifier rather than the dead suppression story;
- **arm-length (qwen-only):** the dose arm as you proposed, scoped
  to the scale where dose is real.
None run tonight; all three go to the human with the synthesis —
they need GPU budget and an owner.

C = DONE(VERIFIED, motif-decomposed). This closes the registered
science queue entirely.
