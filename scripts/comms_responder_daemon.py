#!/usr/bin/env python3
"""comms/ ack-marker daemon for the file-drop protocol (v1.9+).

This daemon is a detector, not an agent. Its whole job:

  1. watch inbox_<party>/ for `type: action` mail addressed to <party>;
  2. for each such mail, write ONE ack marker to comms/acks/ (protocol §9 rule 5)
     carrying a mechanical refs-check (every listed ref exists and is non-empty);
  3. nothing else.

What it deliberately does NOT do (protocol §9 rule 4, "auto-acks never take a
thread seq"; PROTOCOL v1.13+ "the watcher never authors mail"):

  - it never writes thread mail, never assigns a seq, never appends a ledger row;
  - it never archives another party's mail (reading and archiving is the
    session's job — archiving unanswered mail would hide it from the session);
  - it never emits a body with a claim in it. The ack text is a fixed string.

History: until 2026-09-15 this file carried hard-coded, thread-specific reply
bodies that were sent as `type: result` / `review` mail under a party's name
(four instances in sympy-symbolic, Aug 2026). That code is gone; the test in
tests/test_comms_responder_daemon.py fails if anything like it comes back.

Usage:
  python scripts/comms_responder_daemon.py --party kimi --once
  python scripts/comms_responder_daemon.py --party kimi --loop --interval 15
  python scripts/comms_responder_daemon.py --party fable --comms-dir sympy_symbolic/comms --loop
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_COMMS = ROOT / "comms"
STOP_ROOT = ROOT / "STOP"
DAEMON_NAME = "comms_responder_daemon"

# The only mail type that gets an ack marker (protocol §9 rule 5).
ACKABLE_TYPES = {"action"}

# The one and only body this daemon may write. No f-strings with content, ever.
ACK_BODY = (
    "Mechanical ack marker written by the responder daemon. "
    "No judgment, no claim, no thread seq. "
    "A full agent session for this party still owes the reply."
)


def utc_now_str() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")


def utc_iso_str() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ── front-matter parsing (unchanged from the previous version) ──────────────

def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML-ish front-matter and body. Falls back to plain-markdown scan."""
    if not content.startswith("---"):
        meta = _parse_plain_markdown_meta(content)
        return meta, content.strip()

    parts = content.split("---", 2)
    if len(parts) < 3:
        meta = _parse_plain_markdown_meta(content)
        return meta, content.strip()

    header_text = parts[1]
    body = parts[2].strip()
    meta: dict = {}
    for line in header_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, val = line.split(":", 1)
        key, val = key.strip(), val.strip()
        if val.startswith("[") and val.endswith("]"):
            meta[key] = [x.strip() for x in val[1:-1].split(",") if x.strip()]
        else:
            meta[key] = val

    if "from" not in meta:
        meta.update(_parse_plain_markdown_meta(header_text + "\n" + body))
    return meta, body


def _normalize_party(name: str) -> str:
    name = re.sub(r"\s*\([^)]*\)", "", name.strip())
    return name.lower()


def _parse_plain_markdown_meta(text: str) -> dict:
    meta: dict = {}
    lines = text.splitlines()
    for line in lines:
        m = re.match(r"^(?:\*{0,2})?From:?\*?\*?\s*([^·*\n]+)", line, re.IGNORECASE)
        if m:
            meta["from"] = _normalize_party(m.group(1).strip().rstrip("*"))
            break
    for line in lines:
        m = re.match(r"^(?:\*{0,2})?To:?\*?\*?\s*([^·*\n]+)", line, re.IGNORECASE)
        if m:
            raw = m.group(1).strip().rstrip("*")
            rec = [_normalize_party(r) for r in re.split(r"[,;]", raw) if r.strip()]
            meta["to"] = rec if len(rec) > 1 else (rec[0] if rec else "")
            break
    for line in lines:
        m = re.match(r"^#+\s*(.*)", line)
        if m:
            heading = m.group(1).strip()
            tm = re.match(r"(?:.*?—\s*)?(?:COMMITTEE TASK:\s*)?([\w\-]+(?:\s+[\w\-]+)*)", heading)
            meta["thread"] = tm.group(1).strip() if tm else heading[:60]
            break
    if "thread" in meta and "seq" not in meta:
        meta["seq"] = "1"
    return meta


def read_inbox(party: str, comms_dir: Path) -> list[Path]:
    inbox = comms_dir / f"inbox_{party}"
    if not inbox.exists():
        return []
    return sorted(
        (p for p in inbox.iterdir() if p.is_file() and p.suffix == ".md" and p.name != ".gitkeep"),
        key=lambda p: p.name,
    )


# ── the ack marker ──────────────────────────────────────────────────────────

def refs_check(refs: list[str] | str | None, root: Path = ROOT) -> tuple[str, list[str]]:
    """Mechanical refs check: every ref exists and is non-empty. Returns (verdict, missing)."""
    if not refs:
        return "PASS", []
    if isinstance(refs, str):
        refs = [refs]
    missing = []
    for r in refs:
        p = Path(r)
        if not p.is_absolute():
            p = root / r
        if not p.exists() or (p.is_file() and p.stat().st_size == 0):
            missing.append(r)
    return ("FAIL" if missing else "PASS"), missing


def make_ack(incoming_meta: dict, incoming_filename: str, my_party: str,
             root: Path = ROOT) -> tuple[str, str]:
    """Build the ack marker (filename, content) for one action mail.

    The marker has no `seq`, no claim, and names the daemon as its author.
    """
    sender = incoming_meta.get("from", "unknown")
    thread = str(incoming_meta.get("thread", "general"))
    incoming_id = incoming_filename[:-3] if incoming_filename.endswith(".md") else incoming_filename
    verdict, missing = refs_check(incoming_meta.get("refs"), root)
    safe_thread = re.sub(r"[\\/ ]", "-", thread)
    # Two different mails can share thread and seq (a duplicate seq is exactly what the
    # protocol asks daemons to flag), so the incoming file's own timestamp goes in the name.
    incoming_ts = re.match(r"(\d{8}-\d{4,6})", incoming_id)
    tag = f"-re-{incoming_ts.group(1)}" if incoming_ts else ""
    filename = f"{utc_now_str()}-{my_party}-ack-{safe_thread}-s{incoming_meta.get('seq', '?')}{tag}.md"

    header = [
        "---",
        f"from: {my_party}",
        f"to: [{sender}]",
        f"thread: {thread}",
        f"re: {incoming_id}",
        "type: ack",
        "automated: true",
        f"authored-by: {DAEMON_NAME}",
        f"refs-check: {verdict}",
        "---",
        "",
    ]
    body = [f"# ack marker (no thread seq) — {thread} s{incoming_meta.get('seq', '?')}", "", ACK_BODY, ""]
    if missing:
        body += ["refs-check FAIL — missing or empty:"] + [f"- {m}" for m in missing] + [""]
    return filename, "\n".join(header + body)


# ── state: never ack the same mail twice ────────────────────────────────────

def _state_path(comms_dir: Path, party: str) -> Path:
    return comms_dir / f".responder_state_{party}.json"


def load_state(comms_dir: Path, party: str) -> set[str]:
    p = _state_path(comms_dir, party)
    if not p.exists():
        return set()
    try:
        return set(json.loads(p.read_text(encoding="utf-8")).get("acked", []))
    except (ValueError, OSError):
        return set()


def save_state(comms_dir: Path, party: str, acked: set[str]) -> None:
    _state_path(comms_dir, party).write_text(
        json.dumps({"acked": sorted(acked), "updated": utc_iso_str()}, indent=1), encoding="utf-8"
    )


def already_acked(acks_dir: Path, incoming_id: str) -> bool:
    if not acks_dir.exists():
        return False
    needle = f"re: {incoming_id}"
    for p in acks_dir.glob("*.md"):
        try:
            if needle in p.read_text(encoding="utf-8"):
                return True
        except OSError:
            continue
    return False


# ── main pass ───────────────────────────────────────────────────────────────

def process_inbox(my_party: str, comms_dir: Path, root: Path = ROOT) -> int:
    """Write ack markers for un-acked action mail in inbox_<party>. Touches nothing else."""
    mail_files = read_inbox(my_party, comms_dir)
    if not mail_files:
        return 0

    acks_dir = comms_dir / "acks"
    acked = load_state(comms_dir, my_party)
    written = 0

    for mail_path in mail_files:
        try:
            meta, _body = parse_frontmatter(mail_path.read_text(encoding="utf-8"))
            sender = meta.get("from")
            if not sender or sender == my_party:
                continue
            if str(meta.get("type", "")).strip().lower() not in ACKABLE_TYPES:
                continue
            incoming_id = mail_path.stem
            if incoming_id in acked or already_acked(acks_dir, incoming_id):
                acked.add(incoming_id)
                continue

            filename, content = make_ack(meta, mail_path.name, my_party, root)
            acks_dir.mkdir(parents=True, exist_ok=True)
            (acks_dir / filename).write_text(content, encoding="utf-8")
            acked.add(incoming_id)
            written += 1
            print(f"[{utc_iso_str()}] ack marker for {mail_path.name} -> acks/{filename}")
        except Exception as e:  # noqa: BLE001 — a bad file must not stop the loop
            print(f"Error processing {mail_path.name}: {e}", file=sys.stderr)

    save_state(comms_dir, my_party, acked)
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description="comms ack-marker daemon (detector only)")
    parser.add_argument("--party", default="kimi")
    parser.add_argument("--comms-dir", default=None, help="comms directory (default: comms/)")
    parser.add_argument("--loop", action="store_true", help="run continuously")
    parser.add_argument("--interval", type=int, default=15, help="poll interval, seconds")
    parser.add_argument("--once", action="store_true", help="single pass and exit")
    args = parser.parse_args()

    sys.stdout.reconfigure(line_buffering=True)
    if not args.loop and not args.once:
        args.once = True

    comms_dir = Path(args.comms_dir) if args.comms_dir else DEFAULT_COMMS
    if not comms_dir.is_absolute():
        comms_dir = ROOT / comms_dir
    stop_daemon = comms_dir / "STOP_DAEMON"

    print(f"[{DAEMON_NAME}] party={args.party} comms={comms_dir} mode={'loop' if args.loop else 'once'} interval={args.interval}s")

    if args.once:
        n = process_inbox(args.party, comms_dir)
        print(f"[{DAEMON_NAME}] wrote {n} ack marker(s).")
        return 0

    tick = 0
    while True:
        tick += 1
        try:
            if STOP_ROOT.exists() or stop_daemon.exists():
                print(f"[{DAEMON_NAME}] STOP file detected — exiting.")
                return 0
            n = process_inbox(args.party, comms_dir)
            if n:
                print(f"[{DAEMON_NAME}] tick {tick}: wrote {n} ack marker(s).")
            elif tick == 1 or tick % 20 == 0:
                print(f"[{DAEMON_NAME}] tick {tick}: idle")
        except Exception as e:  # noqa: BLE001
            print(f"[{DAEMON_NAME}] tick {tick} ERROR: {e}", file=sys.stderr)
        time.sleep(max(3, args.interval))


if __name__ == "__main__":
    sys.exit(main())
