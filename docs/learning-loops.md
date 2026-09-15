# Learning Loops — self-improvement cadence for every agent (v0.1 STANDING)

Status: **STANDING** — RATIFIED by the human 2026-08-13T~12:00Z (kimi s19 + muse s20 folded). kimi's ledger + cron build is now authorized per its s19 commitment.
Author: fable, 2026-08-13 (human-directed). Companions:
[discovery-reduction-protocol.md](discovery-reduction-protocol.md),
[arm-process-flow.md](arm-process-flow.md).

## 1. The distinction this doc pins

We run two kinds of loops and have been conflating them:

- **Monitor loops** (exist): watch state, flag changes — fable's 5-min
  comms check, muse's inbox daemon. They keep the system RESPONSIVE.
  They learn nothing.
- **Learning loops** (mostly missing): on a cadence, compare what the
  agent EXPECTED to what actually HAPPENED, bank the delta, and adjust
  exactly one pin. They make the system BETTER. The only live instance
  is fable's every-4-iteration protocol-review round — and its yield
  this week (heartbeats, acks, relay codification, seq rules) came
  from exactly this shape.

## 2. The learning-loop pattern (one shape, per-agent instantiation)

```
OBSERVE   what did I do since last cycle (artifacts, estimates, calls)
DIFF      expectation vs outcome — as NUMBERS (Sankhya rule: no narrative)
BANK      one-line delta to the agent's learnings ledger (append-only)
ADJUST    at most ONE pin/practice change per cycle, proposed as a
          dated amendment through the normal review path — never
          silently self-applied
```

Constraints (anti-patterns from our own history):
- **One adjustment per cycle** — batch adjustments are how process
  thrash starts; the comms-protocol thread queues the rest.
- **DIFF must be measured** — "went well" is not a diff. Estimate vs
  actual, predicted vs banked, claimed vs recomputed.
- **BANK even when the diff is zero** — a run of zero-diffs is
  calibration evidence, not silence.
- **Learning loops never hold keys** — they read artifacts and write
  ledger lines + proposals; execution stays in the arm lanes.

## 3. Per-agent instantiation

### fable (two instances)
1. Protocol-review cadence (every 4 monitor iterations): ran rounds
   1-4, CONCLUDED 2026-08-13 — its yield (v1.10) was ratified and the
   loop retired with its mission; restartable on need. A learning loop
   that has banked its yield SHOULD conclude, not idle (fire #19).
2. Claim-vs-artifact audit loop (human-directed): CADENCE ADJUSTED
   2026-08-13T20:22Z by human GO — 5-min tick retired after 43 fires
   (13 diffs caught, the rest zero-diff/zero-event; the tick's own
   zero-event run was the evidence). Now EVENT-DRIVEN (audit fires in
   the same turn as any published claim) + 2 h drift sweep — the same
   correction kimi s19 made to the original spec, applied to its
   author's loop.
DIFF axes: process-flow step adherence on the active arm; summary
compression vs banked tables (the "~0 on singles" class); estimate
calibration on own dev work.
Ledger: `docs/insight/*-learnings.md` + memory. Already the source of
v1.1.

### muse (exists as daemon — add the DIFF)
muse's loop today is monitor-only (inbox → audit → witness). Add the
learning half, cadence per witness: DIFF = witness verdicts vs later
outcomes — did anything a signed card later get corrected by a
reviewer substitution or a probe? (Current record: 2 signs, both
survived probes — bank that as calibration, not as silence.) Ledger:
one line per witnessed card — **scored as VERDICT CORRECTNESS, never
action count (muse s20, closes the A3-inversion worry):**
`sign/shrink + reason | later outcome (adjudicating probe cited) |
hit/miss`. Sign-that-survives = hit; sign-later-corrected = miss;
unnecessary shrink = miss; shrink-that-survives = hit — over-shrink
costs exactly what under-shrink costs. 2/2 survived-to-date is the
seed entry.

### kimi (MISSING — build this; the spec under review)
kimi is the executor+pricer — the agent whose loop pays fastest.
Correction (kimi s23, was misattributed here): the four hot headline
estimates were FABLE's, not kimi's — they seed fable's calibration
axis, not kimi's; kimi's own banked ratios start at 0.65 (Stage-1
overestimate) and 1.00. kimi's motivating failure mode is the daemon
silence that caused the comms-protocol thread's own exhibit (s5 "the
silence was the exhibit").

**kimi-loop v0.1 spec (cadence CORRECTED by kimi s19: event-driven +
2 h sweep — a fixed 30-min tick banks contentless lines during long
runs, monitor noise dressed as learning content):**
- EVENT-DRIVEN: DIFF+BANK fires on estimate-issued (expectation logged
  at issue time), estimate-resolved (ratio, ×2-adjusted), and
  spot-recompute-completed.
- SWEEP (2 h while seated): heartbeat age, unconsumed-inbox count,
  zero-diff banking. ONE spot-recompute per sweep, target from a
  SEEDED ROTATION pinned in the ledger header — picking easy targets
  in the moment is the quiet failure mode of self-audit.
- Ledger: comms/KIMI_CALIBRATION.md (format owned by kimi s19; header
  carries running estimate-ratio median + rotation queue; seed entries
  = the four hot estimates, the s45 43-min event, the headroom-null
  recompute). Implementation starts ON RATIFICATION, not before.

Original v0 sketch (superseded by the above):

```
OBSERVE  tasks executed since last tick + estimates given + daemon state
DIFF     1. estimate-vs-actual ratio per task (wall clock, ×2-adjusted)
         2. one seeded spot-recompute of a banked number from raw
            artifacts (rotating; the muscle that caught headroom-null)
         3. own-daemon heartbeat age + unconsumed inbox count
BANK     one line per DIFF axis to comms/KIMI_CALIBRATION.md
         (append-only; running estimate-ratio median in the header)
ADJUST   ≤1 proposal per cycle (e.g., "my sim-dev estimates need ×3
         not ×2") via the normal thread, never self-applied
```

Why the spot-recompute leg: kimi's s16 datum — "the substitutions were
cheap BECAUSE the artifacts were banked and recomputable" — makes
recompute practice the cheapest standing verification muscle we have;
one per cycle keeps it warm without a verification arm.

## 4. Closing the loop between loops

Learnings ledgers are INPUTS to the protocol-review rounds: each round
reads the three ledgers first, and any pin change cites the ledger
lines that motivated it. That is the whole self-improvement circuit:
monitor loops keep us live → learning loops bank calibrated deltas →
review rounds turn deltas into dated amendments → arms run under the
amended pins → artifacts feed the next DIFF. No step is new; this doc
only names the circuit and builds kimi's missing quarter of it.

## 5. Review asks (s17)

- kimi: is the 30-min cadence right for your seat pattern; is the
  spot-recompute leg one-per-cycle sustainable; own the ledger format.
- muse: does WITNESS-CALIBRATION create pressure to over-shrink (the
  A3 worry inverted); audit the anti-patterns list.
- human: ratify after fold, as with v1/v1.1.
