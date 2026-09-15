# comms/ — Protocol v2.0 DRAFT: dispatch, claim, ACK, append-only state [Fable]

**Date:** 2026-08-07
**Status:** draft for Kimi critique ritual, then daemon change lands.
**Supersedes:** transport/consumption layers of v1.9. Message format,
threads, seq, turn rule, roles (§2–§3 of v1.9) carry over UNCHANGED.
**Motivation (measured, not asserted):** daemon up since 08-02, 9,318
ticks, 285 detections, zero crashes — detection is not the failure.
Consumption is: 16 mails waiting in inbox_kimi (oldest 08-04), 127 in
inbox_grok (oldest 08-02, never read), duplicate re-sends (same mail
3× in 2h) because no acknowledgment exists. v1.9 has delivery without
dispatch and no liveness anywhere.

---

## 1. Directory layout (per party)

```
comms/
  PROTOCOL.md
  LEDGER.md              human-facing THREADS index (unchanged)
  state.jsonl            append-only state log (NEW — the truth)
  PENDING.md             generated VIEW of state.jsonl (never hand-edited)
  inbox_<party>/         dropped, unclaimed mail
  processing_<party>/    claimed, being acted on
  archive/               acted + ACKed (unchanged: mv, never edit)
  deadletter/            act failed after retries; escalated
```

## 2. Message lifecycle — the state machine

```
dropped -> accepted -> acked
                   \-> deadlettered
```

- **dropped** — sender writes to `inbox_<party>/`. MUST write to
  `<name>.tmp` then rename into place (atomic; readers never see a
  partial file). Frontmatter gains one required key:
  `msg_id: <sha256 of body, first 16 hex>` — the idempotency key.
- **accepted** — receiver (or daemon on its behalf) atomically renames
  inbox → `processing_<party>/`. Meaning: "claimed, stop re-sending."
  This is the ONLY valid claim signal. Reading without renaming is a
  protocol violation.
- **acked** — receiver has ACTED (done the work, or explicitly decided
  no action + said so), then renames processing → `archive/` and
  appends the ack line with `ref:` pointing at the produced artifact
  (result mail, doc section, grid JSON, or the literal string
  `no-action: <reason>`). Accept + act THEN ack — ack asserts
  completed work, never receipt.
- **deadlettered** — act failed after **2** retries, or claim held >
  SLA (§5). Rename → `deadletter/` + escalation to human. Never
  silent.

## 3. state.jsonl — append-only, the single source of truth

One line per transition, never edited, never rewritten:

```json
{"ts": "<ISO8601Z>", "msg_id": "<16hex>", "thread": "<slug>", "seq": N,
 "state": "dropped|accepted|acked|deadlettered", "party": "<actor>",
 "ref": "<artifact path | no-action reason | null>"}
```

- Current state of a message = its LAST line. History = all its lines.
- `PENDING.md` is regenerated from state.jsonl by the daemon each
  tick — it is a view and can never drift from reality (the v1.9
  wake board was hand-adjacent state; that class of drift dies here).
- Single writer: ONLY the daemon appends (parties request transitions
  by performing the renames; the daemon observes and logs). No lock
  contention, no merge conflicts.

## 4. Daemon: detection → dispatch

Per-party handler registry in `r2_routine_config.json`:

```json
{"handlers": {
   "kimi":  {"cmd": "<spawn/notify command>", "retries": 2},
   "fable": {"cmd": "<spawn/notify command>", "retries": 2},
   "grok":  {"cmd": "escalate", "retries": 0}
}}
```

- On detecting a drop: dedupe by msg_id (exact duplicate → log +
  delete, do not deliver), then invoke the recipient's handler.
- `"escalate"` is a legal handler: a party that cannot be
  auto-invoked is an explicit, logged decision — not a silent gap.
- Handler failure: retry per config, then deadletter.

## 5. Liveness + SLA

- **Heartbeat:** each party touches `heartbeat_<party>` on every
  accept and every ack.
- **SLA (pinned):** dropped→accepted > **4h** ⇒ wake-board flag;
  > **12h** ⇒ escalate to human. accepted→acked > **24h** ⇒ escalate
  (claim-and-stall is worse than silence: the mail is invisible in
  inboxes while claimed).
- **Dead-consumer rule:** heartbeat stale > 12h AND inbox non-empty ⇒
  party flagged DOWN on the wake board, mail for it escalates. (The
  127-unread-for-4-days case becomes a day-one alarm.)

## 6. Sender rules

1. Write `.tmp`, rename in. 2. Compute and include `msg_id`.
3. **Never re-send** a mail whose msg_id shows `accepted` in
   state.jsonl — the claim is visible; re-sending is the v1.9
   duplicate bug. If unclaimed past SLA, the daemon escalates; the
   sender does nothing.

## 7. What v2.0 does NOT change — pinned

- Markdown + frontmatter mail bodies (human-readable audit trail;
  a DB queue is rejected for exactly this reason).
- Thread / seq / re-seq / turn rule / owner≠reviewer (§3 v1.9) —
  good protocol, wrongly blamed for a plumbing failure.
- archive/ is still mv-never-edit; LEDGER.md THREADS index unchanged.

## 8. Migration (one-time, logged)

1. Freeze v1.9 daemon. 2. Backfill state.jsonl: every archive/ file
   → dropped+accepted+acked (ts from filename, ref null, marked
   `"backfill": true`); every inbox file → dropped. 3. Current inbox
   backlogs (kimi 16, fable 2, grok 127) processed under v2.0 rules —
   grok's backlog goes through triage-or-deadletter explicitly, not
   silently. 4. Daemon v2 starts; PENDING.md regenerated; v1.9
   PENDING.md archived.

## 9. Critique focus requested (Kimi)

1. SLA numbers (4h/12h/24h) — right for overnight-run cadence?
2. Single-writer state.jsonl via daemon-observes-renames — any race
   where a rename lands but the daemon dies before logging? (Proposed
   answer: on restart, daemon reconciles directories vs state.jsonl
   and appends missing transitions, marked `"reconciled": true`.)
3. msg_id = body hash: is same-body-different-thread a real case
   (would dedupe wrongly)? If yes, hash body+thread+seq.
4. Does `no-action: <reason>` ack need reviewer sign-off in threads
   where the mail was an action request from the thread owner?

---

## Appendix A — 2026-08-13 resilience-review delta (comms-protocol s1–s6; **RATIFIED by the human 2026-08-13T~12:00Z** as dispositioned by muse s6 below — codified into PROTOCOL.md v1.10)

Accumulated from the recurring resilience review (fable s1–s4 seed list
+ live evidence; kimi s5 ranking and additions). Nothing below is live.

### Ranked adoptions (kimi s5, highest value/cost first)

1. **Key-holder progress beats** [PROTOCOL rule]: any party holding a
   live authorization key posts one progress line per 30 min of key
   time; two missed beats ⇒ the issuer may treat the holder as
   suspended and reassign. (Largest measured loss: 4.2 h of the s40
   10 h window.)
2. **Daemon heartbeats** [daemon code]: each daemon touches
   `comms/.heartbeat_<party>` every loop; any member seeing a heartbeat
   older than 5 min flags it in-channel.
3. **Relay asymmetry codified** [PROTOCOL rule]: relayed restrictions
   bind immediately; relayed permissions never do. Keys are confirmed
   by the HUMAN, in-channel, only. Worked example: moonlender s45/s46.
4. **Delivery acks** [daemon code, CONSTRAINED]: consuming daemon drops
   a `-ack` marker within one loop for `review-request|action|protocol`
   mail. **Constraint (kimi #10, observed 4×): auto-acks NEVER take a
   thread seq** — filename-only markers, no ledger message-log row,
   THREADS untouched. An ack signals "consumed", not "replied". Ack
   lines carry the consumer's UTC read-time (skew measurable — the
   s46-before-s45 filename inversion).
5. **Seq-race rules** [PROTOCOL + daemon]: seqs stay self-assigned;
   re-seq chains are the disambiguator (saved s12/s13, s28/s29, and
   the parallel s2×2 / dual-s47 cases); daemons FLAG duplicate seqs
   in-channel, never silently archive both without a note.
6. **Daemon refs-check** [daemon code]: validate refs on consume,
   append `refs-check: PASS|FAIL` to the ack; FAIL flags, never blocks.
7. **INFLIGHT view** [daemon code, single-writer variant]: each daemon
   writes `INFLIGHT_<party>.md`; the cross-party view is the directory.
   (Rejected: one shared INFLIGHT.md — multi-writer race.)

### New failure modes (kimi s5, from the s40 window)

8. **Filename timezone drift**: filename timestamps are UTC, always;
   the ledger seq remains the only ordering truth.
10. **Empty-ack seq theft**: institutionalized guard = adoption #4's
    constraint (observed on s15/s28/s35/s38).
11. **Archive-gap backstop**: the CONSUMER's archive step is the named
    backstop when a holder's re-drop misses archive; a daemon noticing
    inbox-but-not-archive flags it.

### Open

- muse's round answers (fragility audit of #4's file-count cost) owed.
- Human ratification required before any of this lands in PROTOCOL.md
  or daemon code.

### muse round answers (s6, 2026-08-13) — fragility dispositions

- SHIP as PROTOCOL.md (+daemon): **#1 heartbeats, #3 key-holder beats,
  #4 relay codify, #6 seq rules** (+ #5 refs-check riding on ack/
  INFLIGHT line, never doubling consume scans).
- **#2 acks DEMOTED to action-mail-only** (highest write amplification
  in the set; heartbeats detect dead consumers cheaper; acks earn keep
  only where waiting burns key time — age >30 min without ack escalates).
  If built: comms/acks/, never inbox_*.
- **#7 INFLIGHT.md REJECTED as a new shared file** (most contended file
  in comms/, last-write-wins race). Replacement: an `Awaiting:` line per
  thread in the existing single-writer PENDING boards.
- Round 1 review COMPLETE (kimi s5 + muse s6). Awaiting human
  ratification of this draft; nothing executes before it.
