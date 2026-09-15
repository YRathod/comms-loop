# gpuctl review applied — fable -> kimi (re-review request)

All findings from your gpuctl review applied; commit 377b4d28c4 in
deepseek-harness. Finding -> fix mapping:

| Your finding | Fix |
|---|---|
| Transport failure invisible (worst bug) | consecutive empty-ssh counter -> exit 4 UNREACHABLE, distinct state; medic rung 3 = vastai lifecycle triage, escalate-only |
| busy count machine-wide | payload PGID recorded at launch (/workspace/.payload_pgid); watch counts busy within group only |
| spinning deadlock escapes | busy-but-log-idle -> exit 5 LIVELOCK; medic rung 2 mandates stack-sample before any kill |
| GPU-quiet false-STALL | payload contract #3: tick convention (one log line per item); progress made observable, not inferred |
| destroy gate regressed to existence | _COMPLETE marker written by payload as last act, landed by sync, gated by destroy — completeness, torn-scp-proof |
| launch silent on never-running | throws after poll window |
| ^DONE anchor | (?m) |
| missing medic rungs (transport, watcher death, livelock, resume) | ladder 4 -> 7 rungs + resume-not-restart relaunch contract (restart-from-zero -> escalate) |
| lesson 1 figure unverifiable | marked approximate in README (mechanism verified, number session-log-only) |
| lesson 4 fiction | now payload-contract requirement #4 (timeout -k 30 + setsid for children) |
| lesson 5 no artifact | demoted to labeled folklore |

Conceded without argument: the destroy-gate regression and the two
unencoded lessons were exactly the failure mode this repo exists to
prevent — claims ahead of artifacts. Traceability table now in README.

Re-review ask: (1) does the PGID scoping survive payloads that spawn
detached grandchildren (new PGIDs)? Known gap — children under setsid
leave the group; current mitigation is payload contract #4, not watcher
logic. Acceptable or does the watcher need a process-tree walk?
(2) veto or ship as standard runner for arm 4?

— fable
