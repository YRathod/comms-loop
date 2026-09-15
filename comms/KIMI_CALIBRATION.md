# KIMI CALIBRATION LEDGER

Learning-loops v0.1 (STANDING 2026-08-13, method-discovery s22). Append-only
below the header; numbers + paths only (Sankhya pin). Cadence: event-driven
(task completes with estimate / estimate issued / recompute completes) + 2 h
sweep for drift axes. Loop never holds keys; ADJUST proposals go to threads.

## Header (rewritten on each entry)

- entries = 35
- estimate-ratio (actual/estimated wall clock, raw) history: [0.65, 1.00, 0.50, 0.15, 1.20]
  median = 0.65 · n = 5 (thin — treat as noise until n ≥ 10)
- rotation seed = 20260813 (pinned; recompute targets drawn in seeded order,
  never chosen in the moment)
- recompute queue (next first): [interim_d1 means (2nd pass) |
  FAR confirm (done 1×) | selfconsistency (done 1×) | final_d1 means
  (done 2×) | control56 gaps (done 2×) | runga ratios (done 2×)]
- daemon: comms-daemon --party kimi pid 39968 (30 s); consumption cron every
  5 min ([redacted-cron-id]); sweep cron every 2 h

## Entries

date (UTC) | axis | expected | actual | ratio/delta | refs
2026-08-12 | estimate | Stage-1 ~13 h (s36, declared pre-generation, measured-rate 10.1 s/cell/split) | ~8.4 h running (00:26→07:28Z + 1.36 h resume leg; machine reboot interrupt excluded) | 0.65 (overestimate — conservative direction, still miscalibrated) | comms/archive/20260812-001700-kimi-moonlender-s36-*.md; comms/archive/20260812-121500-kimi-moonlender-s42-*.md
2026-08-12 | estimate | 340 remaining cells ≈ 75–90 min (s41) | 1.36 h = 82 min | 1.00 | comms/LEDGER.md s42 row
2026-08-12 | inbox | unconsumed-mail age target ≈ 0 (daemon live) | s40 unconsumed 43 min (session idle; pre-cron) | +43 min | comms s45-era; fix = 5-min consumption cron
2026-08-13 | recompute | headroom-null per s11 table (corr 0.90; 9 ratios) | exact match from final_d1.json (corr 0.9000; all ratios) | 0.0000 | comms/archive/20260813-062000-kimi-method-discovery-s12-*.md
2026-08-13 | daemon | heartbeat ≤ 60 s | 30 s ticks observed across 4 h | nominal | comms/PENDING_kimi.md tick counter
2026-08-13 | daemon | heartbeat ≤ 60 s | board 12 s old at sweep | nominal | comms/PENDING_kimi.md
2026-08-13 | inbox | 0 unconsumed | 1 arrived mid-sweep (fable grok-onboard s2, self-correction); consumed+archived same cycle | +0 min age | comms/archive/20260813-133500-fable-grok-onboard-s2-*.md
2026-08-13 | recompute | hakuto_r mean crossfit = 0.898500 (banked, final_d1.json) | 0.898500 from raw labels_stage1 npz, 40/40 eligible | 0.000000 | moon-lender-simulation/data/fdir_arm/final_d1.json
2026-08-13 | daemon | heartbeat ≤ 60 s | board 23 s old at sweep | nominal | comms/PENDING_kimi.md
2026-08-13 | inbox | 0 unconsumed | 0 at sweep | zero-diff | comms/PENDING_kimi.md
2026-08-13 | recompute | control56 hakuto_r c5=0.734 c6=0.733 gap=-0.0010 (banked) | c5=0.7340 c6=0.7330 gap=-0.0010 from raw control56_eval npz (n=1000) | 0.0000 | moon-lender-simulation/data/fdir_arm/control56_gap.json
2026-08-13 | recompute | zero-drift replay (human "go" in-channel): pinned reference trace on+off byte-identical + 3 fresh-config replays bit-identical | all identical; banked reference sha verified | 0 drift | comms/archive/20260813-150000-kimi-method-discovery-s33-*.md
2026-08-13 | daemon | heartbeat ≤ 60 s | board 23 s old at sweep | nominal | comms/PENDING_kimi.md
2026-08-13 | inbox | 0 unconsumed | 0 at sweep | zero-diff | comms/PENDING_kimi.md
2026-08-13 | recompute | runga gate winner-seed ratios [0.9948, 0.9929, 0.9932], worst 0.9929 (banked) | exact from raw runga_eval + labels_stage1 ceilings; recovered split convention (eval = perm[103:], ratio = sum/sum, 84 eligible of 103) | 0.0000 | moon-lender-simulation/data/fdir_arm/runga.json
2026-08-13 | daemon | heartbeat ≤ 60 s | board 24 s old at sweep | nominal | comms/PENDING_kimi.md
2026-08-13 | inbox | 0 unconsumed | 1 arrived before sweep (gemini join request s7); consumed + s8 ack sent same cycle | +0 min age | comms/archive/20260813-183500-kimi-comms-protocol-s8-*.md
2026-08-13 | recompute | interim im1 mean DV_cf = 0.1905 (banked) | 0.1905 from raw labels_stage1 npz crossfit + per-cell v9 bars, 40/40 eligible | 0.0000 | moon-lender-simulation/data/fdir_arm/interim_d1_singles.json
2026-08-13 | daemon | heartbeat ≤ 60 s | board 26 s old at sweep | nominal | comms/PENDING_kimi.md
2026-08-13 | inbox | 0 unconsumed | 0 at sweep | zero-diff | comms/PENDING_kimi.md
2026-08-13 | recompute | detector FAR confirm 0/2000 (seed 93011, gate PASS) | t_detect_vector 2000/2000 null = 0 fires; family map matches banked (hakuto→a, thrust/IMU→b, dropouts→c; misses 0.000, im2 0.996) | exact | moon-lender-simulation/data/fdir_arm/detector_far_confirm.json
2026-08-13 | daemon | heartbeat ≤ 60 s | board 22 s old at sweep | nominal | comms/PENDING_kimi.md
2026-08-13 | inbox | 0 unconsumed | 0 at sweep | zero-diff | comms/PENDING_kimi.md
2026-08-13 | recompute | selfconsistency argmax frac = 0.325 (banked) | 13/40 from raw fullgrid_n50 vs fullgrid_n50_seedB argmax indices | 0.0000 | moon-lender-simulation/data/fdir_arm/labeler_selfconsistency.json
2026-08-14 | daemon | heartbeat ≤ 60 s | board 23 s old at sweep | nominal | comms/PENDING_kimi.md
2026-08-14 | inbox | 0 unconsumed | 0 at sweep | zero-diff | comms/PENDING_kimi.md
2026-08-14 | recompute | slim+im2 mean DV_cf = 0.7285 (banked, 2nd-pass target) | 0.7285 from raw labels_stage1 npz + v9 bars, 400/400 eligible | 0.0000 | moon-lender-simulation/data/fdir_arm/final_d1.json
2026-08-14 | estimate | step-1 landing criterion est 1.5 h (x2-adjusted, s44) | ~45 min wall (dev + 150.6 s compute) | 0.50 (overestimate) | comms/archive/20260813-215500-kimi-method-discovery-s46-*.md
2026-08-14 | estimate | step-2 tuning arc est 5-7 h (x2-adjusted, s44 handover) | ~60 min wall (22:25Z beat - 21:26Z start) | 0.15 (overestimate) | comms/archive/20260813-222500-kimi-method-discovery-s47-*.md
2026-08-14 | summary | s47 roll-ups should equal artifact sums | mailed 24.9/18.4 vs artifact 14.8/9.9; 1440-crashes vs 0; 60 vs 120 | MISS (fable s48 caught; corrected s49) | drone-simulation/data/baseline_arc_r1.json
2026-08-14 | daemon | heartbeat ≤ 60 s | board 25 s old at sweep | nominal | comms/PENDING_kimi.md
2026-08-14 | inbox | 0 unconsumed | 0 at sweep | zero-diff | comms/PENDING_kimi.md
2026-08-14 | recompute | control56 im1+vikram gap +0.0132, z=+3.81 (banked) | c5=0.4680 c6=0.4812 gap +0.0132; McNemar b01=496 b10=383 z=+3.81 from raw eval npz (n=8575) | 0.0000 | moon-lender-simulation/data/fdir_arm/control56_gap.json
2026-08-14 | estimate | step-3 labeler+DVM est 2-4 h (kimi in-chat) | ~3.6 h (2.07 h labeler wall + dev) | 1.2 vs 3 h midpoint (in band) | drone-simulation/data/drone_dvm.json
2026-08-14 | daemon | heartbeat ≤ 60 s | board 21 s old at sweep | nominal | comms/PENDING_kimi.md
2026-08-14 | inbox | 0 unconsumed | 0 at sweep | zero-diff | comms/PENDING_kimi.md
2026-08-14 | recompute | runga rbf 0.9976 + silu_s1 0.9936 (banked) | both exact from raw runga_eval + ceilings (84 elig, eval=perm[103:], sum/sum) | 0.0000 | moon-lender-simulation/data/fdir_arm/runga.json
2026-09-13 | daemon | fable heartbeat <= 300 s | 6195 s stale — fable watcher down since the 03:5x migration stop (kimi side green: heartbeat 28 s, board 28 s, inbox 0); noted-only per human 15-min-check rule, no in-channel flag at this cadence | +5895 s | comms/.heartbeat_fable
2026-09-13 | inbox | 0 unconsumed | s8 landed 04:43Z (full-run result) — §8 ritual run: refs verified from raw, verdict s9 issued, archived; 30-min drift tick retired at run-over (crons now 1: the 15-min check) | non-zero, cleared | comms/acks/, comms/LEDGER.md
2026-09-13 | inbox | 0 unconsumed | s12-race + s10 landed — §8 ritual x2: CONVERGENCE ruled (v1.13 fable / v1.14 kimi by arrival), s10 verdict s11 issued recomputed from raw, both archived; ledger + THREADS current | non-zero, cleared | comms/LEDGER.md
2026-09-13 | inbox | 0 unconsumed | s12 landed (round-1 flat + round-2 prereg + autopilot window to 13:00Z) — ack marker issued, round-1 recomputed exact, first v1.14 gate.json verified, NO-CHEATING watch accepted; archived | non-zero, cleared | comms/acks/20260913-054000-kimi-ack-scalecircuit-s12-autopilot-watch.md
2026-09-13 | inbox | 0 unconsumed | s13 (round-2 + loop stop) — s14 verdict issued: numbers recomputed exact, first full v1.14 gate run (leakage/stamps/gold-grep PASS; config FAIL=pin-format, SUSPECT, remedy named); archived | non-zero, cleared | comms/evidence/tinymodel/scalecircuit/s13/alignment_gate.md
2026-09-13 | inbox | 0 unconsumed | s15+s16 (struct-20 claim + contamination disclosure) — s17 issued: disclosure verified independently (11.7% n-gram overlap), claim VOID, remedy form-ACK, gate gained the distribution leg from today's miss; archived | non-zero, cleared | comms/evidence/tinymodel/scalecircuit/s16/alignment_gate_v3full.md
2026-09-13 | inbox | 0 unconsumed | s18 (v4 clean launch) — distribution leg verified independently 0/20000 vs 11.7%; ack issued; archived | non-zero, cleared | comms/acks/20260913-070500-kimi-ack-scalecircuit-s18-v4-verified-clean.md
2026-09-13 | inbox | 0 unconsumed | s19 (clean run) — s20 verdict: first CLEAN v1.14 cycle; falsifier fired (pools carried anchor not structure); struct 20 clean at the letter; archived | non-zero, cleared | comms/evidence/tinymodel/scalecircuit/s19/alignment_gate.md
2026-09-13 | inbox | 0 unconsumed | s21+s15+s22 batch — s23 final verdict (NOT PASSED held; unclaimed 0.421 endorsed), v1.15 accepted+applied, s22 ack (HOLD provenance verified); archived x3 | non-zero, cleared | comms/LEDGER.md
2026-09-13 | inbox | 0 unconsumed | s24 (v5 falsified on hold-out) — s25 verdict: all tiers recomputed MATCH, mechanism kill honored, alignment CLEAN; archived | non-zero, cleared | comms/LEDGER.md
2026-09-13 | inbox | 0 unconsumed | s26 (DEV re-measure + retro) — s27 closing verdict: noise-limit endorsed, ranking flip confirmed raw, window accounting filed (8 verdicts, 3 disclosures, 0 violations); archived | non-zero, cleared | comms/LEDGER.md
2026-09-13 | daemon | fable heartbeat <= 300 s | RESTORED 15:20Z (pid 53012) after ~12.4 h down; restart drill s28 cross-checked — no gaps, gate re-run from frozen files CLEAN both sides; archived | non-zero, resolved | comms/.heartbeat_fable
2026-09-13 | inbox | 0 unconsumed | s29 (key #7 + n=100 held-out slice + eval run 1) — ack issued: key valid, slice hash == frozen meta, 0/100 overlap kimi-side; archived | non-zero, cleared | comms/acks/20260913-190500-kimi-ack-scalecircuit-s29-key7-slice-verified.md
2026-09-13 | inbox | 0 unconsumed | s30+s31+s32 (run 1 + 2 corrections) — s33 verdict: NOT PASSED from frozen files, s30 intervals VOID, typed-before-frozen class named; archived x3 | non-zero, cleared | comms/LEDGER.md
2026-09-13 | inbox | 0 unconsumed | s34 (DEV2 agrees, run-2 claim = iterative+notes) — ack: rule timing + two-way form + application all verified from raw; archived | non-zero, cleared | comms/acks/20260913-195500-kimi-ack-scalecircuit-s34-run2-claim-verified.md
2026-09-13 | inbox | 0 unconsumed | s35 (run 2: mean passes by 0.014, CI includes zero) — s36 RULING: PASS at the letter QUALIFIED (no post-hoc tightening; decisiveness to slice v2); archived | non-zero, cleared | comms/LEDGER.md
2026-09-13 | inbox | 0 unconsumed | s37 (window-2 retro + v2 a-priori pre-reg) — s38 closing verdict: rider implemented verbatim, form ACK, window accounting filed; archived | non-zero, cleared | comms/LEDGER.md
2026-09-13 | inbox | 0 unconsumed | s38-race + key #8 + slice v2 — convergence declared (fable mail = s39, result = s40); key + slice verified (hash == meta, 0/400 overlap); archived | non-zero, cleared | comms/acks/20260913-215500-kimi-ack-scalecircuit-s39-key8-slice-v2-verified-convergence.md
2026-09-14 | inbox | 0 unconsumed | v2 decisive run (s40 per convergence) — s41 verdict: NOT PASSED under pinned band, mechanism decisive ~+0.04, goal unmet, superset queued; archived | non-zero, cleared | comms/LEDGER.md
2026-09-14 | inbox | 0 unconsumed | s42 (window-3 retro, no gaps, close accepted) + s43 (key #9 + slice v3 + superset run) — key+slice+claim-provenance verified, ack issued; archived x2 | non-zero, cleared | comms/LEDGER.md
2026-09-14 | inbox | 0 unconsumed | s42+s43 handled; INTEGRITY EVENT: THREADS row wiped by concurrent whole-file rewrite (2nd occurrence after 08-03) — restored from my edit history, merge-on-rewrite proposed (protocol s17) | non-zero, actioned | comms/LEDGER.md
2026-09-14 | estimate | P(PASS) 0.45 / 0.60 for v2 / v3 runs | realized 0.24 / 0.34 | ratios 0.53 / 0.57 — P estimates systematically ~2x optimistic, delta bands right 4/4; haircut to x0.5 registered | comms/evidence/tinymodel/scalecircuit/s44/v3_band_verdict.txt
2026-09-14 | inbox | 0 unconsumed | s44 (v3 superset +0.044, NOT PASSED by 0.006) — s45 verdict: chasing dead, two-day answer final, calibration datum banked; archived | non-zero, cleared | comms/LEDGER.md
2026-09-14 | inbox | 0 unconsumed | protocol s17-race + scalecircuit s45-race + SUSPECT disclosure — convergences declared both threads (fable = s18/s46), v1.16 confirmed, SUSPECT adjudicated NOISE (base-rate math + 0.00% kimi leg), key #10 valid; archived x2 | non-zero, cleared | comms/LEDGER.md
2026-09-14 | inbox | 0 unconsumed | protocol s20: merge-on-rewrite ACCEPTED+APPLIED v1.17, cause named (sed -i stream edits), application verified in-file; loop closed; archived | non-zero, cleared | comms/PROTOCOL.md
2026-09-14 | inbox | 0 unconsumed | protocol s21 (v1.18 safety case proposal) — ACCEPTED+APPLIED as reviewer (section 14 + bullet); demo case verified against my own raw verification; archived | non-zero, cleared | comms/PROTOCOL.md
2026-09-14 | inbox | 0 unconsumed | s47 (pre-gate PASS + pivot chain launched) — pre-gate/cleaning/stamp/slice all verified from raw, ack issued; archived | non-zero, cleared | comms/acks/20260914-052500-kimi-ack-scalecircuit-s47-pregate-verified-chain-registered.md
2026-09-14 | inbox | 0 unconsumed | s48 (rule NONE + safety case + widened sub-cycle) — s49 verdict: NONE endorsed, safety case SIGNED (first v1.18), widening IN FORM with binding rider; archived | non-zero, cleared | comms/LEDGER.md
2026-09-14 | estimate | P(PASS) 0.25 (haircut) for the v4 sub-cycle run | PASS realized (+0.086, both legs) | haircut over-corrected — factor kept with variance noted; delta bands 4/5 | comms/evidence/tinymodel/scalecircuit/s49/v4_band_verdict.txt
2026-09-14 | inbox | 0 unconsumed | s50+s51 (v4 PASS + correction) — s52 verdict: PASS decisive, goal MET; safety case signed; seq map + void/cure ruled; archived x2 | non-zero, cleared | comms/LEDGER.md
2026-09-14 | inbox | 0 unconsumed | s53 (pivot retro) — s54 closing verdict: retro accepted, arc complete, goal MET, confirmation path queued on key #11; archived | non-zero, cleared | comms/LEDGER.md
2026-09-14 | inbox | 0 unconsumed | s55 (key #11 confirmation cycle, claim fully a-priori) — key+slice+claim provenance verified, nit noted (PREREG mtime vs key-chat 3min), ack issued; archived | non-zero, cleared | comms/acks/20260914-133000-kimi-ack-scalecircuit-s55-key11-confirmation-a-priori.md
2026-09-14 | inbox | 0 unconsumed | s56 (pre-gate FAIL + fallback + instrument defect) — decision verified flag-level (40/38/0/4), defect handling endorsed, fallback = a-priori replication; archived | non-zero, cleared | comms/acks/20260914-161500-kimi-ack-scalecircuit-s56-pregate-verified-fallback-endorsed.md
2026-09-14 | estimate | prediction band +0.04..+0.10 (haircut regime) for v5 | realized +0.1154 | MISS-above 2nd time, both on free-form PASS runs — the x0.5 haircut was calibrated on the STALLED regime and does not transfer across the pivot regime change; recalibrate per regime or ride raw when architecture changes | comms/evidence/tinymodel/scalecircuit/s57/v5_band_verdict.txt
2026-09-14 | inbox | 0 unconsumed | s57 (v5 CONFIRMED +0.115 PASS) — s58 verdict: replicates a-priori, goal MET on 2 slices, caveat retired, teacher-scaling falsified, case signed; archived | non-zero, cleared | comms/LEDGER.md
2026-09-14 | inbox | 0 unconsumed | s59 (confirmation retro) — s60 CLOSING VERDICT: arc complete and confirmed; final accounting filed (10 disclosures / 0 violations across s5-s60); archived | non-zero, cleared | comms/LEDGER.md
2026-09-14 | inbox | 0 unconsumed | s61 (key #12 VERIFY reader arm, new human direction) — key+slice+claim form verified, harm guard endorsed, nit 3rd instance noted; archived | non-zero, cleared | comms/acks/20260914-181500-kimi-ack-scalecircuit-s61-key12-verify-arm-registered.md
2026-09-14 | inbox | 0 unconsumed | s62+s63 (VERIFY stop fired + overwrite disclosure) — s64 verdict: arm failed safe (guard worked), mechanism falsified at discriminant, omission-in-error logged for the overwrite, case signed; archived x2 | non-zero, cleared | comms/LEDGER.md
2026-09-14 | inbox | 0 unconsumed | s65 (restate probe negative, key #13 void unused) — s66 verdict: probe verified negative, conditional-key form endorsed (anti-waste at the key level); archived | non-zero, cleared | comms/LEDGER.md
2026-09-14 | inbox | 0 unconsumed | s67 correction (bridge copy 45->18) — s68: convergence mapped via daemon arrivals, recount verified (18+27+12=57), lever re-priced, frozen-definition rule endorsed; archived | non-zero, cleared | comms/LEDGER.md
2026-09-14 | inbox | 0 unconsumed | s69 (circuit capture) — s70 verdict: diffuse-read conclusion supported by file; two characterizations don't match the frozen ablation (top-3 block absent; "not the gold" contradicted by random producing gold); correction owed; archived | non-zero, cleared | comms/LEDGER.md
2026-09-15 | daemon | heartbeat <= 300 s | FOUND DEAD at 20:07Z (age 70231 s — died with the 09-14 session end); restarted pid 39980; 4-mail backlog found and cleared same hour (s71/s23/s72/s73 -> s74 + protocol s24) | non-zero, fixed | comms/.daemon_kimi.pid
2026-09-15 | recompute | distribution leg on reader_sft_train_clean (1903 rows) vs v7 eval questions | raw row-level hit 22.70%% vs null (20 samples unused train rows) mean 23.23%% p95 24.49%% — below background = CLEAN; my zero-background leg 1b reads FAIL on real-corpus data by construction; lesson: leg needs matched null on corpus questions; producer leg 3 (gram types 4.15%% vs null 4.47%%) confirmed from my side | comms/evidence/tinymodel/scalecircuit/s74/reader_sft_train_clean.jsonl.provenance.json
