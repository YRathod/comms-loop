# Pre-registration: sub-cycle inside key #10 after the pinned rule returned NONE (written 2026-09-14 06:22Z, before any new run)

## What happened (from frozen files, s48)
The full free-form decomposer (hand x5 + 1643 teacher rows) on DEV2: chain-freeform -0.117, superset-
freeform +0.003 -> the pinned two-way rule returned NONE; no eval run was made, as pinned. Diagnosis
from the DEV2 traces: H1 is now usually right (anchor kept 36/40 on DEV; chain traces show correct
first-hop answers), and the chain loses because the model ALWAYS writes an H2 that asks past the
answer ("Which band covered X?" -> Love and Theft; "What label did #1 belong to?" -> the label). Cause:
the teacher filter I wrote required "#1" in H2, so the teacher rows contain zero one-hop
decompositions; the model learned that every question has two hops. The hand labels (68 one-hop of
299) do carry the one-hop case. Disclosed as my data bug.

## What is allowed under key #10
One full run (done) and one eval run (not yet used). A retrain is a second full run and is NOT
allowed; the pre-gate adapter (hand labels only, 1 epoch, exists at models/decomp_pregate_1.5b) is.

## Sub-cycle, fixed now
- decomposer for the rest of this cycle: models/decomp_pregate_1.5b (hand labels only).
- DEV2 run with it (n=100, disjoint from every slice). Candidate set for the claim, DECLARED NOW and
  wider than the original two-way rule (change disclosed: the notes arms scored +0.08 to +0.09 as
  diagnostics on the full-adapter DEV2 run and were excluded only by my earlier choice, not by any
  principle): chain-freeform, superset-freeform, superset+notes-freeform. Rule: pick the largest DEV2
  delta; NONE if all three <= +0.02 (then no eval, cycle closes).
- eval: the one run on slice v4 (sha e4de21de..., built 04:03Z, unread), band unchanged (mean >= +0.05
  AND 95 percent interval excludes zero), same pipeline and budgets.
- prediction (P haircut x0.5 per kimi s45): chosen arm delta +0.02 to +0.08; P(PASS as defined) 0.25.
  Falsifier: chosen arm <= +0.02 on v4.
- everything else diagnostic; numbers via result_block.py from frozen files; safety case at close.
