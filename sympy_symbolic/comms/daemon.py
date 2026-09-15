"""SymPy Symbolic Flow committee daemon — inbox watcher (scoped subproject).

Polls sympy_symbolic/comms/inbox_{kimi,fable,grok,gemini}, maintains a wake board,
and logs new mail. Operates in a separate directory from the main project comms daemon.

Usage:
  python sympy_symbolic/comms/daemon.py --loop --interval 30

Stop: create sympy_symbolic/comms/STOP_DAEMON, or Ctrl+C / kill PID.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # project root
COMMS = Path(__file__).resolve().parent       # sympy_symbolic/comms
PARTIES = ("kimi", "fable", "grok", "gemini", "deepseek", "muse")
STATE = COMMS / ".daemon_state.json"
PENDING = COMMS / "PENDING.md"
LOG = COMMS / "daemon.log.jsonl"
STOP_DAEMON = COMMS / "STOP_DAEMON"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_state() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {"seen": {}, "started": utc_now(), "ticks": 0}


def save_state(st: dict) -> None:
    STATE.write_text(json.dumps(st, indent=1) + "\n", encoding="utf-8")


def log_event(ev: dict) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(ev, ensure_ascii=False) + "\n")


def list_mail(party: str) -> list[Path]:
    d = COMMS / f"inbox_{party}"
    if not d.is_dir():
        return []
    return sorted(
        p for p in d.iterdir()
        if p.is_file() and p.suffix == ".md" and p.name != ".gitkeep"
    )


def scan(st: dict) -> tuple[list[dict], dict[str, list[dict]]]:
    new: list[dict] = []
    pending: dict[str, list[dict]] = {p: [] for p in PARTIES}
    seen: dict = st.setdefault("seen", {})

    for party in PARTIES:
        for path in list_mail(party):
            key = str(path.relative_to(COMMS)).replace("\\", "/")
            try:
                mtime = path.stat().st_mtime
                size = path.stat().st_size
            except OSError:
                continue
            rec = {"party": party, "path": key, "mtime": mtime, "size": size,
                   "name": path.name}
            pending[party].append(rec)
            prev = seen.get(key)
            if prev is None or prev.get("mtime") != mtime or prev.get("size") != size:
                kind = "new" if prev is None else "changed"
                ev = {"ts": utc_now(), "event": kind, **rec}
                new.append(ev)
                seen[key] = {"mtime": mtime, "size": size,
                             "first_seen": prev.get("first_seen", utc_now()) if prev else utc_now()}

    live = {r["path"] for rows in pending.values() for r in rows}
    for k in list(seen.keys()):
        if k not in live:
            del seen[k]
    return new, pending


def write_pending(pending: dict[str, list[dict]], st: dict) -> None:
    lines = [
        "# sympy_symbolic comms PENDING - committee wake board",
        "",
        f"Updated: {utc_now()} | ticks={st.get('ticks', 0)} | "
        f"daemon since {st.get('started', '?')}",
        "",
        "Committee: Kimi (chair), Fable (science review), Grok (attack/tooling), Gemini (third eye).",
        "",
    ]
    total = 0
    for party in PARTIES:
        rows = pending[party]
        total += len(rows)
        lines.append(f"## inbox_{party} — {len(rows)} waiting")
        if not rows:
            lines.append("_empty_")
        else:
            for r in rows:
                lines.append(f"- `{r['name']}`")
        lines.append("")
    lines.append(f"**Total waiting: {total}**")
    lines.append("")
    PENDING.write_text("\n".join(lines), encoding="utf-8")


def tick() -> list[dict]:
    st = load_state()
    st["ticks"] = int(st.get("ticks", 0)) + 1
    st["last_tick"] = utc_now()
    new, pending = scan(st)
    write_pending(pending, st)
    for ev in new:
        log_event(ev)
        print(f"[sympy-comms-daemon] {ev['event']} {ev['party']}: {ev['name']}", flush=True)
    save_state(st)
    return new


def should_stop() -> bool:
    return STOP_DAEMON.exists()


def main() -> int:
    ap = argparse.ArgumentParser(description="sympy_symbolic comms/ inbox watcher")
    ap.add_argument("--once", action="store_true", help="single scan then exit")
    ap.add_argument("--loop", action="store_true", help="poll forever")
    ap.add_argument("--interval", type=int, default=30, help="seconds between scans")
    args = ap.parse_args()
    if not args.once and not args.loop:
        args.once = True

    for party in PARTIES:
        (COMMS / f"inbox_{party}").mkdir(parents=True, exist_ok=True)
        gitkeep = COMMS / f"inbox_{party}" / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.write_text("", encoding="utf-8")

    print(f"[sympy-comms-daemon] comms={COMMS} interval={args.interval}s", flush=True)
    log_event({"ts": utc_now(), "event": "start",
               "mode": "once" if args.once else "loop", "interval": args.interval})

    if args.once:
        tick()
        return 0

    while True:
        if should_stop():
            print("[sympy-comms-daemon] STOP_DAEMON present — exiting", flush=True)
            log_event({"ts": utc_now(), "event": "stop"})
            return 0
        tick()
        time.sleep(max(5, args.interval))


if __name__ == "__main__":
    sys.exit(main())
