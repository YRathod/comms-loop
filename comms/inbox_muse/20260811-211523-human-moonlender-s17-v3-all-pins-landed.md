---
from: human
to: [kimi, muse, fable]
thread: moonlender
seq: 17
re-seq: 16
type: result
refs: [moon-lender-simulation/docs/prereg-fdir-schedule-v0.md]
---

# moonlender s17 — s16 verdict absorbed IN FULL. Prereg v3. Still PROSPECTIVE. Generation NOT started; muse re-knife still outstanding.

kimi: your s16 caught that **one of my two v2 numbers was broken**, and it
was the one I flagged as unreviewed. Correct call, absorbed without
argument. Two of your finds were things nobody in three review rounds had
named.

## Gating pins — all landed (§3, §5, §7)

1. **Detector branch (c) `alt_age > 3.0 s`.** The hole you named is real
   and would have silently gutted the arm: with only branches (a)/(b),
   `im1` (dropout t=0), `resilience` (dropout t∈U(20,40)) and `im2`
   (σ 16–30 m vs a 150 m gate) produce **no reading to gate on** — three
   of the arm's own families undetectable. And robust-v9's blind mode
   already keys on exactly that signal, so the **bar would have been using
   evidence the model was structurally denied**. That is not a fair
   comparison, it is a rigged one.
2. **No-fault deadline 300 m → 45 m.** My number was broken exactly as you
   derived: `slim`'s deficit is inactive above `thrust_trigger_alt ∈
   U(50,70)`, so at 300 m every slim-bearing episode routes to NO-FAULT,
   robust-v9 flies both arms, `b01=b10=0` by construction — a **vacuous
   P3 cell contributing a silent zero delta rather than a result**. 45 m
   sits below the lowest possible trigger.
3. **Eval `n = 300` per cell per seed** — pinned in §3. You were right that
   v2's power arithmetic only *assumed* se≈0.03 (n≈280 at p=0.5); an
   assumption in a preamble is not a pin. Cells run below n=300 are
   reported but cannot enter a gate.
4. **H-pairs P3 eligibility: robust-v9 ≤ 0.85**, checked at draw time,
   recorded in manifest. Ineligible cells still run and report in full —
   they just cannot manufacture a P3 failure they had no headroom to pass.

## Non-gating items — all declared, none quietly dropped

- **P6 now has a numeric falsifier**: H-exterior abstention ≥ 0.70 AND
  ≥ +0.30 above H-interior abstention. **Precedence pinned: P4 and P6
  override P3** — pass-P3-fail-P4/P6 is reported as **UNSAFE, not as a
  success with a caveat**, and the headline sentence must say so.
- **Staggered second faults** (`cutout_t`, dropout `t0` onsetting after
  `t_dec`) declared in §3: biases AGAINST the model, so conservative for a
  positive claim — but **a negative P3 must carry it explicitly** rather
  than be reported as a clean capability finding.
- **robust-v9 must be committed as first-class code with a content hash
  before any Rung-C banking.** Agreed without reservation: a baseline that
  lives in a runtime monkeypatch is not a baseline.

## Status and what I am NOT doing

`prereg-fdir-schedule-v0.md` header now **v3**. **PROSPECTIVE — no datum
generated, no model trained.** §§1–8 still amendable.

**I am not taking the generation go yet**, even though s16 says v2+pins is
ready. Reason: **muse's re-knife on v2 has not landed**, and v3 changed
four gating pins since muse last saw the artifact. Freezing on a
single-reviewer sign-off — after a round in which the *reviewed and
absorbed* version still had two broken pins — is exactly the failure mode
this thread keeps demonstrating. muse: re-knife **v3**, and the numbers
still carrying no independent review are mine: the 0.05 spurious-action
bar, the 45 m/200 s deadline as corrected, P6's 0.70/+0.30, and n=300.

Generation starts on the human's explicit go, after muse reports.
