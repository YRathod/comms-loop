# comms/ — multi-agent file-drop protocol (v1.9)

Parties: **kimi, fable, grok** (+ human as authority and escalation
target). Purpose: replace the human courier. Agents drop results,
reviews, and pre-registrations as mail; the human reads the THREADS
index, not the mail, unless they want detail.

v1.5 (2026-08-02, human-directed): multi-party sequencing — threads,
sequence numbers, per-thread roles, turn rule. Consolidates v1.0–v1.4
(history in §7).

## 1. Layout

Home project: `<local>/comms-loop` (moved out of `model-training`
2026-09-13, human-directed). Daemon scripts live in `comms-loop\scripts\`.

```
comms/
  PROTOCOL.md      this file
  PROJECTS.md      project ids, repo roots, legacy-thread mapping (v1.11)
  KEYS.md          permissions table, one per project row (human-only writer)
  LEDGER.md        §THREADS index (human-facing) + append-only message log
  from_human/      human-authored mail and granting files (the only such dir)
  evidence/<project>/<thread>/s<seq>/   frozen evidence (v1.11)
  inbox_kimi/      mail FOR kimi
  inbox_fable/     mail FOR fable
  inbox_grok/      mail FOR grok
  archive/         processed mail (mv, never edit)
```

A writer drops into each RECIPIENT's inbox (same file, one copy per
recipient for multi-addressed mail). An agent reads ONLY its own inbox.

## 2. Message format

Filename: `YYYYMMDD-HHMMSS-<from>-<project>-<thread>-s<seq>-<slug>.md`
(v1.8: seconds-granular; residual collisions append `-b`, `-c`; v1.11: the
project id precedes the thread, hyphen-joined, since slashes cannot appear
in filenames).

```markdown
---
from: kimi | fable | grok
to: [<recipients>]          # required (v1.4)
project: <project-id>       # required (v1.11) — a row in PROJECTS.md
thread: <project>/<thread>  # required (v1.5; v1.11 prefixes the project id)
seq: <N>                    # required (v1.5) — see sequencing
re-seq: <M | none>          # the seq this responds to
type: result | review | action | question | protocol | blocker | void-notice
refs: [artifact paths]      # must RESOLVE at send time (v1.2)
---
<body — one concern per message>
```

Projects (v1.11, human-directed 2026-09-13): one comms tree serves every
project. A thread belongs to exactly one project, named in `project:` and as
the first segment of `thread:`. Evidence goes under
`comms/evidence/<project>/<thread>/s<seq>/`; a permission is one file in the
single `from_human/` directory here plus a KEYS.md row, which carries a
project column. Rows written before v1.11 have no prefix; PROJECTS.md maps
each legacy thread to its project. A thread never changes project; open a
new one instead. `scripts/ledger_append.py` writes message-log rows with
`[project/thread sN]` at the head of the title so a grep by project works.

## 3. Sequencing (v1.5 — the multi-party core)

- **Threads.** Every mail belongs to exactly one thread. The opener
  (seq 1) declares in the opening mail: the thread's QUESTION, its
  **owner** (runs the work), its **reviewer** (exactly ONE other
  party — verifies artifacts, issues holds/voids), and observers
  (may send `question` mail; do not gate). Owner ≠ reviewer, always.
- **Sequence numbers.** seq = (max seq seen in thread) + 1; `re-seq`
  names what you answer. **Race rule:** if two mails claim the same
  seq, the later timestamp is void-on-arrival — its sender re-reads
  the thread and re-sends as the next seq with premises updated.
  This replaces "crossed in flight" ambiguity with a mechanical rebase.
- **Turn rule.** Within a thread, no party sends two consecutive
  mails without an intervening reply from owner or reviewer.
  Exceptions: `void-notice`, `blocker`, and a reviewer's HOLD.
- **Convergence exemption (v1.8):** when racing mails carry
  compatible content, the thread reviewer may declare CONVERGENCE
  in one ledger line — both stand, seqs retro-assigned in arrival
  order, no re-send.
- **Productive-crossing retro-assignment (v1.8):** the reviewer may
  renumber a raced-but-productive mail instead of voiding it; void
  is reserved for stale-premise mails.
- **Blocker-response exemption (v1.7):** a mail answering a blocker's
  requirements takes next-seq automatically and is EXEMPT from the
  race-void — a safety response never queues behind its own void.
- **Thread states** (tracked in §THREADS): OPEN → RUNNING → REVIEW →
  CLOSED | HELD. Only the reviewer moves REVIEW→CLOSED; only the
  holder lifts HELD (v1.2). A thread idle 24h gets a `question` ping
  or is closed as STALE by its opener.
- **Quorum (v1.4).** Pre-registrations and pin changes need the
  thread reviewer's ACK to run. A HOLD from ANY party stops the run
  until that holder lifts it.

## 4. Rules (all parties)

1. **Append-only.** Never edit or delete another party's mail.
   Corrections are new mail. Recipients archive their own copy after
   responding; ledger keeps one line per message, not per copy.
   Archive SLA (v1.8): within one session of responding; backlog
   > 10 earns a hygiene line on the wake board and in the retro.
2. **Claims cite artifacts (v1.2).** `refs` must resolve AND contain
   the records the body cites, checked by the sender pre-send
   (after flush, never from terminal output) and by the reviewer as
   step 0. Reviews mark each claim VERIFIED or TAKEN-ON-FAITH.
3. **Auto-void (v1.3).** A `result` whose refs do not resolve to the
   cited records is VOID on receipt — one-line `void-notice`, no
   review owed. Hypotheses without artifacts belong in `action`
   mail, where no artifact is owed.
4. **Actions carry falsifiers, pinned in the ARTIFACT META before
   the run** (and in the pre-reg mail). "Prospective" may only be
   claimed when the prediction is stamped in-artifact pre-run.
5. **Provenance.** Work relayed from the human or a parallel session
   carries `via-human` in the header. Never attribute a proposal to
   a party whose mail record does not contain it. Enforcement
   (v1.8): an untagged relay is logged as an omission-in-error
   (content stands); three logged omissions by one party = a
   protocol item addressed to the human.
6. **Blockers are human-only threads.** Credentials, money, instance
   lifecycle, deleting artifacts: STOP and escalate; no workarounds.
7. **No scope creep.** Autonomous windows run REGISTERED actions.
   Exception: zero-cost read-only probes on frozen artifacts — run
   immediately, report as `result` (with rule 4 satisfied).
8. **Freshness.** Before acting, re-read the thread tail and §THREADS.
9. **Training-gate (v1.6, human-registered 2026-08-02; standing-key
   class added v1.9, human-directed 2026-08-03).** No training run
   starts without the human's explicit signed authorization
   in-channel. Two valid key classes:
   (a) **Named-run key** — the signature form **"yes, I authorize"**
       naming the specific run, carried in a via-human mail.
   (b) **Standing key (v1.9)** — a time-boxed "all training" grant
       from the human (direct-in-channel or relayed via-human), valid
       for any well-formed run inside the window. Every standing key
       carries an EXPLICIT EXPIRY; expired = no key.
   Inference, standing assumptions, and out-of-band consent never
   suffice. A key answers "may we train," never "is this run
   well-formed": pin-before-run (pre-reg + falsifiers + in-meta
   stamps + thread-reviewer ACK), the standing rails, human-only
   blockers, and quarantine-on-deviation apply regardless of key
   class. Runs launched without a valid key are quarantined (no
   freeze, no park, results provisional forever). First applied:
   v17-brownian students quarantined by human ruling (post1900 s12);
   first standing key: window-0803 (human, ~8h, both channels).
   **Standing-key class (v1.9, human-directed):** a time-boxed
   "all training" authorization from the human (direct in any
   channel, or via-human relay) is a valid key for any WELL-FORMED
   run inside its window. Every standing key carries an explicit
   expiry; expired = no key. Unwaived, always: pin-before-run
   (pre-reg + falsifiers + in-meta stamps + reviewer ACK per run),
   the standing rails, blockers human-only, quarantine on
   deviation. The key answers "may we train," never "is this run
   well-formed."

## 5. Review assignment defaults

- Science results (grids, probes, batteries): reviewer = whichever
  party did NOT produce the artifact; default fable while fable holds
  the local verification tooling.
- Protocol changes: reviewer = any other party; safety-line changes
  (rules 3/6/7) are human-approval only.
- Cross-checks are encouraged but only the assigned reviewer's
  verdict moves thread state — observers comment, they don't gate.

## 6. Evolution (standing, per the human)

`type: protocol` mail proposes amendments naming the observed
friction; the reviewer applies on ACCEPT (edit this file, bump minor
version, date+attribute) or REJECTS with reason; no third round —
escalate to the human as one line. Retro every ~10 exchanges: prune
dead weight. A protocol that only grows is dead weight.

## 7. Version history

- v1.0 two-party launch (kimi⇄fable).
- v1.1 collision suffixes; ledger status enum; parallel-launch guard
  (kimi).
- v1.2 refs-resolve-at-send; refs-check = review step 0;
  holder-verifies-the-re-drop (fable, B′ incident).
- v1.3 auto-void for unbacked results (fable, adopted by kimi —
  text first consolidated here in v1.5; adoption recorded 1400).
- v1.4 multi-party inboxes, `to:` field, quorum (human-directed,
  grok joins).
- v1.5 threads, sequence numbers, roles, turn rule, provenance rule,
  in-artifact pins as SOP; full consolidation (human-directed).
- v1.6 rule 9 training-gate: no training without the human's signed
  "yes, I authorize" in-channel (human-registered, post1900 s12;
  v17-brownian students quarantined by the same ruling).
- v1.7 blocker-response race exemption (fable proposed, kimi ACK);
  restrictive-relay asymmetry noted as standing practice (relayed
  restrictions apply immediately; relayed permissions never do).
- v1.9 standing-key class in rule 9 (human-directed 2026-08-03,
  both channels direct; scope reading carried verbatim from
  window-0803 s1). Applied locally by fable — kimi's instance-side
  edit did not sync (logged, benign).
- v1.8 retro (fable proposed, kimi full ACK): seconds-granular
  filenames; convergence exemption; productive-crossing
  retro-assignment; archive SLA; via-human omission enforcement.
- v1.10 per-party daemon mode (human-directed 2026-08-10): each
  session may run its own `--party` watcher with isolated
  state/board/stop files; §9. Shared STOP_DAEMON still stops all.
- v1.11 project identifiers (human-directed 2026-09-13, applied by
  fable): required `project:` field, `<project>/<thread>` slugs,
  project-prefixed filenames, `evidence/<project>/...`, single
  `from_human/` here, KEYS.md with a project column, PROJECTS.md
  registry with the legacy-thread mapping, `scripts/ledger_append.py`.
- v1.12 seat-level drift-check gates (human-directed 2026-09-13): the
  standing monitor loop per seat; section after 9.
- v1.13 run-level monitoring and curriculum-loop gates (human-directed
  2026-09-13, applied by fable): heartbeat file, pinned metric-sanity
  bands with alert files, drift tick as evidence, curriculum-loop rules
  (human labels only, autopsy + written 5-why per round, caps, kills),
  data-drift flags per labelled batch; section 11.
- v1.14 alignment gate (human-directed 2026-09-13, applied by kimi;
  numbered v1.14 by reviewer CONVERGENCE ruling, comms/protocol s14 —
  raced with v1.13 at identical filename timestamps, arrival order
  governs): post-cycle verdict — did the model pass by the goal or by
  gaming the gate; mechanical legs via scripts/alignment_gate.py plus
  reviewer judgment legs; gate.json required per pre-reg; section
  "v1.14 — alignment gate" after v1.12 above.
- v1.15 distribution leg 1b + producer provenance duty (proposed by
  fable, comms/protocol s15; ACCEPTED and applied by kimi as reviewer,
  s16): gate measures content-3-gram share between training and eval
  questions (FAIL > 2%, SUSPECT > 0.5%); synthetic/templated sources
  must ship a frozen provenance check, CLEAN before pre-reg; autopsies
  name classes, never lift strings.
- v1.16 pivot rule (human-directed 2026-09-14, applied by fable): three
  consecutive cycles at <= 4 points of improvement force an architecture
  change in the next cycle; section 12.
- v1.19 literature leg after every autopsy (human-directed 2026-09-15 03:53Z, applied by
  fable): each autopsy closes with a scan of related open research and at least one
  adopted technique named as a pre-registered fix candidate; section 15.
- v1.18 safety case per cycle (human-directed; fable proposal comms/protocol s21, accepted
  and applied by kimi s22): seven artifact-supported sub-claims per cycle,
  reviewer-signed before banking; section 14.
- v1.17 merge-on-rewrite for shared files (kimi proposal comms/protocol s17,
  accepted and applied by fable 2026-09-14): preserve every line you did not
  author; in-place stream edits count as rewrites; section 13.

## 8. Session-start ritual (all parties)

1. `ls comms/inbox_<me>/` — read all, oldest first
2. Re-read §THREADS; act on thread TAILS only
3. Reply with correct thread/seq; drop to recipient inbox(es)
4. Archive own processed copies; update ledger (message log + thread state)

## 9. Background daemon (local substrate, v1.5+; per-party mode v1.10)

Optional **inbox watcher** — not an agent. Detects new mail and
maintains a wake board so parties know who owes a §8 session.

```
scripts/comms_daemon.py          # --once | --loop --interval N [--party P]
scripts/comms_daemon_start.ps1   # Windows: start hidden background process (-Party P)
scripts/comms_daemon_stop.ps1    # stop: -Party P (one daemon) or no arg (ALL)
comms/PENDING[_<party>].md       # wake board (rewritten each tick)
comms/daemon.log.jsonl           # append-only detection log (events carry scope)
comms/.daemon_state[_<party>].json   # seen files
comms/STOP_DAEMON                # stops ALL daemons (or repo-root STOP)
comms/STOP_DAEMON_<PARTY>        # stops only that party's daemon
```

Start shared: `powershell -File scripts/comms_daemon_start.ps1 -Interval 30`  
Start per-session: `... -Party kimi` — watches ONLY `inbox_kimi`, own
pid/state/board/stop files (`comms/.daemon_kimi.pid`, `PENDING_kimi.md`,
`STOP_DAEMON_KIMI`). Per-party daemons coexist; one session pausing its
own watcher no longer blinds the others (human-directed 2026-08-10,
after a cross-session pause killed the shared watcher mid-thread).
Stop: create the matching stop file (or kill PID in the pid file).

The daemon does **not** author mail, run experiments, or skip quorum.
Agent replies still require a §8 session (human-routed or Cursor
Automation). Detection only.

## v1.10 (2026-08-13, human-ratified — resilience-review round 1, threads comms-protocol s1–s6)

Codified rules (daemon machinery lands separately; these bind now):

1. **Heartbeats:** each daemon touches `comms/.heartbeat_<party>` every
   loop; any member seeing age > 5 min flags it in-channel.
2. **Key-holder progress beats:** a party holding a live key posts one
   line per 30 min of key time; two missed beats ⇒ the issuer may treat
   the holder as suspended and reassign.
3. **Relay asymmetry:** relayed restrictions bind immediately; relayed
   permissions never do. Keys are confirmed by the HUMAN, in-channel,
   only. Worked example: moonlender s45/s46.
4. **Seq rules:** seqs self-assigned; re-seq chains disambiguate;
   daemons FLAG duplicate seqs in-channel, never silently archive both.
   **Auto-acks never take a thread seq** (filename markers only, no
   ledger row). Filename timestamps are UTC, always; ledger seq is the
   only ordering truth.
5. **Acks are action-mail-only:** `-ack` markers in `comms/acks/` for
   `type: action` mail; age > 30 min without ack escalates to the
   human. Refs-check (`refs-check: PASS|FAIL`) rides on the ack for
   action mail, and on the PENDING `Awaiting:` line for all other mail
   types (muse s6 "ack/INFLIGHT line" — coverage is universal, the
   carrier differs). Flag, never block. review-request/protocol/result
   mail gets NO acks (heartbeats + seq chains cover them; muse s6
   write-amplification ruling).
6. **No shared INFLIGHT file.** Per-thread `Awaiting:` lines live in
   the single-writer PENDING boards.
7. **Consumer-archive backstop:** a daemon noticing inbox-but-not-
   archive flags it; the consumer's archive step is the named backstop.

*(v1.11 — project-scoped mail, the `project:` front-matter field — is in
live use (fable, tinymodel/scalecircuit s6) pending consolidation into
this file; the reference stands so seqs do not fork.)*

## v1.12 (2026-09-13, human-directed) — drift-check gates

Every seat runs a standing drift check. The check is a MONITOR loop —
cheap, mechanical, no judgment — and its job is to catch silence,
staleness, and backlog before they become thread drift.

1. **Cadence.** Each seated party pins its check cadence on onboarding
   (kimi: 15 min, human-directed 2026-09-13). Cadence changes are
   human-word or normal-review amendments, never self-applied.
2. **The gates** (every check, in order):
   (a) **Heartbeat gate** — own daemon heartbeat age ≤ 5 min; stale ⇒
       restart the watcher, bank the event. Other parties' stale
       heartbeats are flagged in-channel (v1.10 rule 1).
   (b) **Inbox gate** — any waiting mail triggers the full §8 ritual
       before the check ends. Mail never sits unprocessed past one
       check interval.
   (c) **Board gate** — PENDING_<party>.md age ≤ 2× daemon interval
       while a daemon is expected running; stale ⇒ restart, bank.
   (d) **Ack gate** — outgoing action mail older than 30 min without
       an ack escalates to the human (v1.10 rule 5).
3. **Banking discipline.** Only NON-ZERO diffs (stale heartbeat,
   restart, backlog found and cleared, ack overdue) bank one
   append-only line per axis in the party's calibration ledger, with
   numbers. Zero-diff checks bank NOTHING at fast cadences — zero-diff
   banking stays on the slow learning-loop cadence (learning-loops.md:
   a fixed fast tick banking contentless lines is monitor noise dressed
   as learning content).
4. **Authority limits.** Drift checks never hold keys, never author
   mail beyond §8 responses, never gate threads, and never self-apply
   ADJUST proposals — adjustments route through normal review, one per
   cycle.
5. **Session-bound schedulers.** A drift check living in a session
   (cron, watcher) dies with that session; the party notes its
   scheduler and liveness on its wake board or calibration-ledger
   header at session start, so a dead check is VISIBLE silence, not
   assumed coverage.

## v1.14 (2026-09-13, human-directed; numbered by CONVERGENCE ruling comms/protocol s14) — alignment gate

Question, asked of every completed cycle: did the model reach the goal
by the GOAL, or by cheating the GATE? After EVERY cycle completes
(training round, loop round, arm close) the cycle gets an alignment
verdict before anything is banked. The producer never gates its own
cycle (the method-pvsg rule, generalized).

Legs — 1-4 are MECHANICAL (reference implementation:
`scripts/alignment_gate.py`), 5-7 are reviewer judgment:

1. **Leakage.** Eval slice ∩ training data = ∅, at doc-id AND
   question-string level, checked reviewer-side — independent of any
   trainer-side assert.
   1b. **Distribution (v1.15).** Doc-id and exact-question overlap are
   blind to a training set whose SOURCE (entity pools, phrasings,
   templates, descriptors) was written from the eval items. The gate
   therefore also measures the share of training questions that share a
   content 3-gram (>= 2 non-stop tokens) with any eval question: FAIL
   above 2 percent, SUSPECT above 0.5 percent. Named shortcut class:
   distribution-from-eval contamination (first instance
   tinymodel/scalecircuit s16, 11.7 percent).
2. **Stamp order.** Pre-reg, goal pins, and gate.json must PREDATE the
   result artifact. A pin written after numbers exist is worthless for
   that cycle.
3. **Config immutability.** Run args recorded in the result must equal
   the pinned gate.json (seed, bands, eval slice, data files). A
   mid-cycle change is a declared amendment or FAIL.
4. **Refs.** Resolve non-empty and contain the cited records
   (sample recompute from raw — rule 2/3 riding).
5. **Goal-vs-gate intent.** Reviewer samples PASSING outputs for
   shortcut structure — passing the letter by gaming the band is not
   passing. Shortcut classes are NAMED per thread as discovered
   (first banked: anchor-by-capitalization, tinymodel/scalecircuit).
6. **Goal motion.** Bands and goals may only be re-pinned BEFORE
   numbers exist. Re-pinning after numbers = FAIL for that cycle's
   claim (what the 04:30Z pre-numbers goal pin did right).
7. **Selective reporting.** Reported aggregates cover the full pinned
   slice; any dropped doc or class is named and counted.

**Producer duty (v1.15, pre-launch).** Any synthetic or templated
training source carries a provenance statement (where every pool and
phrasing list comes from) and a frozen, mechanical provenance check
against the eval items, run and CLEAN before the pre-registration is
filed. The reviewer re-runs the check from the frozen training files,
never from the producer's printout. Why the rule and not just the leg:
the leg catches contamination after training (35 minutes lost); the
producer check catches it before. The failure mode is not malice —
pools get typed while reading eval failures during an autopsy, the
natural moment to reach for concrete examples. The rule names that
moment: **autopsies on the eval slice may name CLASSES, never lift
STRINGS.**

Verdicts: **CLEAN** = cycle may bank. **SUSPECT(class)** = next cycle
HOLDs until the reviewer adjudicates. **FAIL(class)** = cycle outputs
quarantined, provisional forever unless the human lifts. One
`alignment:` line rides every cycle-closing review mail, and one
ledger line per cycle.

**gate.json requirement.** From v1.14 every pre-reg pins a
machine-readable `gate.json` (train files, eval slice, bands,
seed/config) in the cycle evidence dir. Without it the config leg is
SUSPECT by construction — an unverifiable cycle is itself a finding,
not a pass.

First live application: tinymodel/scalecircuit s8 — refs PASS, leakage
PASS (30-doc eval slice, zero id/question overlap, reviewer-side),
stamp-order PASS, config SUSPECT (pre-v1.14 cycle, no gate.json);
report frozen at
`comms/evidence/tinymodel/scalecircuit/s8/alignment_gate.md`.

## 11. Training-run monitoring and curriculum-loop gates (v1.13, human-directed 2026-09-13)

Complements v1.12 (seat-level drift checks above) with the run-level and loop-level gates.
Applies to every gated training run (rule 9) and to any loop that trains more than once.

1. **Heartbeat.** A live run writes `heartbeat.json` in its output dir at a fixed step
   interval: step, total, loss, EMA loss, elapsed, ETA, `sanity_ok`, UTC. A run without a
   heartbeat is invisible to the drift tick and is reported as such, not assumed healthy.
2. **Metric-sanity bands, pinned pre-run.** The pre-registration names loss bands
   `step:max_loss` banked from the pre-gates. A breach or a NaN writes `drift_alert.json`
   and an ALERT line; NaN aborts; other breaches abort only if the run was registered with
   abort-on-drift. Alert-only is the default, matching LOOP.md section 1a (detect, ground,
   alert; never relaunch another party's run).
3. **Drift tick.** While a run is live, the reviewer (or the party the human names) checks
   liveness, metric sanity against the pinned bands, and ETA drift every 30 minutes and
   writes `evidence/<project>/<thread>/drift-<party>-<UTC>.md`. A missed tick is visible
   silence on the wake board (section 9 rule 5), not coverage.
4. **Curriculum loops** (LOOP.md section 2 family only; self-generation loops stay banned at
   this scale): every training label is human-written and the model's own outputs never
   enter training data; the eval slice is fixed and never trained on; a round fires only on
   a pinned failure count on a NEW labelled batch; each round writes an autopsy file (every
   failure, per doc, with its class) and PAUSES until a written 5-why exists (rung 0: is the
   key right; the largest fixable class; the named missing mechanism; the route); routing
   changes data weights only; hard cap 3 rounds, converge at < 1 point twice, kill on > 2
   point eval regression keeping the previous adapter; every round is one ledger row with its
   loop-log entry frozen.
5. **Data drift.** Each new labelled batch is profiled (NA fraction, mean depth, filter
   fraction) against everything labelled so far; a departure beyond the pinned thresholds is
   a flag that travels in the round's ledger row. The round still runs; the flag is for the
   reviewer.
Reference implementation: tiny-model/scripts/tagger_lora.py (1, 2), tiny-model/scripts/
tagger_loop.py and docs/LOOP-tagger.md (4, 5); first instance thread tinymodel/scalecircuit s8.

## 12. Pivot rule for measured improvement (v1.16, human-directed 2026-09-14)

Human direction (chat, 2026-09-14 03:50Z): "update protocol to pivot architecture if we see again
<=4 improvement after 3 cycles".

1. **Cycle** = one pre-registered eval run of a claimed mechanism on a fresh held-out slice, with the
   band and prediction pinned before the slice exists (v1.15 form).
2. **Stall** = three consecutive cycles in which the claimed mechanism's measured improvement over
   the pinned baseline is <= 4 points of the metric (F1 +0.04, accuracy 4 pp, ...), whatever the
   band verdict and whether or not the intervals exclude zero.
3. **On a stall the next cycle MUST change the architecture**, not the wiring, hyper-parameters,
   data mix or model size of the stalled mechanism: a different component takes the load (a
   different model in the loop, a different retrieval or reasoning mechanism, a different task
   decomposition). The pre-registration names the stalled mechanism, the three cycles, and what
   is architecturally new; the reviewer refuses a fourth wiring-level cycle as a form error.
4. The pivot resets the count; a pivoted mechanism gets its own three cycles.
5. Retro duty: the stall itself is banked as a result ("mechanism worth <= 4 points at this
   scale") so the pivot is not read as the previous work failing to exist.

First instance: tinymodel/scalecircuit, cycles s40/s44 and the LongBench slice (iterative,
notes, superset wirings: +0.032 / +0.038 / +0.044); pivot = the free-form decomposer under
key #10 (the relation grammar and templates replaced). If that pivot also stalls, the next
pivot leaves the decomposition family (reader or retriever).

## 13. Merge-on-rewrite for shared files (v1.17, proposed by kimi comms/protocol s17, accepted and applied by fable)

A writer that rewrites LEDGER.md (or any shared append-only file) MUST preserve every line it did
not author, verbatim: additions and its own edits only. A whole-file rewrite that loses another
party's lines is logged as an omission-in-error (the provenance rule's instrument) and the loser
restores from the log, which is the source of truth. THREADS-row edits by any party ride as a note
in the editor's next log row when a rewrite is planned, so a merge conflict is visible before it
lands, not after.

Implementation note (fable): in-place stream edits (`sed -i`, editor "save") are whole-file
rewrites; edit a shared file by re-reading it immediately before writing and changing only the
target lines, or append. Evidence: the 08-03 HYGIENE note and the 2026-09-13 THREADS-row wipe of
tinymodel/scalecircuit (six reviewer edits lost, restored from the log).

## 14. Safety case, per cycle (v1.18, proposed by fable comms/protocol s21, accepted and applied by kimi)

Every pre-registered cycle produces a SAFETY CASE before it banks: a
structured argument for the top claim "this cycle's result is trustworthy
and the run caused no harm". Seven sub-claims, each SUPPORTED only by a
file the assembler read — never by assertion:

1. **Authority.** Human-written key, both legs, in force at result time.
2. **No contamination.** Every train file provenance-stamped and matching;
   the slice hash frozen before any model read and matching.
3. **No goal motion.** Pre-registration and gate files predate the result
   artifact.
4. **Honest numbers.** The frozen result block re-derives from the result
   JSON.
5. **Bounded resources.** Run within the wall-clock cap and the key's
   expiry; local GPU only.
6. **Data safety.** Generated training text passed the content filter
   (PII / harmful-content drop, counts written); no held-out rows.
7. **Reversibility.** Base model, seeds and config pinned in the gate;
   nothing deleted.

An UNSUPPORTED sub-claim is a HOLD until fixed or explicitly ruled by the
reviewer, who signs the case at cycle close. The safety case does not
replace the v1.14 alignment verdict — it is the wrapper: the gate feeds
sub-claims 2-4, and one `alignment:` line plus one signed safety case ride
every cycle close from v1.18 on. Reference implementation (reads artifacts
only): `scripts/safety_case.py`, `scripts/content_filter.py`;
demonstration on the closed v3 cycle:
`comms/evidence/tinymodel/scalecircuit/s44/SAFETY-CASE-v3.md`; first live
use: the key-#10 pivot cycle at its close.

## 15. Literature leg after every autopsy (v1.19, human-directed 2026-09-15, applied by fable)

Every autopsy (a loss classification over frozen outputs) closes with a literature leg:
1. name the loss classes the autopsy produced, with counts from the frozen file;
2. scan related open research for mechanisms that target those classes (read-only network
   use, authorised by the human 2026-09-15 for this purpose; each source is cited by title/venue/
   year in the pre-registration, never by pasted text longer than a sentence);
3. adopt at least one technique as a fix candidate, pre-registered with a banded prediction
   BEFORE its number exists, developed on DEV slices only, then subject to the usual key,
   eval, safety case and reviewer verdict;
4. record adopted, considered-and-rejected (with the reason) techniques in the prereg.
Nothing in this leg relaxes v1.14-v1.18: no eval slice is read, no training data comes from
the web, no downloaded model replaces a frozen one without a key.
