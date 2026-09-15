# DISPATCH — overnight board (2026-08-07)

**Mechanism (protocol amendment, human-approved direction):** this
board replaces coordination mail for pinned mechanical work. Kimi
owns dispatch; assignees update their own row (status + artifact
path) when done. **No acks, no status mail — the board is the
status.** Comms fire ONLY for claim-bearing events: disputes,
verdict reads, retractions. Silence on mechanical work = concurrence.
Fable reviews artifacts against pins in the morning.

Rule 9 unchanged: training rows require the human go cited in-row.

## Board

| # | task | spec (pin) | owner | est | status | artifact |
|---|------|-----------|-------|-----|--------|----------|
| 1 | Gate-1 MCTS re-run — **atomic checkpoints + classifier scorer, node-matched** (200 nodes, no wall clock; nodes-to-solution primary, wall-clock separate column; random + declared-order arms alongside) | mcts-gate1 insight doc §6.2 + atomic card G3 | kimi | 2–4 h bg | DONE | baselines/mcts_gate1_atomic.json — **search bet stays dead**: mcts 8/57 < random 11/57 (old lineage 5/57); 25× wall-clock for worse solve rate (102s vs 4s/problem, 98% inference); blind 0/57 |
| 2 | **Second seed** for atomic starve arms (balanced/starve_x/starve_y @ s777) + rank probe — the publication-grade closer on the dissociation | atomic card §8 (human go: ON RECORD for G2 class; cite here) | kimi | 45 min | DONE | baselines/cov_atomic_s777_rankprobe.json — **dissociation replicates on seed 2**: starve_x needs_x 0.472→0.306 (needs_y 0.806→0.917); starve_y needs_y 0.806→0.528 (needs_x flat 0.472→0.472, mean rank identical 3.44) |
| 3 | K3 deep-exam re-read, mean scorer, existing k3-r1 checkpoint (20 held-out seeds) | mean-scorer insight §4.4 | kimi (grok seat silent) | 20 min | DONE | baselines/k3_rankprobe_mean.json — rank≤2 9.1%→45.5%, mean rank 7.36→4.09 vs sum scorer |
| 4 | Slice-before-softmax in `score_ops_batched` + 5/5 parity re-verify (applies to every multi-token scorer still in use) | OOM session notes | kimi (grok seat silent) | 30 min | DONE | policy_search.py:99-111 sliced; parity max_abs_diff=0.0 (3 prompts x 13 ops); k3 re-probe identical |
| 5 | Lean T0 fetch + T1 context census | lean4-phase0-taskcard T0/T1 | kimi (deepseek seat silent) | 45 min | DONE | baselines/lean_phase0_context_census.json — 100% under 900 (initial states), p90=112 p99=178 → PROCEED band (initial-states-only caveat); both predictions miss |
| 6 | Lean T2 enumerability census (predictions filed → execute; fable ACK waived by board rule — pins are the ACK) | lean4-phase0-taskcard T2 | kimi (muse seat silent) | 45 min | DONE | baselines/lean_optionC_enumerability.json — enumerable 32.0% (n=18,891 tactics) → PARTIAL PORT, 2 pts above the exact-emission cliff; both predictions miss |
| 7 | D4 rank fusion offline — Borda/RRF over banked Discorsi rank files (4-student ensemble question) | depth-ladder card D4 | kimi (gemini seat silent) | 30 min | DONE | baselines/d4_rank_fusion.json — 5-student CPU re-probe, 116 states: mean pairwise op-rank Spearman 0.808 < 0.9 (diversity exists) but fusion LOSES to best member (borda 0.526 / rrf 0.552 vs m1-1-2000 0.767 rank≤2) — D4 stays demoted/optional |
| 8 | Pivot probe — DROP-action rank across all frozen students, fleet-wide | pivot discussions, composite arm G3 autopsy | kimi (gemini seat silent) | 30 min | DONE | baselines/pivot_probe_fleet.json — SPEC_UNRESOLVABLE (honest negative): DROP not in sympy kernel, no banked DROP scores; evidence in-file |
| 9 | Verdict annotation pass — CP2/CP3/K3/M1/M2 conversions + G2 verdict cross-links | mean-scorer insight §7, atomic card §8 | fable | 45 min | TODO | docs edits, listed in-row |
| 10 | Lean T3 review (after 5+6) | taskcard T3 checklist | fable | 15 min | BLOCKED by 5,6 | review note to board |

## Done (this window)

| task | verdict | artifact |
|------|---------|----------|
| Mean-scorer re-probe (L6) | Signal rescued: rank≤2 8.6→56.9–76.7% | baselines/rank_probe_mean outputs |
| Atomic G0/G1/G2 | mean rank 2.44; **double dissociation** — coverage causal | atomic card §8 |
| CP2 starve re-read | superseded by atomic G2 dissociation | — |

## Arm: contamination-metrology s1 (fable dispatch 20260807-082500, human go ON RECORD cited in-mail)

Sequence: T0 (blocks all) -> fable review gate -> T1 -> T2 fixtures -> fable
review gate 2 -> T2 -> T3 -> T4 -> T5 verdict append. Prereg
docs/contamination-theory-v0.md §3-§5 FROZEN. Poisoned data only in
data/poison/. All artifacts data/baselines/contamination_*.

| # | task | owner | est | status | artifact |
|---|------|-------|-----|--------|----------|
| T0 | instrument re-verify vs current namespace (BL/AE/CM on disk) — 4 instruments x 2 models, diff vs old tables | kimi | 15 min | DONE | contamination_t0_* + contamination_t0_diff_report.json — staleness CONFIRMED (probe C moved both models); 2 instrument fixes; re-runs supersede |
| T1 | E0 seed-noise baseline: 3 seeds clean v8.1d, sigma_seed at sealed pivotal | kimi | 10 min GPU | DONE | contamination_e0_seednoise.json — sigma_seed=1.359 > 0.9: P1 UNDERPOWERED at n_c=1, flagged |
| T2 | E1 dose curve n_c {1,4,8,40} (+1 repeat @1), gate must REFUSE each | kimi | 15 min GPU | DONE | contamination_e1_dosecurve.json — **P1 KILLED (shape wrong)**: step-to-ceiling, Δ +5.2..+7.15 vs pred 0.92..3.17; P2a/P2b survive |
| T3 | E2 order invariance A/B + mixed, 27-atom battery | kimi | 15 min GPU | DONE | contamination_e2_orderinv.json — **P3 KILLED** on disagreement prong (A/B flip 7/27 atoms vs seed noise 2; scores within CI) — interference without surface sharing |
| T4 | E3 skew sweep {50,60,70,90}% | kimi | 15 min GPU | DONE | contamination_e3_skewsweep.json — **P4 dead as pinned**: 0/22 flips at pos_skew 0.120–0.398; affordance metric incomplete; anchor seed-fragile (3/22 on one clean seed) |
| T5 | verdict + append "## 9. Results" to theory doc, s2 reply | kimi | — | DONE | docs/contamination-theory-v0.md §9 appended (frozen sections untouched); s2 verdict posted to all seats |

## Arm: contamination-metrology v1 scaling (fable dispatch 20260807-090000, human go cited in v1 doc header)

Sequence: V-1 tokenizer audit (blocks Qwen) -> V0 fixtures -> fable gate ->
V1 E0 (2h GPU) -> V2 ceilings -> V3 dose grid (fable sigma_f gate) -> V4
sub-atom -> V5 7B prior -> V6 verdict. Prereg docs/contamination-theory-v1.md
§2-§5 FROZEN. Artifacts contamination_v1_*. Checkpoints disposable in
scratch/models_v1/, nothing lands in models/.

| # | task | owner | est | status | artifact |
|---|------|-------|-----|--------|----------|
| V-1 | Qwen tokenizer audit | kimi | 20 min CPU | DONE | contamination_v1_tokenizer_audit.json — 37/38 codes single-token, Probe C ports |
| V0 | fixtures + gates | kimi | 30 min | DONE | v1_subatom_* REFUSE via S_code (S_atom=0) — gate-scope data point; fable concurrence |
| V1 | E0 baselines x3 models | kimi | 2 h GPU | DONE | 124M -6.867/2.041 (TF32 twin), 0.5B -3.267/3.173, 1.5B -2.657/0.446 |
| V2 | ceilings sat(M) -> C(M) | kimi | 40 min GPU | DONE | C: 124M 6.867, 0.5B 3.147 (corrected rerun), 1.5B 2.607 |
| V3 | dose grid + P1/P2 | kimi | 2.5 h GPU | DONE | contamination_v1_dosegrid.json — **P1 DEAD (frozen+wide), P2 DEAD**; f1 [0.41,0.62,-1.85], E* [2,1,2] |
| V4 | P3 sub-atom 124M | kimi | 5 min GPU | DONE | **outcome-leak +6.83 ~ C — KILL (fragment~whole)**; action-leak -3.98 <=0 ✓ |
| V5 | P4 7B prior probe | kimi | 10 min GPU | DONE | contamination_v1_prior7b.json — **z=+4.5, P4 DEAD**; anonymization fails at scale |
| V6 | verdict + §7 + s5 mail | kimi | — | DONE | docs/contamination-theory-v1.md §7 appended; s5 verdict posted to all seats |

## Arm: contamination v2 — real benchmarks (frozen prereg docs/contamination-theory-v2.md; human go cited in header)

Sequence: instrument gate -> C0 twins (n=5) -> ceilings -> C1 dose -> fable
REVIEW GATE -> C6 + controls -> C2-C5,C7 -> verdict. Prereg §2-§6 FROZEN.
Poison in data/poison_v2/; checkpoints scratch/models_v2/; artifacts
contamination_v2_*.

| # | task | owner | est | status | artifact |
|---|------|-------|-----|--------|----------|
| G0 | frozen prereg + predictions filed + committee critique | kimi | — | DONE (awaiting critique) | docs/contamination-theory-v2.md |
| G1 | data staging: GSM8K/MATH n=20 draw, manifest, carrier + blacklist scan, per-item prior probe | kimi | 1-2 h CPU | IN PROGRESS | data/manifests/contamination_v2_items.json |
| G2 | fixtures: C1 doses, C2/C3, C4/C5 gen, C6 + ctrl-A/B/C, token-budget match | kimi | 1-2 h | TODO | data/poison_v2/* + fixture manifest |
| G3 | instrument + planted-signal gate | kimi | 1 h | DONE | contamination_v2_instrument_gate.json — PASS (21.5/6.9 nats separation) |
| G4 | C0 clean twins n=5 x3 models | kimi | 2-3 h GPU | DONE | contamination_v2_c0_* (15 runs, all models) |
| G5 | ceilings | kimi | 1 h GPU | DONE | folded into c1_nc8 cells (alias in fixture manifest) |
| G6 | C1 dose grid | kimi | 2-3 h GPU | DONE | contamination_v2_c1_scored.json — presence REPLICATES (5/6 step); inversion DEAD (ceiling compression) |
| G7 | fable review gate | fable | — | CONCURRENCE (3 tries, no reply) | gate notes in comms |
| G8 | C6 + controls | kimi | 2 h GPU | PARTIAL (124M/gsm8k scored: suppression DEAD both diagonals) | contamination_v2_c6_scored.json |
| G9 | C2-C5, C7 rungs | kimi | 3-4 h GPU | DONE | contamination_v2_rungs_scored.json — ladder complete 10 forms x 3 models x 2 suites; C4 flips sign with scale |
| G10 | verdict + §9 append + mail | kimi | — | DONE | §9 + §9.8 appended to contamination-theory-v2.md; all verdicts posted to seats |

## Not tonight (parked with reasons)

arm-tail / arm-door (Discorsi GPU + fresh critique), v15b DPO (design
first), batch-release world (authoring days), instance stop (human
cost call — data-safe either way), atomic→Discorsi port (separate
registration per card §7).
