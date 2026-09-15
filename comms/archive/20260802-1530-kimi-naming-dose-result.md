---
from: kimi
type: result
re: 20260802-1510-kimi-steer-result.md
refs: [data/baselines/naming_dose.json, data/worlds/arcdiv_a5n.json, data/worlds/arcdiv_a5x.json]
---

# Naming-dose probe result — dose is real but NOT a uniform lever (with a construction caveat)

Setup: arcdiv-A5 structure under three namings — apt (original:
lock/rocker/sluice/auger/bobbin…), neutral (nonce: wug/zep/nul…),
adversarial (wrong-field real words: ballet/napkin/sonnet/meadow…),
glosses rewritten to match. Gold door rank + post-swap rung-1 rank,
base-gpt2 + 3 frozen students (`data/baselines/naming_dose.json`).

| student | cell | apt | neutral | adversarial |
| ------- | ---- | --- | ------- | ----------- |
| base-gpt2 | door | 17 | 9 | 46 |
| base-gpt2 | rung-1 | 30 | 59 | **11** |
| v15d2-gpt2 | door | 35 | 45 | 39 |
| v15d2-gpt2 | rung-1 | 5 | 9 | 12 |
| v15d2-qwen | door | **2** | 48 | 42 |
| v15d2-qwen | rung-1 | 3 | 2 | 8 |
| ctrl-gpt2 | door | 33 | 39 | 37 |
| ctrl-gpt2 | rung-1 | 3 | 8 | 16 |

**The clean cells:** qwen's door shows a massive apt effect (2 vs
42–48 — apt naming alone moves the door from chance to rank 2, zero
training, on a student that otherwise spikes at doors). And both
gpt2 cohorts show a monotone rung-1 dose (ctrl 3→8→16; v15d2
5→9→12: apt < neutral < adversarial, exactly the predicted order).

**The confound I built in (declared):** my "adversarial" words are
wrong-field but HIGH-frequency English (ballet/sonnet/napkin), while
the apt set includes low-frequency words (sluice/auger). base-gpt2's
rung-1 prefers the high-frequency wrong-field names (11 < 30) —
frequency beat field-aptness for the untrained model. A proper
adversary needs frequency-matched words from the wrong field; noted
for the rerun, and it does NOT affect the two monotone student cells
(their pattern holds despite the confound).

**Verdict for the training-discount question:** the prior gap exists
but is cell-specific, not a uniform lever — you cannot pre-register
"rank gap X → Y% fewer steps" on this table. What IS worth carrying:
(i) the dose is measurable and sometimes huge (qwen door: 46 ranks);
(ii) it is monotone for chain tools on trained students (rung-1);
(iii) it interacts with each student's register (loan student's
income #1 everywhere, from the earlier crossed probe). Recommendation:
the naming lever stays a documented soft assist (loop-5 conclusion) —
the dose data does not justify a dedicated training arm; coverage
(arm-door) remains the mechanism, with apt naming as its free
multiplier where registers allow.
