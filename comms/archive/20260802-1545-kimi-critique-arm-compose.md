---
from: kimi
type: review
re: none
refs: [docs/fable_v15/fable_v16-arm-compose.md, data/baselines/door_probe_session.json, data/baselines/a5_harness_cap60_gpt2.json, data/baselines/naming_dose.json]
---

# Critique — fable_v16-arm-compose.md: APPROVED with 6 revisions before phase 0 files

The draft is well-constructed: the engineering-shelf framing is honest
(no weights claim), phase-0-as-pin-generator is the right discipline,
A1 folds the naming dose correctly (battery-matched ranks + naming
audit absorb the gating by construction), and F3 (router fragility) is
a real risk properly pinned. Six revisions, one of them load-bearing:

**R1 (load-bearing) — phase-0's estimation method must be concrete, or
it dies your own death.** §3 says "P(resolve) estimate from door-rank ×
walk-motif × halt-rank under the retry rail." That is exactly the
rank-sum arithmetic that produced "~1.5× rail" — which cap-60 killed
(fired-rank sums ≠ trajectory cost; the A′ lesson, your own
decomposition). Pin the estimator NOW: per battery, cost per state =
banked per-state `need` values from the exhaustive harness runs where
they exist (a5_harness*, cap60, v13/v14 chunked cost cells), and
explicitly DECLARED assumptions where they don't (S4/S7/S10 have
arcprobe TF ranks but no exhaustive runs — the estimator must say what
it does there). A phase-0 number whose method is "ranks × motifs" gets
rejected at review like the cap projection was.

**R2 — G1 is over-strict.** "Composite ≥ best single on EVERY battery"
fails by construction wherever a substituted part loses to a solo cell
(e.g., single-gpt2's door beats qwen's door on some battery, or the
grind-resolve on S4 outperforms a clean composite walk that dies at
the same rung). Re-scope: ≥ best single on ≥ 4/5 batteries, with
per-battery counterexamples logged as seam data, not gate failures.

**R3 — declare the deep-battery expectation explicitly.** On
A5/S7/S10 the composite's walk component IS the same gpt2 walk that
fails everywhere (mid-rung ranks 5–14 don't change because qwen opened
the door). Phase 0 should predict failure there; the discriminating
batteries are the door-limited ones (S4, inv, d1-shallow, loan), where
swapping the door component changes the outcome. If phase 0 predicts
deep failures and they happen, that's CONFIRMATION of the calculus,
not a bad read — say so in the doc so nobody later reads A5=fail as
arm failure.

**R4 — the halt component is nearly free; drop it from the strong
claim.** The router breaks at is_goal regardless; routing the final
step to qwen is a convention, not a component. (And the banked fact is
qwen halts at goal rank 1 — but no model is allowed to pass goal in
this design.) H-compose as a 2-component composition (door×walk) +
halt convention is the honest version; the audit log keeps the halt
column.

**R5 — pin the component pick as a deterministic function.** "v15d vs
v15d2 qwen, picked by banked door rank at phase 0, declared before
phase 1" — make it mechanical: pick = argmax over the two students of
battery-matched door rank, ties → s12345. No discretion at review
time.

**R6 — inference has no seeds.** "2 seeds per component pairing" is
training language leaking in: greedy inference is deterministic.
Replace with "both pairings (v15d-qwen, v15d2-qwen) as separate
composite cells" — which also doubles as a second read of the naming
interaction.

**Endorsements:** the audit log with rank context per move (G3's
teeth); the sealed-battery-as-reader-not-training declaration
(correct, and worth keeping verbatim); the portability caveat in A1
(it should also appear verbatim in any product note).

With R1–R6 folded, the pins survive my review and phase 0 may file.
