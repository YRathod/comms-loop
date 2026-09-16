#!/usr/bin/env python3
"""muse ack-marker daemon — a thin wrapper around comms_responder_daemon for the muse seat.

Cut down 2026-09-15. Until then this file assigned thread seqs, filed its acks as
`type: review`, dropped them into other parties' inboxes, and echoed 500 chars of
the incoming body. All of that breached protocol §9 rule 4 (auto-acks never take a
thread seq). It now delegates to the one sanctioned ack implementation:

  - acks `type: action` mail only, as a marker in comms/acks/ (§9 rule 5);
  - no seq, no thread mail, no ledger row, no archiving, no body echo.

Kept for compatibility: the CLI (--loop / --interval / --once) and the stop file
comms/STOP_REPLY_DAEMON. State now lives in comms/.responder_state_muse.json.

Usage:
  python scripts/muse_reply_daemon.py --once
  python scripts/muse_reply_daemon.py --loop --interval 15
Stop: create comms/STOP_REPLY_DAEMON (or comms/STOP_DAEMON, or STOP at repo root)
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import comms_responder_daemon as responder  # noqa: E402

ROOT = responder.ROOT
COMMS = responder.DEFAULT_COMMS
PARTY = "muse"
STOP_FILES = (COMMS / "STOP_REPLY_DAEMON", COMMS / "STOP_DAEMON", responder.STOP_ROOT)


def tick(comms_dir: Path = COMMS) -> int:
    """One pass: write ack markers for un-acked action mail addressed to muse."""
    return responder.process_inbox(PARTY, comms_dir)


def main() -> int:
    ap = argparse.ArgumentParser(description="muse ack-marker daemon (wrapper)")
    ap.add_argument("--loop", action="store_true")
    ap.add_argument("--interval", type=int, default=15)
    ap.add_argument("--once", action="store_true")
    args = ap.parse_args()
    if not args.loop and not args.once:
        args.once = True

    sys.stdout.reconfigure(line_buffering=True)
    if args.once:
        n = tick()
        print(f"[muse-reply-daemon] wrote {n} ack marker(s).")
        return 0

    print(f"[muse-reply-daemon] start interval={args.interval}s")
    while True:
        if any(p.exists() for p in STOP_FILES):
            print("[muse-reply-daemon] STOP found — exit")
            return 0
        try:
            n = tick()
            if n:
                print(f"[muse-reply-daemon] wrote {n} ack marker(s).")
        except Exception as e:  # noqa: BLE001
            print(f"[muse-reply-daemon] error {e}", file=sys.stderr)
        time.sleep(max(5, args.interval))


if __name__ == "__main__":
    sys.exit(main())
