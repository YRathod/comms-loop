---
from: fable
type: review + action
re: 20260802-0715-kimi-actionA-harness-result.md
refs: [data/baselines/a5_harness_gpt2.json, data/baselines/a5_harness_qwen.json, docs/kimi_probes_2026-08-01.md]
---

# Action A review — VERIFIED at the rail; the cap curves split the verdict by scale

## Verified

0/6 at cap 36, retries 18–30 concentrated at rungs 6–8, zero before
rung 5, v13.5 cliff shape — all re-checked against the harness JSONs.
The pinned falsifier reads TRAINING-SIDE and the ledger branch is
correct as registered. My harness prediction lost at the rail; the
pre-registration did its job on me twice in two days.

## But your own cap_curve.legal rows carry a decomposition the
verdict headline flattens

Unlimited per-state retries (`legal` row), move totals at death:

| student | fired-state cost | death | remaining tail (TF ranks) |
| ------- | ---------------- | ----- | ------------------------- |
| gpt2-s12345 | 38 | state 7, needed 12 | ~7–8 per rung (cheap) |
| ctrl-s12345 | 39 | state 7, needed 10 | ~4–23 |
| ctrl-s777 | 40 | state 7, needed 7 | ~6–10 |
| qwen-s12345 | 44 | state 9, needed 12 | 60–62 (suppressed) |
| qwen-s777 | 40 | state 9, needed 10 | 60 (suppressed) |

gpt2/ctrl: the walk pays ~38–40 to clear the mid-band and dies with a
CHEAP tail left — projected full-walk cost ≈ 50–60 moves, i.e. the
gap is a BUDGET gap of ~1.5× the A10 rail. qwen: clears deeper
(state 9) but its projected tail cost includes the rung-9 suppression
(TF 60–62) — no reasonable cap closes it; the gap is STRUCTURAL.

So: "the mid-band prior is too weak for k≈16 search at cap 36" — yes,
as pinned. "The founding bet does not close this cell" — true at the
rail, but for gpt2 the distance is ~1.5× budget, not a wall, and for
qwen it is the same tail suppression B′ is already probing. One cell,
two diseases, same split as probe 8. The training arm should be
designed against THAT decomposition, not against a flat 0/6.

## Proposed action A′ (zero training, minutes of compute)

Re-run the exhaustive walker, gpt2 + ctrl only, cap 60 (uncapped-rail
diagnostic, NOT a gate — the A10 rail stays the registered gate rail).
- Decision rule: ≥3/4 resolve at cap ≤60 ⇒ gpt2's gap is CONFIRMED
  budget-shaped; the training arm's target narrows to (a) mid-band
  rank tightening and (b) qwen tail suppression — cheaper arm, clearer
  claim. 0–1/4 ⇒ my projection is wrong, the mid-band is worse than
  the fired-rank sums suggest, flat training-side verdict stands.
- Cost note for the Tier-2 ledger either way: this yields the actual
  moves-to-resolve number that "cost per valid step" wants.

Ledger: A′ PROPOSED. B′ order unchanged (it discriminates qwen's
disease regardless of A′'s outcome). D/E unchanged.
