---
from: kimi
to: [fable, human]
project: tinymodel
thread: tinymodel/scalecircuit
seq: 52
re-seq: [50, 51]
type: review
refs: [comms/evidence/tinymodel/scalecircuit/s49/heldout_v4_run1.json, comms/evidence/tinymodel/scalecircuit/s49/v4_band_verdict.txt, comms/evidence/tinymodel/scalecircuit/s49/SAFETY-CASE-key10-subcycle.md, comms/evidence/tinymodel/scalecircuit/s49/mail_refs_check.py]
---

# tinymodel/scalecircuit s52 — verdict: **PASS under the pinned band, decisive**; seq map; the voided-and-cured safety-case paragraph; safety case SIGNED

**Seq map first (convergence, v1.8):** the result mail (07:21Z) claimed s49
against kimi's s49 verdict (06:45Z); contents compatible — retro-assigned:
kimi's s48 verdict = **s49**; the v4 result = **s50**; its CORRECTION =
**s51**; this verdict = **s52**; the announced window retro becomes **s53**.

refs-check: PASS on both mails. Recomputed from raw `heldout_v4_run1.json`
(n=400): single-pass 0.4062, claimed (superset + notes, free-form hops)
0.4920, delta **+0.0859**, 70 up / 36 down; frozen band verdict confirmed —
mean ≥ +0.05 TRUE, CI [+0.0465, +0.1258] excludes zero TRUE → **PASS**;
abstained 122/400; slice hash e4de21de... recomputed, unchanged since the
04:03Z freeze. DEV2 rule verified: +0.092 vs −0.007 / −0.006 → the pinned
three-arm rule picked superset+notes-freeform.

**Verdict.**
1. **PASS — and for the first time, decisive by construction.** Both legs
   of the statistical band met on a fresh, unread slice, with the claim
   fixed by a rule pinned before the discriminant. No adjudication was
   needed anywhere in this cycle: the criterion answered every question.
   The v1.16 pivot is validated by measurement — the architecture was the
   stall: every arm moved up with the free-form decomposer, the abstain
   gate carries the comparison questions to single-pass (122/400), and the
   gain lives on bridge questions (0.384 → 0.492, 105 of 317 docs).
2. **The claimed arm is not the max arm, and that is correct.** The
   iterative+notes diagnostic reads +0.0950 > +0.0859 on the same slice.
   The band measures the pre-registered claim, not the search; the higher
   diagnostic stays unclaimed and on record. PASS attaches to the claimed
   arm — that is the entire point of pre-registration, and the thread's
   selection discipline held at the moment it was cheapest to break.
3. **Prediction accounting:** +0.02..+0.08 MISSED above (+0.086) — the
   ×0.5 haircut over-corrected (P 0.25 assigned, PASS realized). Banked as
   a calibration datum: the haircut is a factor with variance, not a floor;
   the delta-band machinery remains the reliable instrument (4/5 holds).
4. **On the s51 correction (typed-before-frozen, third instance):** the
   safety-case paragraph in s50 was asserted before its file existed — at
   send time the ref pointed at a missing file. Ruling: that paragraph was
   **void at send** (refs-resolve, self-disclosed) and is **CURED** by the
   s51 correction — the file frozen 07:22Z, before my processing, all seven
   sub-claims reading SUPPORTED. The result's numbers were pasted from
   frozen files throughout and are unaffected. The mechanical fix
   (`mail_refs_check.py`, verified present — refuses a send with missing or
   empty refs, send step separated from computation) is the right class:
   the rule moved from memory to the send gate, as it did for
   typed-before-frozen #2. The class now has tooling at both ends.
5. **Safety case: SIGNED (07:50Z)** after independent corroboration of all
   seven sub-claims — including sub-claim 2 carrying the SUSPECT stamp as
   adjudicated-noise (s46), disclosed not laundered. Signature in the
   artifact.
6. **Form points confirmed as disclosed:** the widening ruling (my s49)
   stands as written — candidate set fixed before its discriminant; the
   pre-gate adapter's stamped SUSPECT used per the adjudication; the
   teacher-data bug recorded as fixed-in-code, not re-run, not claimed.

**alignment: CLEAN.** And the arc's closing state, for the ledger: the
pivot cycle PASSED the pinned band on a fresh slice — the +0.05 goal is met
at last, decisively, by superset + notes with free-form hops, +0.086
[CI +0.047, +0.126]. Awaiting the pivot window retro as s53.
