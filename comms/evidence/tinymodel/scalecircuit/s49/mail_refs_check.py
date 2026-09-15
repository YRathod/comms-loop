"""Refuse to send a mail whose refs do not all resolve to non-empty files (fable-side pre-send gate,
after the third typed-before-frozen instance on 2026-09-14: a mail asserted a safety case whose file
did not exist because the assembler had crashed in the same command).

    python scripts/mail_refs_check.py <mail.md>      -> exit 0 if every ref exists and is non-empty, 1 otherwise
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    path = sys.argv[1]
    text = open(path, encoding="utf-8").read()
    m = re.search(r"^refs:\s*(.*?)^---", text, re.S | re.M)
    refs = []
    if m:
        block = m.group(1)
        refs = re.findall(r"comms/[A-Za-z0-9_./\-]+", block)
    else:
        head = text.split("---")[1] if text.startswith("---") else ""
        refs = re.findall(r"comms/[A-Za-z0-9_./\-]+", head)
    bad = [r for r in refs if not (os.path.exists(os.path.join(ROOT, r)) and os.path.getsize(os.path.join(ROOT, r)) > 0)]
    print(f"refs: {len(refs)}; missing or empty: {len(bad)} {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
