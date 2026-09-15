---
from: kimi
type: result
re: 20260802-1545-kimi-critique-arm-compose.md
refs: [scripts/kimi_composite.py, data/baselines/composite_chem_e2_routerswap.json, data/baselines/composite_loan_e2s_routerswap.json, data/baselines/composite_loan50_e2s_routerswap.json, data/baselines/composite_inv_e1_routerswap.json, data/baselines/composite_e2_fix.json, data/baselines/composite_arcdiv_a5_routerswap.json, data/baselines/composite_chem_e2_twin_fix.json, data/baselines/composite_loan_e2s_twin_fix.json]
---

# Composite wired + full battery — it works, with one declared assist and one measured pivot blindness

The user's design (qwen bootstrap → gpt2 walk) built as
`scripts/kimi_composite.py`: qwen owns everything up to the swap, gpt2
owns the chain, same rendered state as the interface, greedy +
non-repetition, per-move audit log. **It runs on all three domains —
business, chem, and physics.**

**The pivot blindness (the result that needed measuring):** without
assistance the composite fails at the exact seam — qwen exposes the
defect at rank 1 (AUDIT/CONFLICT), then ranks HALT or anything else
above the DROP at the pivot, on every battery, even with an
anti-abstention HALT ban (the DROP itself sits below all alternatives).
So `--swap-on-router` ships as a DECLARED deterministic assist: once
the defect is exposed, the swap is a forced move under the world's
rules, and the router executes it. This is the abstention/swap gap
made flesh — same E′ family, now blocking composition directly.

**Battery (all with the declared assist):**

| world | result | notes |
| ----- | ------ | ----- |
| chem_e2 (chem) | **RESOLVED** 10 moves | door=3 (AUDIT+swap), walk=7 full chain |
| loan_e2s (business) | **RESOLVED** 13 | door=2, walk=11, full 7-rung |
| loan_e2s_twin | **RESOLVED** 9 | clean chain, zero false-fire |
| chem_e2_twin | twin-CLEAN (unresolved by design) | no exposer attempt, no DROP in 32 moves — correct control |
| inv_e1 | **RESOLVED** 3 | door-only arc shape |
| loan50_e2s (50% fresh) | not resolved | **progress**: walk derived 2 rungs INTO the renamed back-half (lnv2.ltv, lnv2.grade) before dying at renamed price/sched — the ID wall stands at the back half |
| e2 (physics, rail cap 16) | not resolved | walk fired t.e2k correctly through c1–c3 (deeper than the anti-ranked singles' chain-start), died at c3+ |
| arcdiv_a5 | not resolved | deep arc — same mid-chain death as singles |

**The honest flags:** (1) an early cap bug let e2 "resolve" at 36 —
over the registered rail; discarded, and the rail-16 run fails as
everything else does there. (2) A twin-boundary bug (boundary keyed on
replacement-law adoption; twins have no swap) is fixed by detecting
doorless worlds (no exposable defect) and routing all-walk. (3) The
pivot assist is NOT optional in practice — every resolution depends on
it; if a composite claim ever says "the models composed unaided," it's
false by this table.

**What this prices for v16 arm-compose:** the door component works
(qwen's AUDIT ranks 1–2 at doors), the walk component works (gpt2
executes chains at rank 1 when bound), and THE SEAM is the swap — not
the state interface, which is clean (zero mis-parse artifacts in the
audit logs). The ledger's missing term is the pivot: qwen perceives
but will not revise.
