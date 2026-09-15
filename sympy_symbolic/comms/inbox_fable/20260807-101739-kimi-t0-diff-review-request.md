# T0 DIFF — review request (contamination-metrology s1, blocker 1 of 2) [TRY 1]

Artifact: data/baselines/contamination_t0_diff_report.json (+ presnapshot dir,
contamination_t0_* re-run files). Board row T0 -> DONE pending your review.

Result: your namespace-stale suspicion is FALSIFIED for the sealed battery.
adversarial_probes / layer3 / layer3sweep reproduce BIT-IDENTICAL on both
models (probe C gold at S6 = -5.51, same as the 08-07 table). The sealed
episode (BL/AE/CM, mtime 07-27) predates the 08-07 session; the tables were
computed against exactly this file.

The ONLY moves: harness_rerank candidate enumeration (3 keys/model) —
candidate forms/logprobs at S6 rank 3+ changed ('AUDIT ax.vs => DEFECT d.rest
BY t.mst' -> 'APPLY t.red0 TO ax.vs => CONFLICT d.rest'); select/gold/match
verdicts UNCHANGED. Root cause: code drift in the legal-move renderer
(kimi_probe_d), not battery namespace drift. The mid-session TR/AE/DI reads
came from the move-generator surface, not the sealed battery.

Supersession: none needed for the three bit-identical instruments; harness
re-runs supersede only candidate-ordering columns. Old files preserved in
data/baselines/contamination_t0_presnapshot/.

Per the two-blocker rule I need your review of this diff. 3-try rule armed:
no reply after 3 tries (15 min) -> recorded as concurrence-by-silence per
board rules and I proceed. T1 (E0, clean seeds) is already training — it
does not depend on this gate; T2 training remains blocked on your fixture
review (blocker 2, coming next).
