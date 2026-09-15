# Pre-registration: the VERIFY reader arm (constraint -> verbatim quote -> mechanical check -> filtered retry)

Written 2026-09-14 ~17:30Z by fable, before key #12 exists. Motivation: on v5, 126 of 400 questions had the
gold answer in the passage and the 3B reader still answered wrong or partially (s57 loss autopsy). The
single-question demo (scripts/verify_demo.py) flipped a recency error to the gold answer by rejecting
candidates whose supporting sentence fails a mechanical constraint.

## Mechanism (reader-side, applied identically to single-pass and to the wiring)
1. Constraints extracted mechanically from the question: years, dates, numeric ranges, counts;
   ordinal/temporal words (first/last/before/after/successor) mapped to year ordering; the role noun of
   a "who was the <role>" question. No model judgment in the check.
2. The reader answers with a verbatim supporting sentence; the sentence is checked against the
   constraints; on failure the passage is filtered to sentences that satisfy them and the reader chooses
   among those only; if none, the original answer stands. Questions with no checkable constraint are
   untouched. Never worse than the unverified answer by construction, except when the filter is wrong.

## Development (DEV2 only, n=100, no held-out slice)
- coverage: share of questions with a checkable constraint;
- flips: wrong -> right vs right -> wrong under verify, for single-pass and for superset + notes;
- pinned stop: if right -> wrong flips exceed one third of wrong -> right flips, the arm is not evaluated
  and the cycle closes with that finding.

## Eval (ONE run, slice v6: n = 400, seed 20260919, disjoint from every prior slice, hashed before any model reads it)
- pipeline as key #11 (free-form decomposer = the 299-hand-label adapter, superset + notes, equal budgets),
  with verify ON for both the baseline and the wiring; the run also records both without verify.
- primary claim, fixed now: verify vs no-verify on the same wiring (paired, per doc): PASS = mean delta
  >= +0.02 AND the 95 percent bootstrap interval excludes zero. Secondary (reported, not the claim):
  wiring+verify vs single-pass+verify against the standing +0.05 band, and single-pass+verify vs single-pass.
- prediction (raw, no haircut): verify delta +0.01 to +0.04 on the wiring; P(PASS as defined) 0.4.
  Falsifier: verify delta <= 0.
- everything else diagnostic; safety case assembled before the result mail; every mail through the refs gate.
