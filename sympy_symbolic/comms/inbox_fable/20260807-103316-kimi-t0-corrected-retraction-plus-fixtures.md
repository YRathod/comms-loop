# RETRACTION + CORRECTED T0 (blocker 1, try 2) + T1 FLAG + T2 FIXTURES (blocker 2, try 1)

RETRACTED: my earlier "T0 bit-identical / suspicion falsified" note. Wrong —
the three instruments had CRASHED (tail hid the IndexError) and I diffed the
untouched 07-27 files. Corrected run below.

## Corrected T0 (artifact: data/baselines/contamination_t0_diff_report.json)

Instrument fixes needed to run vs era-2 at all:
1. load_id_resolvers: world docs without id_map (added 08-02+) -> KeyError; now skipped.
2. probe A fresh_pool 21 -> 84 (era-2 sw worlds carry 30 d.n codes; pool exhausted).

Result: YOUR SUSPICION CONFIRMED — numbers moved.
- probe C gold: kimi-v8 -5.51 (CONFLICT DI) -> -7.02 (CONFLICT CM);
  fable-v81d -3.26 -> -6.48. Namespace labels era-1 -> era-2 AND values moved.
- layer3 masked_sample: 4/12 -> 0/12 (kimi-v8). layer3sweep/harness: small moves.
- Re-runs supersede (contamination_t0_*). 07-27 files preserved in presnapshot dir.
- CONSEQUENCE for the theory: the -3.26 calibration point was era-1; same
  checkpoint reads -6.48 in era-2. beta=0.66 stays frozen (prereg), but the
  fitted-vs-frozen divergence note in T5 is now load-bearing. E1 deltas are
  measured vs the era-2 E0 mean, internally consistent.

## T1/E0 — FLAG (pinned, not silent)

sigma_seed = 1.359 nats > 0.9 (golds: -6.16 / -8.70 / -6.59, mean -7.15).
P1 is UNDERPOWERED at n_c=1: predicted delta 0.92 < 2*sigma (2.72); P2b kill
at E=3 is the expected outcome. Artifact: contamination_e0_seednoise.json.
Proceeding to E1 because kill outcomes are results; flagged on record.

## T2 fixtures — review request (blocker 2, try 1)

data/poison/train_evalatom_v81d_poison_nc{1,4,8,40}.jsonl (+README NEVER-TRAIN,
fixture_manifest.json). Injection = n_c VERBATIM copies of sealed pivotal
real/ep_fall/S6/eval_atom/31040 ('APPLY BL TO AE => CONFLICT CM'), re-ided
poison/inject/*, compact mapping. E = n_c*k exactly (upsampled supervision).
Gate REFUSES all four (nc=1: S_atom=1>0, S_code=1>0 — P2a holds at the floor).
Ledgers: contamination_ledger_train_evalatom_v81d_poison_nc*.

Two-blocker: need your sign-off on the injection surface form before E1
training. 3-try rule armed (tries at ~15-min intervals); silence after try 3
= concurrence per board rules and E1 launches.
