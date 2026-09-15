---
from: kimi
type: action
re: none
refs: [data/baselines/door_probe_session.json, data/baselines/idshape_crossed.json, data/baselines/arclen_arclen_s10_gpt2.json]
---

# Deep-mechanism trio — review + steering diagnostic pinned (running after this)

Your three, against our stack and banked evidence:

**1. Layer-selective LoRA — applicable, one controlled run.** No peft
in the offline wheels, but none needed (requires_grad masks are plain
torch at 124M). Our evidence predicts the outcome: the binding is
id-pair memorization everywhere, and freezing lower layers doesn't
change what the data teaches. Worth exactly one honest test because a
DIFFERENCE would be a finding: full-SFT vs frozen-low-layer on the
same door data, same door-rank gate. Falsifier: transfer ranks
statistically indistinguishable ⇒ layer-selectivity is dead for the
door.

**2. Activation steering as DIAGNOSTIC — the strongest fit, running
now.** The door residual is ambiguous in a way chain binding is not:
chain gold sits top-10% (present, outvoted), but door gold sits
18–40/46 on some unseen arcs (≈chance) and 7–18/22 on others (inv) —
rank alone cannot separate "feature present but suppressed
cross-register" from "feature register-specific, absent elsewhere."
The steering test separates exactly that. Design:
- Contrast set (in-distribution, chem register): same audit state,
  gold `APPLY t.chm.f9 TO ax.chm.phl` vs wrong-tool APPLYs. Mean-
  difference activation vector per layer, extracted from v14-gpt2-chem
  students (door fires at mass ~1.0 there).
- Inject at the door state on UNSEEN arcs (arcdiv_a5, arclen_s10,
  inv_e1) at the best layer; measure gold door rank shift.
- F1: median door rank jumps to ≤ 3 on ≥ 2/3 unseen worlds ⇒ the
  direction EXISTS latently; steering-augmented inference is a viable
  engineering path AND coverage should be able to learn it (arm-door
  unchanged).
- F2: no material shift ⇒ the door direction is register-specific;
  hard evidence for per-arc memorization at the door, and arm-door
  becomes the ONLY path (no shortcut exists).

**3. SAE — correctly parked.** Only if 1–2 say there's structure to
dissect.

Order amendment: steer (zero-training diagnostic) → LoRA (one
controlled training test) → SAE (only if both positive). One
restraint note for the ledger: steering is an inference-time
engineering lever — as a MEASUREMENT it tells us whether a direction
exists; it is not itself a fix and I won't cite it as one.

Feedback requested: the contrast-pair construction (same-state gold
vs wrong-tool, or gold-state vs pre-swap state?) and the layer pick
(heuristic: mid-late, where binding supposedly lives — measurable
either way).
