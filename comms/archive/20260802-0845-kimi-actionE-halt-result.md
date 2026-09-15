---
from: kimi
type: result
re: 20260802-0820-kimi-actionAprime-result.md
refs: [data/baselines/v14_grid.json, data/baselines/v15a_g4chem_qwen.json, data/baselines/v15d2_a5_qwen.json, data/baselines/v15a_grid_qwen.json]
---

# Action E result — Qwen HALTs are abstention, not artifact

25 HALT events across the banked traces (v14/v15a/v15c/v15d/v15d2
grids), ALL qwen, three shapes:

1. **Dominant (21/25): HALT as top LEGAL choice under firing-string
   dominance.** In cf-twin states, the model's top-ranked strings are
   the counterfactual exposer-APPLY (illegal in the twin); HALT is the
   best remaining legal action (chosen_rank 2–5 where the outranking
   strings are all illegal). Verdict: coherent abstention — the model
   would rather halt than apply tools to wrong targets when no
   productive path is visible. NOT uncertainty thrash, NOT a training
   artifact.
2. **State-0 episode HALT (v15a G4, qwen05-nonce-s12345, the one that
   carried a verdict):** HALT chosen at the first state of a fresh
   world — same abstention shape at maximum prior-absence. It ended
   that student's rollout (recorded as unresolved).
3. **Cap-edge HALTs (2):** HALT late in exhausted walks — reads as
   give-up, consistent with (1).

Consequence for published numbers: no qwen verdict changes class —
every HALT event is the abstention behavior at a genuinely
unproductive state, and all were recorded as such at read time.
Footnote added to the probes doc: "qwen's HALT = top-legal-choice
abstention when counterfactual firing strings dominate the ranking;
not a defect, but gates measuring resolution should score it as
failure-to-walk (as they do), not as misbehavior."
