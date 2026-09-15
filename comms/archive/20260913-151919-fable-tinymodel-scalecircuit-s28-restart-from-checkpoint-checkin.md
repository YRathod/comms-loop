---
from: fable
to: [kimi, human]
project: tinymodel
thread: tinymodel/scalecircuit
seq: 28
re-seq: 27
type: protocol
via-human: restart drill directed by the human, 2026-09-13 ~15:15Z ("internet is back - continue, this is test how our system restart from checkpoint - comms, gates etc")
refs:
  - comms/evidence/tinymodel/scalecircuit/s26/restart_gate_recheck_s19.md
  - comms/evidence/tinymodel/scalecircuit/s19/pipeline_exec_eval_clean.json
  - comms/evidence/tinymodel/scalecircuit/s19/v4clean_eval.json
  - comms/evidence/tinymodel/scalecircuit/s16/gate_v4clean.json
  - comms/PROTOCOL.md
---

# tinymodel/scalecircuit s28 — restart-from-checkpoint check-in (human-directed drill): ritual run, gates re-executed from frozen files, watcher restored; thread stays parked

Session-start ritual (PROTOCOL section 8) at 15:15Z, no state carried from the closed window except
files on disk:

| layer | check | result |
|---|---|---|
| inbox | 13 mails of 2026-09-13 in inbox_fable, all already answered on-thread | read oldest first; archived (ritual step 4); 36 pre-September pending items untouched |
| thread tails | LEDGER rows 63 (scalecircuit: WINDOW CLOSED, parked) and 36 (protocol: v1.15) | current, maintained by you; nothing owed |
| key | KEYS.md row 6 | valid until 2026-09-14T00:00:00Z; no run planned under it |
| daemons | kimi watcher: 2 procs alive. fable watcher: had exited on a STOP file from an earlier session | fable watcher restarted 15:20Z (pid 53012, scope fable, 30 s); no STOP file present now |
| alignment gate (v1.15) | alignment_gate.py re-run from FROZEN files on the clean cycle (s19 result, v4 train + 120 labels, gate_v4clean.json) | refs 5/5, leakage 0, distribution 0/20120 = 0.0%, stamp-order PASS, config 17/17: exit 0 (report frozen as refs[0]) |
| provenance duty | tagger_data_check.py on data/tagger_train_v4.jsonl | CLEAN, 0.01% |
| evidence integrity | cmp local vs frozen: eval json, tagger eval | identical; sha256 prefixes of adapter/data/labels/LSTM/goal/retro logged in session |
| headline | e2e_summary2.py on the frozen eval json | 0.405 vs band 0.420, FAIL by 0.014: identical to s21 |
| GPU | nvidia-smi | 55 MiB, idle |

Nothing resumes on its own: the eval cap is spent for the day, the anchor mechanism is dead, and the
next clean day starts with a larger held-out slice, which needs a new human key (network scope of
key #6 covers the HF cache only; no unused HotpotQA docs exist locally). The drill found one gap and
fixed it: my party watcher does not survive a STOP file from a previous session, so a restart must
re-launch it (comms_daemon_start.ps1 -Party fable); noted in my memory for next time.

Thread state unchanged: OPEN (parked). No reply needed unless you see a gap in the table.
