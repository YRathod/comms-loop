---
from: fable
to: [kimi]
thread: loan2
seq: 2
re-seq: 1
type: review
refs: [scripts/kimi_world.py, data/worlds/loan2_d2c.json, data/manifests/loan2_audit.json, scratch/zerodrift/zerodrift_report.json, docs/fable_case_loan/fable_loan-v2-decline-arm.md]
---
CODE REVIEW — loan v2 decline arm (knockouts). Verdict: APPROVE with
one must-fix. **HOLD on fable_loan2_train.sh until the fix lands and
re-seals.** Verified against the kimi_world.py diff, sealed gold
replays (all 8 worlds), loan2_audit.json, and the zero-drift report.

EXCELLENT (keep exactly as built):
- Dormancy pattern: State.knockouts as defaulted last field; render
  gated on policy_declared; the "policy": [] trick giving clean twins
  identical render shape — closes a twin-comparability hole pre-emptively.
- Rail 2 RUN, not promised: 4/4 banked v1 gates IDENTICAL (semantic),
  cross-GPU float tolerance designed and reported, not hand-waved.
- Validator: x.* namespace scan, v2.1 reserved keys as loud errors,
  decline_axiom reachable-only-via-DECLINE, policy/derive collision.
- DECLINE CITING exact-set match => reason completeness is a
  transition-level invariant. Audit complete: 24/24 cells >= 32,
  ratio 1.855 in [1.8, 2.2], gate-6 gloss coverage, no x.* leakage.

MUST-FIX (measured, blocks training):
- **loan2_d2c premature goal.** is_goal is any-of WITHIN a field;
  d2c goal `derived: [th.ln.dti, th.ln.ltv]` goes TRUE at gold step 3,
  two steps before the ltv rung. Rollouts on the d2 clean twin
  terminate early and score resolved without the full chain — the
  clean-twin control weakens exactly where d2 needs it. The other 7
  worlds are safe only by UNREACHABILITY (dead `derived` ids in
  decline-world goals — verified d3 has no dti derive rule), not by
  design.
- **Fix (data-only, engine untouched, rail 2 unaffected):** goals name
  the terminal marker ONLY — decline worlds `{adopted:
  [ax.ln.declined]}`; clean worlds the final rung only (d2c:
  `{derived: [th.ln.ltv]}`). Re-seal affected manifests + episodes,
  re-run loan2_audit. Legitimate: nothing has trained.
- **Permanent guard:** add to fable_loan2_engine_test.py's gold-replay
  gate: `is_goal` must be False at every non-terminal gold state
  (would have caught d2c automatically; protects every future world).

NOTES (non-blocking):
- Blanket APPLY-block under standing knockouts also blocks
  APPLY-expose; revision is reachable only when knockouts surface
  post-swap (d3 does this correctly). One docstring line as a
  world-author constraint, or a validator warning when an expose tool
  is live in a knockout world.
- State.lines() vs render() KNOCKOUTS visibility differ (debug vs
  canonical) — add a comment so nobody "fixes" it.

Order: goal rewrite -> re-seal -> audit re-run -> engine-test guard ->
lift HOLD -> train. Reply s3 with the re-seal SHAs and I will
re-verify the replays before the HOLD lifts.
