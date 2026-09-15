r"""Append one message-log row to comms/LEDGER.md (v1.11) — the sanctioned way; never edit the log by hand.

The comms-loop log format is:  | id | from | type | re | title | status |
v1.11 puts the project, thread and seq at the front of the title so a ledger grep by project works:
  [tinymodel/scalecircuit s6] <title>

Usage:
  python scripts/ledger_append.py --from-party fable --project tinymodel --thread scalecircuit \
      --seq 6 --type result --re 20260913-031927-fable-tinymodel-scalecircuit-s5-... \
      --id 20260913-040000-fable-tinymodel-scalecircuit-s6-slug --title "one line" [--status OPEN]

Opens the ledger with O_APPEND and writes exactly one line; never read-modify-rewrite.
"""
from __future__ import annotations

import argparse
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "comms" / "LEDGER.md"
PROJECTS = ROOT / "comms" / "PROJECTS.md"
TYPES = {"result", "review", "critique", "action", "question", "protocol", "blocker", "void-notice",
         "limitation", "notice", "review+action"}


def known_projects() -> set[str]:
    text = PROJECTS.read_text(encoding="utf-8")
    return {m.group(1) for m in re.finditer(r"^\| ([a-z][a-z0-9-]*) \| ", text, flags=re.MULTILINE)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--from-party", required=True)
    ap.add_argument("--project", required=True)
    ap.add_argument("--thread", required=True, help="thread slug WITHOUT the project prefix")
    ap.add_argument("--seq", required=True, type=int)
    ap.add_argument("--type", required=True, choices=sorted(TYPES))
    ap.add_argument("--re", default="none", help="id of the mail this answers, or none")
    ap.add_argument("--id", required=True, help="the mail filename without .md")
    ap.add_argument("--title", required=True)
    ap.add_argument("--status", default="OPEN")
    args = ap.parse_args()
    projects = known_projects()
    if args.project not in projects:
        raise SystemExit(f"unknown project {args.project!r}; add a row to comms/PROJECTS.md first (known: {sorted(projects)})")
    for field in (args.title, args.id, args.re, args.status):
        if "|" in field or "\n" in field:
            raise SystemExit("fields may not contain '|' or newlines")
    title = f"[{args.project}/{args.thread} s{args.seq}] {args.title}"
    row = f"| {args.id} | {args.from_party} | {args.type} | {args.re} | {title} | {args.status} |\n"
    fd = os.open(LEDGER, os.O_WRONLY | os.O_APPEND | os.O_CREAT)
    try:
        os.write(fd, row.encode("utf-8"))
    finally:
        os.close(fd)
    print(row.rstrip("\n"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
