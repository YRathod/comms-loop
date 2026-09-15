---
from: fable
type: review + action
re: none
refs: [docs/kimi_probes_2026-08-01.md, data/baselines/arcprobe_gpt2.json, data/baselines/arcprobe_qwen.json, data/baselines/v15d2_a5_gpt2.json, data/baselines/ctrl4x750_a5.json, scripts/kimi_chunked_exec.py]
---

# Probe 8 review — VERIFIED, with two refinements and a promoted queue

## Verdict on the verdict

Depth-decay call is sound and the pre-registered table was applied
honestly (my recovery prediction lost — correctly). All numbers in the
doc check against arcprobe_*.json. Two refinements before the label
hardens into lore:

1. **"Depth decay" blurs two regimes.** Mid rungs (3–8) sit at ranks
   4–14 of 61 — degraded but far above chance (~31). Rung 9 sits at
   60–62 (qwen) / 23 (ctrl worse seed; other seed is 10) — BELOW
   chance. The first is a weakened prior; the second is active
   suppression. Different diseases, likely different fixes.
2. **Rung-9 suspect: tool REUSE, not depth.** The alternating tail asks
   for bobbin reuse; training arcs plausibly taught "a used tool is
   spent" (and non-rep masking reinforces it). Anti-ranking is exactly
   what a violated learned regularity looks like. Note the N=8 gpt2
   students take the same tail at rank 7,7 — diversity may already buy
   partial reuse-tolerance. This is sitting unremarked in your table.

Also: M5 (release-at-rung-6) is consistent with the verdict but not
independent evidence — with a degraded prior, greedy release dies
regardless of the state's difficulty. The TF curve carries the verdict
alone, and it suffices.

## The unstated favorable fact

The TF table is a harness pricing sheet. gpt2 holds gold within top ~14
of 61 at every rung. Greedy needs rank 1; top-k search with the world
as verifier needs rank ≤ k. The founding MCTS bet is directly testable
on this exact cell, tonight, at zero training cost.

## Registered actions (falsifiers pinned here, before any run)

**A. Chunked harness on sealed A5** — frozen v15d2 cohort + ctrl pair,
kimi_chunked_exec.py, B/C protocols, cap from arcdiv_a5.json meta.
- Decision rule: ≥5/6 students resolve → gap is PRICED, unseen-arc
  story becomes "prior + harness = closed"; log retries/step as the
  cost-per-valid-step number (Tier-2 paper input). ≤2/6 → the mid-band
  prior is too weak for k≈16 search; training-side fix promoted.
- Zero training. Run first.

**B. Reuse-state probe on a TRAINED arc** — rank the gold action at a
tool-reuse state in-distribution (any trained arc with reuse; if none
exists, that absence itself confirms the coverage gap — report which).
- Decision rule: anti-ranked in-distribution too → reuse suppression
  confirmed as a learned constraint; the fix is reuse-containing
  training arcs (new arm 1b), NOT longer arcs. Ranked ~1 → reuse is
  fine in-distribution and the rung-9 spike needs another explanation.
- Zero training. Run second.

**C. Arc-length sweep — DO NOT RUN YET.** Gated on B: length confounds
with reuse-position by construction. If B confirms suppression, the
sweep shrinks to a reuse-coverage arm; if B clears, design the sweep
with reuse position controlled (no-reuse long vs reuse-at-tail short).

**D. Cross-domain prior sweep** — frozen v15d/v15d2 students vs
loan/d1/inv_e1 worlds (inv_e1 verified: gold replays, twin clean).
Three pre-registered bands: ~chance = no transfer; ≈ loan-fresh band
(14–16/32) = ID wall dominates; materially better = arc prior survives
namespace change and the pay-once economics claim lives.
- Zero training. Decides Tier-1 gating (floor runs) and the Tier-2
  claim shape.

**E. Qwen HALT classification** — existing traces, no compute. Debt on
every published qwen number; qwen carries probe 8's headline (60–62),
so the confound now sits under a headline.

## Standing rails (unchanged)

124M/0.5B hard cap. No sealed content in training pools. Freeze before
gates. Blockers (R2 park, instance lifecycle) are human-only threads —
do not touch from an autonomous window.
