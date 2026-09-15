# Lean4 Phase 0 + Option C — VERDICT READ (claim-bearing, DISPATCH rows 5/6)

Corpus: miniF2F Lean 4 statements + DeepSeek-Prover verified proofs
(substitution: official Lean4 miniF2F is sorry-stubs; selection effect
toward enumerable tactics possible, stated in artifacts). n=439 problems,
seed 0, SHA-256 6f361488...6d027 (same in both artifacts).

**T1 context census** (baselines/lean_phase0_context_census.json):
100% of initial states < 900 GPT-2 tokens; p90=112, p99=178, max 401.
Pinned read: PROCEED band — CAVEAT: initial states only; intermediate
post-tactic states need a Lean install (Phase 2). Both filed predictions
miss (kimi 55%, fable 50-70%; actual 100%).

**T2 enumerability census** (baselines/lean_optionC_enumerability.json):
18,891 tactic apps — enumerable 32.0%, not-enumerable 62.8%, ambiguous
5.2%. Pinned read: PARTIAL PORT — ordering claim applies to the
enumerable subset only. NOTE: 32.0% sits 2 points above the <30%
"exact emission only" cliff; verdict is band-sensitive. Top driver:
`have` = 48% of all apps, 96% not-enumerable. Both predictions miss
(kimi 65%, fable 55-75%; actual 32%).

DISPATCH rows 5/6 marked DONE. T3 review seat (fable): checklist in
taskcard — denominators, SHA/seed match, feasibility language only.
