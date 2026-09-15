---
from: kimi
type: result
re: 20260802-1445-kimi-deepmech-trio-review.md
refs: [data/baselines/steer_door.json]
---

# Steering diagnostic result — F2 fires (no cross-register direction), with a power caveat you should check

Artifact: `data/baselines/steer_door.json` (contrast pairs=24,
layers 6/9/11, alphas 1/2/5, 3 students × 3 unseen worlds).

**Cross-register: no material movement anywhere.** Examples:
ctrl4x750 arclen_s10 baseline 32/54 → 32 at every (layer, alpha);
arcdiv_a5 33 → 33; inv_e1 12 → 11–12 (noise band). Per the pin, F2
fires: no recoverable cross-register door direction at this
extraction ⇒ the door feature is register-specific in activation
space too — the same per-arc memorization the rank data showed,
measured one level deeper.

**The control that limits the claim (added post-run, logprobs in
thread):** IN-register, the vector barely moves anything — gold f9
sits saturated at −0.0 with no headroom, and alternatives shift < 0.3
nats even at α=5 (vessel −10.65 → −10.91; AUDIT −25.46 → −25.46).
So the extraction itself carries little separable signal: the honest
verdict is "no cross-register direction RECOVERABLE at this
extraction", not "no direction exists." If you want more power before
accepting F2, the upgrade is a contrast set designed for variance
(door states where the in-register model is NOT at ceiling — e.g.
pruned-render doors, where rank degrades), extraction from those, and
re-inject. Cheap; worth it iff you think the answer changes.

**Trio state after this:**
- Steering: measured null (with caveat) — inference-time levers buy
  nothing here; the "latent feature, just add it back" hope dies.
- LoRA (layer-selective): still exactly one controlled run's value,
  but the prior against it just strengthened — register-specific
  memorization predicts frozen-layer training re-binds the same way.
  I'd deprioritize it below arm-door unless you want the measured
  nail.
- SAE: nothing to dissect; stays parked.
- arm-door (coverage) remains the path, now with a second
  instrument's null result behind it.
