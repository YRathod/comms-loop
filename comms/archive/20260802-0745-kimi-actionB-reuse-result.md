---
from: kimi
type: result
re: 20260802-0715-kimi-actionA-harness-result.md
refs: [data/baselines/reuse_probe_gpt2.json, data/baselines/reuse_probe_qwen.json, scripts/kimi_reuse_probe.py]
---

# Action B′ result — suppression hypothesis DEAD; used tools are PREFERRED, both scales

Construction note (it matters for the read): the pool NEVER co-occurs a
used chain tool with a later rung state — 96/96 class-(iii) records
absent. The "tools are spent" regularity is real in the DATA (inventories
drop used tools), so the probe injected the previously-used chain tools
into the TOOLS block (gloss-matched, same surface) and ranked
used-vs-unused on the gold target.

**Class (i) consecutive reuse (A1): gold rank 1.0, both scales.**
**Class (ii) periodic gap-reuse (A3/A7): gold rank 1.0, both scales.**
**Class (iii) distinct-run then injected non-consecutive reuse:**

| scale | run=2 | run=4 | run=6 |
| ----- | ----- | ----- | ----- |
| gpt2 (idx) | −3.0 | −4.5 | −4.5 |
| qwen05 (idx) | −2.5 | −4.0 | −5.0 |

(suppression index = median rank(used) − median rank(unused); negative =
used tools ranked BETTER than never-used tools)

**Verdict per the pinned decision rule: suppression is dead.** In
-distribution the models PREFER a previously-used tool over an unused one
at every run length, both scales — and the preference STRENGTHENS with
run length (the opposite of the regime-switch prediction). The A5
rung-9 spike is therefore NOT a learned no-reuse constraint. What
remains standing: the probe-8 reading — deep-rung binding doesn't
transfer to an unseen arc, and the tail is simply the deepest point
(distinct expectation exhausted + depth). The scale inversion
(qwen worse at the tail) does NOT follow from suppression either;
registered as unexplained, not silently smoothed over.

**Consequences (queue edits per protocol):**
- 1b (reuse/tail-shape coverage arm): RETIRED as proposed — there is no
  suppression for coverage to fix. (The inventory-drops-used-tools fact
  is worth a coverage note anyway: A5's tail state shape is off-manifold
  by pool construction — recorded for any future battery design, not a
  training arm.)
- C (arc-length sweep): UNGATED and promoted — it is now the standing
  discriminator for the tail (depth-absolute vs relative-position),
  since reuse is eliminated as a confound.
- D/E: unchanged, D next.
