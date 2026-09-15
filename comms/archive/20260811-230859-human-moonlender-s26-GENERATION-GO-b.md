---
from: human
to: [kimi, muse, fable]
thread: moonlender
seq: 26
re-seq: 25
type: key
refs: [moon-lender-simulation/docs/prereg-fdir-schedule-v0.md, moon-lender-simulation/docs/fdir-arm-execution-plan.md]
---

# moonlender s26 — GENERATION GO. Rule-9 key on record. Freeze §§1–8 at v6 after the fresh-seed FAR confirm.

**Human direction, verbatim: "go"** — issued 2026-08-11T23:08:25Z in
response to s25 (which pinned the sequence: fresh-seed FAR confirm →
freeze → pilot). This is the explicit generation authorization the arm has
been holding for.

**Freeze target:** `docs/prereg-fdir-schedule-v0.md` **v6**, sha256
`2d2fd00a3680415129d9c43d39c874188a325f05055d9e7dfe71f0b1aa7b3a25`,
35,177 bytes. Verify this hash before freezing. If it does not match, the
artifact moved after the GO — **stop and report**, do not freeze a
different object than the one authorized.

## Authorized sequence

1. **Fresh-seed FAR confirm at 5σ×3.** Seeds disjoint from the gate's own.
   PASS = FAR ≤ 0.01. **Fail ⇒ STOP**, do not freeze, report.
2. **Freeze §§1–8.** Record the freeze sha + UTC in the artifact. From this
   moment §§1–8 are immutable; every later change is a dated §9 amendment
   with affected numbers marked INSTRUMENT-SUSPECT.
3. **1a pilot** (40 cells) — labels, two-stage validation (both recipes),
   determinism check (2% serial, bit-identical).
4. **Green/red rule — this replaces the unconditional stop in s22.** The
   acceptance criteria are pre-registered, so no judgment is being
   delegated:
   - **Validation PASSES** (regret ≤0.02 on ≥95% cells, argmax identical on
     ≥90%) **AND** determinism bit-identical ⇒ **continue automatically**
     into 1b/1c + audits. No round trip needed.
   - **Either FAILS ⇒ STOP and report.** For the two-stage validation,
     escalate `n_search` 20→25→50 first as pinned; if it still fails, stop.
5. **Rung A** — a real kill point. Report the verdict either way. Do not
   push past a KILL.

## Standing stops (unchanged, still binding)

- Any **cloud spend or 124M escalation** — fresh rule-9 key required; the
  ladder permits escalation only on a failed smaller-rung gate, never by
  preference. "Solved by a 30k regressor" remains a preferred outcome.
- Any **post-freeze §§1–8 change** — amendment, dated, disclosed.
- Any **prior-violating PASS** — PVSG battery first; the proposer does not
  grade its own reversal.
- Any **P3 pass with a P4/P6 fail** — reported UNSAFE, headline says so, no
  softening.
- The **LOW-AUTHORITY** and **achievable-headroom** filters (s25) are
  computed from labeler output BEFORE any model is fitted, and their
  results are reported whatever they say — including if they empty half the
  P3 primary set.

## What I expect, honestly

The modal outcome of this arm is a **negative**: robust-v9 already doubled
blind-family survivability from three hand-tuned knobs, which leaves little
headroom for a learned layer. A clean negative — "a learned
severity→schedule layer does not beat a well-tuned classical schedule in
this regime" — is a full result under this prereg, not a failure, and it is
to be reported with the same confidence as a positive.

The oracle references (controls 5 and 6) carry the measurement that
survives either way: **does diagnosis buy recovery at all?** Neither the
diagnosis literature nor the control literature publishes that number.
Protect it — it does not depend on any model working.

Go.
