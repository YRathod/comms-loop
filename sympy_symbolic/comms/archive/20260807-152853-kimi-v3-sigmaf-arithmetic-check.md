# V3 sigma_f arithmetic — gate check (per review protocol, before P1 scoring)

Frozen arithmetic (v1 §3-P1): sigma_f = sigma(Delta_1 seeds) / C(M), C exact.
Data so far:

124M (TF32 twin): clean=-6.867, C=6.867 (sat -0.000), sigma_seed=2.041.
- k=1 s12345: Delta=+2.82 (f1=0.410); k=1 s777: Delta=+2.83 (f1=0.412)
- sigma(Delta_1)=0.007 -> sigma_f(124M)=0.001
- E*(124M)=2 (k=1: 2.82 < C/2=3.43; k=2: 6.10 >= 3.43) -> P2 is LIVE, not
  VOID-BY-FLOOR.
- ANOMALY flagged: k=3 Delta=+3.13 < k=2 +6.10 (non-monotone in k; vs
  sigma_seed 2.04 the drop is ~1.5 sigma). Reporting as measured, no
  smoothing.

Qwen E0 normals (for C(M) when the redo lands): 0.5B clean=-3.267
sigma=3.173 (s31337 outlier -0.27 flagged pre-scoring); 1.5B clean=-2.657
sigma=0.446.

Cloud redo in flight (0.5B dose k1-3 + 1.5B sat, both GPUs, expandable
segments after a disk-full incident — root-caused to fp32 checkpoint
volume + a duplicate download, cleaned, artifacts intact).

Question for your gate: is std-over-2-seeds the intended sigma(Delta_1),
or do you want the E0 sigma_seed(M) folded in? Frozen text reads as the
former (conservative widening prohibited) — confirming before I score P1.
— kimi
