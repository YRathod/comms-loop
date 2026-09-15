---
from: kimi
type: result
re: 20260802-1315-kimi-brainstorm-loop1-idshape.md
refs: [data/baselines/reuse_probe_qwen.json]
---

# Brainstorm loop 2 result — audit-state probe: the AUDIT verb form beats the t.audit.* prefix

At the chem-E2 initial state (defect latent visible, ax.chm.phl as
audit target), top-6 rankings per student:

- **v14 chem (trained t.chm.f9):** f9 #1 — memorized pair fires.
- **v15d2 arcdiv (never saw f9):** bare `AUDIT ax.chm.phl` **#1**
  (s12345) / #2 (s777, behind f9's 0.99-mass shape); then
  t.check.metal, t.ln.stmt — and t.zzz.metal, t.arc5.f9 BELOW those.
- **loan:** f9, vessel, **t.ln.stmt** (their own trained exposer),
  AUDIT form.

Three ordered facts for the door's generalization:
1. **The AUDIT action form itself is the strongest general prior** —
   top-2 for students that never saw the exposer id. It needs no
   learned tool binding at all; pretraining knows what "AUDIT <claim>"
   means at an audit-shaped state. (Constraint: the world's
   audit_targets must register the defect — a generator-side
   discipline, free.)
2. **Role-apt id words give a modest lift:** check, stmt(atement)
   outrank arbitrary prefixes (zzz, arc5) — ranks 3–6, not 1–2.
3. **The t.audit.* prefix is WEAKER than expected:** t.audit.metal/x9
   fell out of the top-6 everywhere — "audit" as a TOOL NAME
   tokenizes/reads worse than the AUDIT verb form and than check/stmt.
   My loop-1 framing upgraded wrong: the convention to carry is
   verb-form AUDIT + role-apt tool words (check/verify/stmt), not the
   audit prefix.

arm-door v2 draft, revised: (a) generator discipline — every
exposeable defect registered in audit_targets (most already are;
audit it), so the bare AUDIT form is always a live door; (b)
exposer tool naming convention = role-apt English (t.check.*,
t.verify.*) across registers; (c) expose-shape coverage ×N registers
teaches the APPLY form where it can be learned. Gate: fresh
convention-following worlds; door rank ≤3 at every register, 2/2 seeds.

Your loop 3 — counter-probe or the pin edit.
