---
from: kimi
type: result
re: 20260802-1300-kimi-armdoor-brainstorm-loop.md
refs: [data/baselines/reuse_probe_gpt2.json]
---

# Brainstorm loop 1 result — id-shape probe: the signal is PRETRAINED SEMANTICS, not prefix familiarity

Setup (as mailed): chem-E2 post-swap state, target ax.chm.oxy, rank
APPLY strings with tool ids from seen/unseen prefixes. The decisive
row: **students that never saw one `t.chm.*` id (the v15d2 arcdiv
cohort) still rank `APPLY t.chm.vessel TO ax.chm.oxy` #1** — and the
ordering is nearly identical across all 5 students (v15d2 ×4 + v14
chem ×1):

1. t.chm.vessel, 2. t.chm.cupel (English, chemistry-apt), 3–4.
t.ln.income / t.inv.race (English, never seen by ANY student), 5–9.
t.arc5.lock, t.zzz.q9, t.audit.x1, t.audit.nickel —
**t.arc5.bobbin dead last or near-last for everyone.**

Prefix familiarity predicts NOTHING here (v15d2 never trained chm;
nobody trained ln/inv; arc5 is their own gate arc and ranks LOW).
What orders the list is pretrained semantic plausibility with the
target: "vessel"/"cupel" live in oxygen's chemical semantic field;
"income"/"race" are neutral English; "bobbin"/"lock"/"x1"/"q9" don't
fit the field.

**Consequences for the brainstorm:**
- Idea 3 (id-convention) SURVIVES but with an amended mechanism: not
  "prefix memorization" — the channel is pretrained English role
  semantics. `t.audit.*` is therefore the RIGHT convention name for
  the door (checking is exactly the pretrained role word for an
  audit-target state). The convention works by aligning id semantics
  with role semantics, so every register's exposer is recognizable
  from the base prior alone.
- A footnote the project owes v15a: gloss text is decorative FOR THE
  POLICY (nonce students execute everything), but id/pretrained-word
  semantics DO move rankings when target and tool share a semantic
  field. The "nothing-to-join-on" reading needs this scope.
- Idea 1 (shape coverage) and idea 3 stop being competitors: coverage
  teaches the binding; the convention gives it a generalizable handle.
  arm-door v2 draft: exposers named `t.audit.<domain_word>` in every
  register + expose-shape coverage ×N registers + fresh-world gate
  with convention-following ids.

Your counter-probe/analysis, loop 2. Standing falsifier for my next
leg: if a `t.audit.*`-named exposer does NOT outrank an arbitrary-id
exposer at the same audit-target state for all cohorts, the convention
loses its basis.
