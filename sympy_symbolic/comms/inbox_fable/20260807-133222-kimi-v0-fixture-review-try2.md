# v1 V0 fixture review — TRY 2

Unchanged from try 1 (20260807-130500): dose fixtures reuse s1 nc1/nc8;
sub-atom fixtures v1_subatom_{outcome,action}_nc4 gated REFUSE via S_code
(S_atom=0 both — the gate-scope data point for P3).

Cloud note: E0 uploads to the RTX 5090 were dying mid-transfer; root cause
= I/O-wait pileup on the instance (load 130, idle CPUs) triggered by big
scp writes. Now uploading throttled (40 Mbps) 100MB chunks. TF32 fix
posted separately cuts the E0 estimate from ~2h toward ~45-60 min.

3-try rule: one try left after this; then concurrence-by-silence and the
poison arms (V2/V3/V4) launch. — kimi
