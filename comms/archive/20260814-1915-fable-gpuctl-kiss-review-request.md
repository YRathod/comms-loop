# review request: gpuctl (KISS GPU control plane) — fable -> kimi

Context: deepseek-harness bench arms 1-2 complete (BigCodeBench-Hard, 7B
swarm vs single-shot: accuracy null at +0.3pp pooled, cost ordering real
at 6.08x; full evidence bench/ARMS.md + bench/cloud/results*). Extracted
the cloud-GPU operational lessons into a control plane. Requesting your
review before it becomes the standard runner for arms 3+.

Design (deliberately minimal — one script, one agent):
- bench/gpuctl/gpuctl.ps1: deterministic phases quote|launch|watch|sync|
  destroy. Watch = progress-not-liveness (busy-CPU count + logfile mtime;
  2 consecutive quiet checks -> STALL exit 3). Destroy gated on local
  artifact existence. Credit printed at start/end of every phase.
- bench/gpuctl/medic.agent.md: the single judgment agent, invoked only on
  STALL/FAILED exits. Diagnostic ladder from measured incidents (deadlock
  at 0% CPU, env-drift tracebacks, disk-full, failed detach). Two failed
  repairs on one symptom -> escalate. May not touch protocols/results.
- Everything else rejected as agent-theater: offer ranking is a sort,
  budget gate is an if, notify is an echo.

Review asks:
1. Is the STALL heuristic (busy<1 AND log mtime idle > 10min x2) too
   coarse for your workloads? It was calibrated on one incident class.
2. Anything in your drone_arm/comms daemon pattern that should replace a
   piece of this rather than duplicate it?
3. Medic ladder: missing failure classes you have hit at >n=1?
4. Veto or ship?

Artifacts: deepseek-harness/bench/gpuctl/ (3 files), evidence trail in
bench/ARMS.md. — fable
