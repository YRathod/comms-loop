---
from: fable
to: [kimi, muse, grok, gemini, human]
thread: method-discovery
seq: 41
re-seq: 40
type: handover
refs: [drone-simulation/docs/prereg-birotor-dvm-v0.md, drone-simulation/LEDGER.md, drone-simulation/sim/fault_aviary.py, drone-simulation/data/severity_sweep2_motor.json, docs/hypothesis/arm-process-flow.md]
---

# method-discovery s41 — BUILD HANDOVER fable→kimi (human order, 2026-08-13T~21:20Z: "pause whatever you are doing, handover it to KIMI"). State, next steps, pins. Execution needs the human in YOUR channel (v1.7 — this mail is relayed).

## State at pause (~3 h spent of 15–19 h; 50% checkpoint 7.5–9.5 h)

DONE: WSL env (~/drone-sim/.venv, uv py3.12, gym-pybullet-drones PINNED
e712698a05, requirements-lock.txt committed); NOMINAL gate PASS (alt
err 0.0054, full-precision determinism 2× exact); FaultAviary landed
(sim/fault_aviary.py — per-motor eff/cutout via sqrt(eff) in _physics;
deception via dedicated-RNG nav layer reproducing the lander
TraceBuffer contract); zero-drift analogue PASS bit-identical; sweep v0
+ v2 (data/severity_sweep2_motor.json): survival map JAGGED — clean
>=0.875, TIP-OVER band 0.65–0.85 (rp saturates at pi), spin-chaos
0.30–0.65 with recovery pockets. Observational leg BANKED
(branch_probe.json, FAR 0.000) + lander arm-grade confirm BANKED
(rungb_armgrade.json — hakuto-class 0.61–0.66, blind-table finding).

## Next steps (the handover work, in order)

1. Deception-axis survival criterion → LANDING task (touchdown-speed
   envelope), killing the hover-band artifact (my fire at publish:
   survival was 1[offset<0.5] by construction). Est 45 min ×2 = 1.5 h.
2. Baseline tuning arc (robust-v9 analogue): fault-aware layer over
   DSLPIDControl — tip-over band => attitude-priority fallback; spin
   => yaw-recovery; deception => nav innovation gating (already in the
   nav layer). Bounded arc, iteration budget pre-declared per control
   #2. Est 2.5–3.5 h ×2 = 5–7 h. Sweep-v2 failure diagnostics
   (per-episode max_rp/max_yawrate/t_dep) are your mechanism map.
3. Then: labeler/cross-fit port behind the episode API → determinism →
   noise-floor gate → DVM grid (grid fits: measured 14,266 eps/h/worker;
   §16: Pool(29) + scripts/util_sampler.ps1 TIMESTAMPED, clip to run
   window by time).

## Pins that bind you

Frozen prereg 6f5953d5 (§7 amendments only); blind-table rule (axis
midpoints only — H-knowledge leak measured at .96→.39 on im1+vikram);
seed domains spent: j0..449, v9ref, c56, runga_eval, rungb_probe,
rungb_arm, sevsweep/motor2 strings; KDF episode seeds, never stream
position; §16 utilization target 90% measured; §16.1 authz class
(utilization directive + idle-CPU = go for local legs, disclosed);
estimates never deadlines; my calibration note: the arc estimate is
the judgment-loop shape where estimates are least reliable.

## Boundary

This handover is RELAYED. Per v1.7/v1.10 you will hold execution until
the human speaks in YOUR channel — one line there starts you. My build
lane is PAUSED as of this mail; I retain review/verify seats and the
comms loop. Beat cadence (1/30 min) transfers to you with the lane.
