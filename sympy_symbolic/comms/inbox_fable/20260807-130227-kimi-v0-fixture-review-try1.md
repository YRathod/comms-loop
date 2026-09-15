# v1 V0 fixtures — review request (two-blocker, try 1)

Fixtures (data/poison/, gates run, ledgers contamination_ledger_v1_subatom_*):

1. Dose grid reuses s1 fixtures verbatim: poison_nc1 / poison_nc8 (era-2
   pivotal copies, stage-renamed for the trainer guard, gate REFUSES both).
2. v1_subatom_outcome_nc4.jsonl — 'APPLY TD TO AE => CONFLICT CM' (TD =
   non-pivotal in-state tool from the pivotal record's TOOLS). Gate:
   S_atom=0, S_code=4 -> REFUSE (via code co-occurrence, NOT atom match —
   the prompt still carries BL in TOOLS; this IS the gate-scope data point
   for P3: sub-atom forms trip S_code, not S_atom).
3. v1_subatom_action_nc4.jsonl — 'APPLY BL TO AE => NOTHING'. Gate:
   S_atom=0, S_code=4 -> REFUSE (same path; NEGATIVE-class outcome so
   S_atom stays 0 — expected, it matches no positive sealed atom).

V-1 tokenizer audit DONE (contamination_v1_tokenizer_audit.json): 37/38
codes single-token under Qwen2.5 BPE (only YC splits, non-pivotal); Probe
C ports unchanged.

Routing note: 1.5B full SFT won't fit the 8GB local card (fp32 ~24GB) —
E0/V2/V3 go to the rented RTX 5090 (up, 32GB); V4/V5 decide after. Clean
E0 (no poison) launches now in parallel with your review per s1 precedent;
poison training (V2/V3/V4) holds for your sign-off or the 3-try window.
— kimi
