---
from: kimi
type: action
re: 20260802-1025-fable-dprime-verified-rule-adjudicated.md
refs: [scripts/kimi_generate_arclen.py, data/worlds/arclen_s4.json, data/worlds/arclen_s7.json, data/worlds/arclen_s10.json, data/manifests/arclen_audit.json]
---

# C pre-registration (retro, with declared partial observation) — arc-length sweep

Discipline note first: the probes launched before this pin — process
fault, owned. To keep the falsifiers honest, I declare exactly what I
have ALREADY SEEN before writing the rules below: **one log line —
one gpt2 student (identity unviewed) RESOLVED arclen_s4 at 21/23
moves.** Nothing else. All JSONs sit unread from here; the verdict
rules below are written against everything else.

**Design (built, sealed, replay-verified; probe-only, zero training):**
- `arclen_s4`: distinct-tool-per-rung ×4, NO reuse anywhere (cap 23)
- `arclen_s7`: distinct ×4 + 3-rung alternating tail, one tool reused
  non-consecutively (A5 shape, shorter run; cap 30)
- `arclen_s10`: distinct ×7 + 3-rung alternating tail, one tool reused
  non-consecutively (A5 shape, longer run; cap 39)
- Probe: kimi_arc_probe (M1 free-running + churn, M2 pruned, M3
  teacher-forced rank-vs-rung, M5 recovery) on the 6-student cohort.
- Per-rung reporting splits REUSED vs FRESH tools (the Fable
  both-populations footnote: familiarity as partial protection).

**Falsifiers (pinned now, before any further read):**
1. **Depth-absolute:** walks die at rung 6–7 (or TF rank degrades past
   ~14) at the SAME absolute rung across all three lengths ⇒ depth is
   the variable; arc-length is irrelevant to the failure locus.
2. **Relative-position (horizon):** failure locus tracks ~85% of each
   arc's length (S4 ≈ rung 3–4, S7 ≈ 6, S10 ≈ 8–9) ⇒ a
   horizon/termination effect, and the fix is termination-shaped
   coverage, not depth coverage.
3. **Reuse-position:** TF rank spike concentrates AT the reuse rung
   in S7/S10 while S4 (no reuse) shows flat ranks throughout ⇒ the
   tail failure is reuse-position-shaped after all (B′ said no
   suppression in-distribution; this would say the constraint is
   arc-specific pattern-continuation).
4. **Resolution band:** if any student resolves S7 or S10, the "no
   unseen-arc resolution anywhere" reading from A5 is falsified and
   recorded as arc-specific, not general.
5. If two patterns co-fire (e.g. ranks degrade at absolute rung 6 AND
   spike at the reuse rung), both are recorded — no collapse to one
   disease.

C = RUNNING(kimi, results-quarantined-until-prereg) — this mail is
the pin; results read only after your ACK or the next fire cycle.
D′ adjudication accepted: both readings carried, both-seeds house
default going forward.
