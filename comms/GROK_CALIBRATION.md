# GROK CALIBRATION LEDGER

Learning-loops v0.1 (STANDING 2026-08-13, grok-onboard s4 ACK + s5
human seat ratification). Reviewer-shaped instantiation. Append-only
below the header; numbers + paths only (Sankhya pin). Cadence:
event-driven (review-issued / review-adjudicated / attack-call
resolved) + 2 h sweep while seated. Loop never holds keys; ADJUST
proposals go to threads. Estimate axis stays dark until an execution
seat is keyed.

## Header (rewritten on each entry)

- entries = 3
- attack-call hit-rate = n/a (n = 0 — no adjudicated calls this seat)
- estimate-ratio history: [] (axis dark)
- rotation seed = 20260813 (pinned)
- recompute queue (next first): [biz-domains survey mappings | card v3.1 claim lines | dvm-results.md §8 headroom-null]
- daemon: comms-daemon --party grok pid 40388 (30 s)

## Entries

date (UTC) | axis | expected | actual | ratio/delta | refs
2026-08-13 | inbox | fable s1 census 190 backlog | 192 in inbox_grok at s3 (190 + s1 + s2) | +2 | comms/archive/20260813-123830-grok-grok-onboard-s3-*.md; comms/archive/20260813-124300-fable-grok-onboard-s4-*.md
2026-08-13 | inbox | unconsumed grok-onboard tail = 0 after s3 | s4 arrived; consumed same session as s5 | +0 min age | comms/archive/20260813-124300-fable-grok-onboard-s4-loop-ack-roles.md
2026-08-13 | daemon | heartbeat ≤ 60 s | pid 40388 alive at s5 send | nominal | comms/.daemon_grok.pid
