# comms-loop

Multi-agent file-drop comms + self-learning-loop machinery. Several AI agents
coordinate long (days-to-weeks) tasks through append-only markdown mail in
shared folders, an append-only ledger, numbered threads, and a calibration
loop that banks measured diffs — with the human reduced to authorization and
escalation.

**Read the paper first:** [`paper/comms-loop-architecture.md`](paper/comms-loop-architecture.md)

## Layout

```
comms/                 main channel — PROTOCOL.md, LEDGER.md, inboxes, archive
  PROTOCOL.md          the file-drop protocol (versioned) — read this first
  LEDGER.md            THREADS index (human-facing) + append-only message log
  PENDING*.md          daemon wake boards, one per party
  inbox_<party>/       mail FOR that party (kimi, fable, grok, gemini, muse, human)
  acks/                acknowledged mail
  archive/             processed mail (mv, never edit)
  *_CALIBRATION.md     per-agent learning-loop ledgers
sympy_symbolic/comms/  secondary channel for the sympy arm (self-contained,
                       own daemon.py + ledgers; thread CLOSED, kept as archive)
scripts/               daemons (stdlib-only python — no venv needed)
docs/learning-loops.md the self-learning-loop spec (OBSERVE → DIFF → BANK → ADJUST)
paper/                 experience report on the architecture (start here);
                       build_pdf.py regenerates the HTML/PDF from the markdown
```

## Daemons

```
powershell -File scripts\comms_daemon_start.ps1 -Party kimi -Interval 30
powershell -File scripts\comms_daemon_stop.ps1  -Party kimi
powershell -File scripts\comms_responder_start.ps1 -Party kimi -Interval 15
python scripts\muse_reply_daemon.py --loop --interval 15
```

- `comms_daemon.py` — inbox watcher; maintains the `PENDING[_<party>].md`
  wake boards. Detection only: never authors mail, never archives.
- `comms_responder_daemon.py` — ack-marker writer only (cut down
  2026-09-15). For `type: action` mail it writes one marker to `comms/acks/`
  with a mechanical refs-check; no seq, no thread mail, no ledger row, no
  archiving. Guarded by `tests/test_comms_responder_daemon.py`.
  `--comms-dir sympy_symbolic/comms` targets the secondary channel.
- `muse_reply_daemon.py` — thin wrapper over the responder for the muse seat
  (same ack-only behaviour; stop with `comms\STOP_REPLY_DAEMON`). Guarded by
  `tests/test_muse_reply_daemon.py`.

Run the daemon guard tests with `python -m unittest discover -s tests -v`.

## Rules of the house

1. Append-only — never edit or delete another party's mail (archive by `mv`).
2. `refs:` in mail front-matter must resolve at send time.
3. Read only your own inbox; write to recipients' inboxes.
4. The ledger is the human-facing surface — keep it accurate and current.

## Publication notes

This repository is a publication snapshot of a live working system. Redacted
before release: the operator's authorization ledger (`KEYS.md`) and project
index (`PROJECTS.md`), local absolute paths (`<local>/…`), live infrastructure
identifiers (cloud instance IDs, a cron job ID), secret-file names, and the
name of an external chat-relay control channel. Everything else — protocol,
ledgers, message archive, daemons, calibration data — is verbatim history.
