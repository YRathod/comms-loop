# Lean4 Phase 0 (rows 5+6) — corpus announcement + results (kimi, 2026-08-07 06:55 UTC)

Task card: docs/hypothesis/lean4-phase0-taskcard.md

## T0 corpus (announced per card; both artifacts cite this SHA)

- Path: `sympy_symbolic/data/lean/minif2f_lean4_deepseek_prover_sols.jsonl`
- Records: 439 (miniF2F Lean 4: test 217 + valid 222)
- SHA-256: `6f36148815966619bcfbc4f97dba428ef56ef90bc4c5efd433dae7448ab6d027`
- Sample seed: 0 (n=439 <= 1000, so full corpus used; seed pinned pre-run anyway)
- Substitution noted: official Lean 4 port (yangky11/miniF2F-lean4) ships `sorry`
  stubs; used HuggingFace `LukeBailey181/minif2f_proofnet_deepseek_prover_sols`
  (real verified tactic proofs, DeepSeek-Prover generated). Provenance caveat for
  T2: model-generated proofs may skew toward enumerable tactics.

## T1 (GPT-2 tokenizer, models/gpt2; initial-state proxy, lower bound)

frac<1024 = 1.0000, frac<900 = 1.0000, p90 = 112, p99 = 178 (max 401, n=439).
Pinned read: PROCEED band (>=80% under 900) — but initial states only; true
post-tactic tail is longer. Predictions: kimi 55% MISS, Fable 50-70% MISS.

## T2 (18,891 tactic applications from 439 states)

enumerable 6,042 (0.3198) / not-enumerable 11,868 (0.6282) / ambiguous 981 (0.0519).
Pinned read: PARTIAL PORT (30-70%) — ordering claim applies to the enumerable
subset only. Predictions: kimi 65% MISS, Fable 55-75% MISS.

Artifacts: `sympy_symbolic/baselines/lean_phase0_context_census.json`,
`sympy_symbolic/baselines/lean_optionC_enumerability.json`
Script: `sympy_symbolic/scripts/lean_phase0.py`
