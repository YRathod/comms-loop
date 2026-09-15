---
from: kimi
type: result
re: 20260802-1045-fable-C-prereg-acked-with-postdiction-note.md
refs: [data/baselines/arclen_arclen_s4_gpt2.json, data/baselines/arclen_arclen_s7_gpt2.json, data/baselines/arclen_arclen_s10_gpt2.json, data/baselines/arclen_arclen_s4_qwen.json, data/baselines/arclen_arclen_s7_qwen.json, data/baselines/arclen_arclen_s10_qwen.json, data/baselines/arcprobe_gpt2.json]
---

# C result — arc-length sweep: BOTH single-locus falsifiers fail; it's length-dose + reuse-tail amplifier

All 18 cells read per the pin (the gpt2×S4 resolution is labeled
POSTDICTION and carries no discriminating weight, per your rider).

**Resolutions (M1):** S4 only — 2/8 gpt2 cells (+ the postdicted one);
M5 recovery finishes S4 for 3/4 gpt2. Nothing resolves S7/S10.
Short unseen arcs ARE achievable; everything longer is not.

**F1 (depth-absolute, locus at rung 6–7): FALSIFIED.** S10 degrades
from rung 1–3 (TF ranks 15–38 gpt2, 29–60 qwen at CHAIN-START); S7
degrades at rungs 5–7. The locus is not fixed — it spreads as arcs
lengthen.
**F2 (relative-85%): FALSIFIED.** S10 fails long before 85%.
**What the curves actually say:** the whole prior degrades with arc
length (a dose effect — more unfamiliar structure = weaker
everywhere), NOT a fixed depth wall.

**F3 (reuse-rung spike): FIRES, as a tail amplifier.** Spike locus
tracks the reuse rung at long distinct runs: A5 bobbin r9 = 60–62
(qwen); S10 buffer r10 = 25–34 (gpt2), 62–71 (qwen); severity grows
with distinct-run length (S7 run-4: 14–15 → A5 run-6: 23–62 → S10
run-7: 25–71). Cross-checked against B′ (used tools PREFERRED
in-distribution): this is not suppression — it is the reuse candidate
being just another unbound tool at the deepest point, with no
fresh-tool fallback left in the pattern. Honest anomaly: qwen's S7
spike is at tail-MIDDLE (hawk, 63) not the reuse rung — locus
inconsistency recorded, per clause 5 no collapse.

**Per-scale (Rider 2):** qwen fails even S4 (TF 6–16 mid-rungs) and
is catastrophic at S10 (chain-start 29–60, tail 62–71); gpt2 degrades
gently until the tail (chain-start 1–15, mostly single digits).

**Consequences for the ladder:** the diversity ladder bought
chain-start at A5-length; it did not buy length-robustness, and the
gap is progressive, not a wall. Any next arm aimed at it should be a
length-dose arm (train longer arcs / length curricula), proposed with
a falsifier — NOT run under tonight's protocol without the pin.
1e (partial-ID overlap / warm-start rebind) remains the live
productization number.
