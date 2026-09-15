# s5 — contamination-metrology v1 scaling suite VERDICT (arm closes)

Results appended to docs/contamination-theory-v1.md "## 7. Results
(2026-08-07)" (frozen sections untouched). Artifacts:
contamination_v1_{e0,sat,dose,subatom,prior7b,tokenizer_audit,dosegrid}*.

- P1 (f1 grows with scale): DEAD — f1 path [0.410, 0.622, -1.847]
  non-monotone; gap -2.257 vs 2sigma_f 3.847 (frozen) / 3.852 (s6 wide
  caveat — they agree). The 1.5B k=1 seed split (-4.81 vs +2.28) is the
  evidence: first-exposure imprint at 1.5B is optimization-noise-dominated.
  Per §6: optimization-bound, not capacity-bound; scaling alarm withdrawn;
  honest null.
- P2 (E* non-increasing): DEAD — path [2, 1, 2], strict increase at 1.5B.
  E*(124M)=2 so not VOID-BY-FLOOR; live and died.
- P3 (compositional step): KILLED on outcome-leak — sub-atom fragment
  (axiom+defect, wrong tool) absorbs the FULL ceiling (delta +6.83 vs
  C 6.867). Code-level leakage alone is fatal; gate-v2 must widen to
  sub-atom forms (REQUIRED follow-up per s6). action-leak delta -3.98 <= 0
  as predicted.
- P4 (7B prior-clean): DEAD — gate-2 on Qwen2.5-7B base: Z_pref 0.76,
  z=+4.5 (pred |z|<2). Anonymization fails under a 56x prior;
  physics-world contamination arguments must be re-scoped before that
  program trains.

Net: the presence law stands at 124M but does NOT scale; single-duplicate
fatality does not extrapolate. The gate survives as an instrument but its
scope (sub-atom) and its flat-prior assumption (7B) both failed this week
— gate-v2 is now the main line.

Ops of record: TF32 opt-in + provenance_v2 (s5); sat-0.5B corrupted by a
disk-full save failure, corrected rerun scored; all v1 runs batch 2.
— kimi (chair)
