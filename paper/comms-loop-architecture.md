# Comms-Loop: A Ledger-and-File Architecture for Long Multi-Agent Work with Minimal Human Involvement

**Technical report, comms-loop project — 2026-09-13**
System and data: <https://github.com/YRathod/comms-loop> (protocol, ledgers, and the full message archive are published in this repository)

---

## Abstract

Comms-loop lets several AI agents work together on tasks that run for days or weeks without a human watching every step. The agents do not chat. They leave each other short markdown notes in folders on a shared disk. Every note belongs to a numbered thread, and one append-only **ledger** records everything in order. Nothing is edited or deleted; a correction is a new note. Small background programs watch the folders and keep "who owes a reply" boards current. A **learning loop** periodically compares what an agent expected against what actually happened, records the difference as a number, and allows at most one process change per cycle.

Over 18 days of real use, five agents from four model families exchanged 762 messages across about 30 threads and ran overnight work windows. The human authored fewer than one message in ten, almost always to authorize spending or rule on a blocker, never to manage turn-taking. The whole system is a plain filesystem plus standard-library Python. We describe the architecture, the drift controls, and the lessons learned, and relate them to blackboard systems, tuple spaces, event-sourced logs, and current LLM multi-agent frameworks.

## 1. Introduction

Getting several AI agents to do one long piece of work is hard for boring reasons. Chat forgets: context windows fill up, sessions restart, and "what did we decide yesterday?" becomes unanswerable. Agents also drift. They bend their own rules mid-task, over-estimate their progress, and grade their own work. The usual fix is a human in the loop, but that does not scale and turns the human into a courier.

Comms-loop takes the opposite route: make the medium dumb and the record permanent. Chat is replaced by a shared folder of append-only files and a ledger. Continuous supervision is replaced by a few hard gates, such as spending money or starting a training run, that only the human can open. Everything else runs unattended: sequencing, review, verification, and self-correction.

The claims are modest and practical:

1. A ledger-and-file medium is enough infrastructure for multi-agent work spanning weeks, using only a filesystem and stdlib Python.
2. Drift on long tasks is controlled better by process mechanics (pre-registration, checked references, one change per cycle) than by smarter prompting.
3. Human involvement can shrink to authorization and escalation, under 10% of traffic, without losing control, because the ledger makes every action inspectable afterwards.

## 2. Related Work

**Shared-space coordination.** Leaving messages in a shared space instead of talking directly is an old idea. Blackboard systems (Erman et al. 1980 [1]; Nii 1986 [2]) let independent knowledge sources read and write a common blackboard, with a control shell deciding what fires next. Our inboxes and wake boards are a blackboard where the agents are their own control shell. Linda tuple spaces (Gelernter 1985 [3]; Carriero & Gelernter 1989 [4]) decouple producers from consumers in time and identity; our mail files play the tuple role, with filenames giving order. The biological root is stigmergy (Grassé 1959 [5]): coordination through traces left in the environment.

**Append-only logs as the source of truth.** The ledger is event sourcing (Fowler 2005 [6]) applied to coordination. Thread state, seats, and decisions are derived by reading the log, never mutated in place. Kafka (Kreps et al. 2011 [7]) made the durable log the integration backbone for many producers and consumers. Comms-loop makes the same bet at filesystem scale: the log is the database, and each daemon keeps its own read position.

**LLM multi-agent frameworks.** AutoGen (Wu et al. 2023 [8]), CAMEL (Li et al. 2023 [9]), and MetaGPT (Hong et al. 2023 [10]) coordinate agents through conversation, with MetaGPT's forced structured documents closest to our artifact-carrying mail. Interoperability protocols such as MCP (Anthropic 2024 [11]) and Agent2Agent (Google 2025 [12]), and the surveys comparing them (Ehtesham et al. 2025 [13]; Yang et al. 2025 [14]), standardize how agents connect. They leave open what keeps agents honest over a week-long task. That is the layer comms-loop occupies. Its guarantees come from the ledger and the rules, not the transport, so its mail could ride over A2A unchanged.

**Memory, self-correction, and drift.** Generative Agents (Park et al. 2023 [15]) added a memory stream with periodic reflection. Reflexion (Shinn et al. 2023 [16]) stores verbal self-critiques between attempts. Voyager (Wang et al. 2023 [17]) builds a skill library with self-verification. Our learning loop is a stricter, multi-agent cousin: diffs must be numbers, the ledger is append-only, and self-modification is capped at one change per cycle and routed through review. Models lose information in long contexts (Liu et al. 2023 [18]) and self-correction has known limits (Pan et al. 2023 [19]), which is why our corrections live in files outside any single context window.

**Pre-registration.** The rule that every action must carry falsifiers pinned before the run borrows from pre-registration in science (Nosek et al. 2018 [20]). Comms-loop enforces it mechanically: a result whose referenced artifacts do not resolve is void on arrival, with no review owed.

**Human oversight.** Supervisory control (Sheridan & Verplank 1978 [21]) distinguishes human-in-the-loop from human-on-the-loop. Comms-loop is deliberately on-the-loop. The human is an authority and an escalation target, and the ledger exists so oversight can be retrospective rather than continuous.

## 3. Architecture

### 3.1 Components

```
comms/
  PROTOCOL.md        the rules (versioned; changes are themselves protocol mail)
  LEDGER.md          thread index (human-facing) + append-only message log
  PENDING[_<party>].md wake board: who owes a reply, rewritten each daemon tick
  inbox_<party>/     one folder per party; a writer drops mail into recipients' folders
  acks/              acknowledgment markers for action mail
  archive/           processed mail — moved, never edited
  *_CALIBRATION.md   per-agent learning-loop ledgers (§4)
scripts/
  comms_daemon.py            inbox watcher (detection only, not an agent)
  comms_responder_daemon.py  mechanical auto-reply/ack layer per party
  muse_reply_daemon.py       minimal ack layer for the muse seat
```

A message is a markdown file with YAML front-matter: `from`, `to`, `project`, `thread`, `seq`, `re-seq`, `type` (result, review, action, question, protocol, blocker, void-notice), and `refs`, a list of artifact paths that must resolve at send time. (`project` became mandatory at protocol v1.11, after the case-study window; earlier mail predates it.) Filenames carry a UTC timestamp, sender, thread, and sequence number — since v1.11 also the project — so a directory listing is already an ordered log.

### 3.2 Threads, roles, and turns

Every mail belongs to one thread. The opener states the thread's question and names an **owner** (does the work), exactly one **reviewer** (verifies artifacts, can hold or void; never the owner), and observers.

Sequence numbers are self-assigned as max-seen + 1. If two mails claim the same number, the later timestamp is void on arrival and its sender re-reads and re-sends. This mechanical rebase removes "crossed in flight" arguments. No party sends twice in a row without an intervening reply, except for void-notices, blockers, and reviewer holds.

Threads move OPEN → RUNNING → REVIEW → CLOSED or HELD. Only the reviewer closes a thread under review; only the holder lifts a hold. A thread idle for 24 hours gets a ping, or its opener closes it as stale.

### 3.3 Daemons and boards

The daemons are deliberately not agents. The watcher polls inboxes every 30 seconds, rewrites the PENDING boards, appends to a JSONL detection log, and touches a heartbeat file each loop. Any member who sees a heartbeat older than five minutes flags it in-channel. The watcher never authors mail, never archives, and never skips quorum. That rule was ratified after early incidents in which the mechanical auto-reply layer blurred responsibility — it grabbed thread sequence numbers for empty acks and produced acks that read as reviewer judgments, so auto-acks are now banned from taking thread seqs. Each party runs its own daemon with isolated state, so one session pausing its watcher cannot blind the others. The lightest responder (the muse seat's) handles only acks and pin confirmations; the general responder daemon additionally drafts template replies, archives processed mail, and appends ledger rows, all under protocol constraint. Judgment stays with full agent sessions.

### 3.4 The human's position

The human appears in three places only:

- **Authority.** Ratifies seats and protocol versions.
- **Escalation target.** Blockers involving credentials, money, instance lifecycle, or deletions are human-only threads with no workarounds.
- **Key issuer.** No model-training run starts without explicit signed authorization in-channel, either a named-run key or a time-boxed standing key with an expiry.

Everything else is agent-run.

## 4. The Learning Loop: Drift Control for Long Tasks

Long tasks drift in three ways. **Expectation drift**: estimates silently detach from reality. **Rule drift**: participants quietly bend procedures mid-task. **Memory drift**: context windows lose earlier decisions. The architecture treats each mechanically.

### 4.1 Monitor loops and learning loops

The design doc (`docs/learning-loops.md`) separates two kinds of loop. Monitor loops (inbox daemons, heartbeats) keep the system responsive but learn nothing. Learning loops make it better, on a cadence, in four steps:

```
OBSERVE   what did I do since last cycle (artifacts, estimates, calls)
DIFF      expectation vs outcome — as NUMBERS, never narrative
BANK      one append-only line per diff to the agent's calibration ledger
ADJUST    at most ONE pin/practice change per cycle, proposed as a dated
          amendment through normal review — never silently self-applied
```

Three rules do most of the work. **One adjustment per cycle** prevents process thrash; everything else queues in the protocol thread. **Diffs must be measured**; "went well" is not a diff. **Bank even when the diff is zero**; a run of zero diffs is calibration evidence, not silence. Learning loops never hold keys. They read artifacts and write ledger lines and proposals; execution stays in the work threads.

### 4.2 Cadence

An early fixed 30-minute tick banked contentless lines during long runs: monitor noise dressed as learning. The corrected cadence is event-driven. A diff banks when an estimate is issued, when it resolves, and when a recompute completes. A two-hour sweep also checks heartbeat age and unconsumed inbox counts and performs one spot-recompute of a previously banked number from raw artifacts. The recompute target comes from a seeded rotation pinned in the calibration ledger's header, because choosing easy targets in the moment is "the quiet failure mode of self-audit."

### 4.3 Standing rules that make drift expensive

- **Pre-registration with falsifiers.** Every action carries failure criteria pinned in the artifact metadata before the run. "Prospective" may only be claimed for predictions stamped pre-run.
- **Checked references.** `refs` must resolve, checked by the sender before sending and by the reviewer as step 0. A result whose refs do not resolve is void on arrival.
- **Provenance.** Relayed decisions carry `via-human`. Relayed restrictions bind immediately; relayed permissions never do. This asymmetry makes authority hard to smuggle.
- **Quarantine on deviation.** Runs launched without a valid key are quarantined: no freeze, no park, results provisional forever.
- **Key-holder progress beats.** A party holding a live authorization posts one line per 30 minutes of key time. After two missed beats the issuer may treat the holder as suspended.
- **Protocol self-evolution.** Rule changes are protocol mail, reviewed and versioned. Rule drift still happens, but in the open, dated and attributed.

## 5. Case Study: Eighteen Days of Live Operation

The system ran from 2026-08-02 to 2026-08-19 coordinating small-model training research in the `model-training` project. On 2026-09-13 it was migrated unchanged into its own repository; the migration itself ran through the protocol and is recorded as a ledger banner.

**Scale.**

| Measure | Value |
|---|---|
| Messages (main channel + secondary arm) | 488 + 274 = 762 |
| Threads | ~30 |
| Seats | 6 (kimi, fable, grok, gemini, muse, human), four model families |
| Messages by sender (main channel) | kimi 216, fable 199, muse 33, grok 5, gemini 1, human 34 |
| Protocol versions shipped | 10, all through in-channel review |
| Human-authored main-channel messages | 34 of 488 (7.0%) |
| Longest thread | method-discovery, 54 sequence numbers |
| Longest unattended window | 10 hours |

**Minimal human involvement.** Only 34 of 488 main-channel messages (7.0%) are human-authored; the wider involvement markers mostly record agents relaying a human ruling rather than the human coordinating. The human's role reduced to issuing time-boxed training keys, ruling on escalated blockers, and ratifying seats and protocol versions. Turn-taking, review, verification, holds, and voids ran entirely between agents.

**Long tasks under light supervision.** The moonlender thread, a failure-detection review cycle spanning 50 sequence numbers (the only longer one, method-discovery at 54, was its successor), closed positive with its deliverable banked and independently verified 14/14. Inside it, a 10-hour autopilot window ran overnight under a standing key: generation, validation, and banking completed with the human reading a summary the next morning. A second arm (fourconnect) reached a pre-registered *falsified* verdict and parked itself cleanly. That is the drift controls working as designed, since the falsifiers that ended it were pinned before the runs. Overnight is where drift usually bites; here pre-registered gates, heartbeat checks, and a morning ledger review replaced a night shift.

**The loop paying rent.** The executor agent's calibration ledger accumulated 37 entries in its first three days of operation. Its first five actual-to-estimated wall-clock ratios were 0.65, 1.00, 0.50, 0.15, and 1.20 (median 0.65), exposing systematic over-estimation of task cost. That is exactly the quiet drift the loop exists to catch, banked as numbers and converted into a dated amendment proposal through the normal thread. The same agent's daemon silence had earlier caused a visible protocol failure; after the loop stood up, heartbeat age became a sweep-checked axis.

**Failure modes observed.** Each became a dated protocol amendment rather than a recurring bug:

- A concurrent ledger rewrite lost 8 thread rows (restored from snapshot; led to single-writer boards).
- A cross-session pause killed the shared watcher mid-thread (led to per-party daemons).
- An agent-authored key "expiry" was ruled invalid by the reviewer (led to keys confirmed by the human only).
- An instance-side protocol edit failed to sync (led to sync checks).

## 6. Discussion and Limitations

**What the architecture buys.** Durability: the record survives session deaths and model swaps. Cheap verifiability: every claim carries resolvable refs, and review starts with a mechanical check. Transport independence: the mail could ride A2A or MCP unchanged. A human-facing surface: the ledger's thread table compresses weeks of work into one screen.

**What it does not solve.** This is a single-machine, trust-by-convention system. There is no access control beyond the append-only norm, no cryptographic signing, and one reviewer per thread, which concentrates verdict power. Latency is human-scale (30-second polls, session-paced replies), so it is unsuitable for interactive tasks. The auto-reply layer handles acks only; real judgment needs full agent sessions, so throughput is bounded by how often each seat opens one. And the drift controls catch process drift, not capability limits. A falsified hypothesis stays falsified no matter how clean the ledger is.

**Next steps.** Multi-machine replication of the ledger, which is already append-only and conflict-tolerant. Cryptographic signing of keys and human rulings. Carrying the protocol over A2A for cross-organization seats. A retrospective on whether the one-adjustment-per-cycle cap should scale with ledger length.

## 7. Conclusion

A shared folder, an append-only ledger, numbered threads with one owner and one reviewer, daemons that watch but never act, and a learning loop that banks measured diffs and changes one thing at a time. None of these pieces is new on its own. Together they let five heterogeneous agents run weeks of long-horizon work, including overnight autonomous windows, while the human's footprint shrank to authorization and escalation. The lesson from eighteen days of operation: for multi-agent systems, the record is the coordination, and drift is best fought with mechanics, not vigilance.

## References

1. Erman, L.D., Hayes-Roth, F., Lesser, V.R., Reddy, D.R. (1980). The Hearsay-II Speech-Understanding System: Integrating Knowledge to Resolve Uncertainty. *ACM Computing Surveys* 12(2).
2. Nii, H.P. (1986). The Blackboard Model of Problem Solving. *AI Magazine* 7(2).
3. Gelernter, D. (1985). Generative Communication in Linda. *ACM Transactions on Programming Languages and Systems* 7(1).
4. Carriero, N., Gelernter, D. (1989). Linda in Context. *Communications of the ACM* 32(4).
5. Grassé, P.-P. (1959). La reconstruction du nid et les coordinations interindividuelles. *Insectes Sociaux* 6.
6. Fowler, M. (2005). Event Sourcing. martinfowler.com/eaaDev/EventSourcing.html.
7. Kreps, J., Narkhede, N., Rao, J. (2011). Kafka: a Distributed Messaging System for Log Processing. *NetDB Workshop*.
8. Wu, Q., Bansal, G., Zhang, J., et al. (2023). AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation. arXiv:2308.08155.
9. Li, G., Hammoud, H., Itani, H., Khizbullin, D., Ghanem, B. (2023). CAMEL: Communicative Agents for "Mind" Exploration of Large Language Model Society. arXiv:2303.17760.
10. Hong, S., Zhuge, M., Chen, J., et al. (2023). MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework. arXiv:2308.00352.
11. Anthropic (2024). Model Context Protocol (MCP). modelcontextprotocol.io.
12. Surapaneni, R., Jha, M., Vakoc, M., Segal, T. (2025). Announcing the Agent2Agent Protocol (A2A). Google Developers Blog, April 2025.
13. Ehtesham, A., Singh, A., Gupta, G.K., Kumar, S. (2025). A Survey of Agent Interoperability Protocols: MCP, ACP, A2A, and ANP. arXiv:2505.02279.
14. Yang, Y., Chai, H., Song, Y., et al. (2025). A Survey of AI Agent Protocols. arXiv:2504.16736.
15. Park, J.S., O'Brien, J., Cai, C., Morris, M., Liang, P., Bernstein, M. (2023). Generative Agents: Interactive Simulacra of Human Behavior. arXiv:2304.03442.
16. Shinn, N., Cassano, F., Berman, E., et al. (2023). Reflexion: Language Agents with Verbal Reinforcement Learning. arXiv:2303.11366.
17. Wang, G., Xie, Y., Jiang, Y., et al. (2023). Voyager: An Open-Ended Embodied Agent with Large Language Models. arXiv:2305.16291.
18. Liu, N.F., Lin, K., Hewitt, J., et al. (2023). Lost in the Middle: How Language Models Use Long Contexts. arXiv:2307.03172.
19. Pan, L., Saxon, M., Xu, W., Nathani, D., Wang, X., Wang, W.Y. (2023). Automatically Correcting Large Language Models: Surveying the Landscape of Diverse Self-Correction Strategies. arXiv:2308.03188.
20. Nosek, B.A., Ebersole, C.R., DeHaven, A.C., Mellor, D.T. (2018). The Preregistration Revolution. *PNAS* 115(11).
21. Sheridan, T.B., Verplank, W.L. (1978). Human and Computer Control of Undersea Teleoperators. MIT Man-Machine Systems Laboratory Report.
