r"""comms/ background daemon — inbox watcher (not an agent).

Polls inbox_kimi / inbox_fable / inbox_grok, maintains a wake board, and
logs new mail. Agents still run PROTOCOL §8 when woken; this process only
detects arrivals so the human (or a Cursor Automation) knows who owes a
session.

Usage:
  .\.venv\Scripts\python.exe scripts\comms_daemon.py --once
  .\.venv\Scripts\python.exe scripts\comms_daemon.py --loop --interval 30
  .\.venv\Scripts\python.exe scripts\comms_daemon.py --loop --interval 30 --hook "..."
  .\.venv\Scripts\python.exe scripts\comms_daemon.py --loop --interval 30 --party kimi

Per-party mode (--party kimi|fable|grok|muse): watches ONLY that inbox and
keeps its own state (.daemon_state_<party>.json), wake board
(PENDING_<party>.md), and stop file (comms/STOP_DAEMON_<PARTY>), so each
session runs and pauses its own watcher without touching the others.
Multiple per-party daemons coexist; the shared log daemon.log.jsonl tags
each event with its scope.

Stop: create STOP at repo root or comms/STOP_DAEMON (stops ALL daemons),
or comms/STOP_DAEMON_<PARTY> (stops only that party's), or Ctrl+C / kill PID.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMS = ROOT / "comms"
PARTIES = ("kimi", "fable", "grok", "muse", "gemini")
LOG = COMMS / "daemon.log.jsonl"
STOP_ROOT = ROOT / "STOP"
STOP_ALL = COMMS / "STOP_DAEMON"

# Scope: None = all parties (shared daemon); a party name = per-party daemon.
SCOPE: str | None = None


def state_path() -> Path:
    return COMMS / (f".daemon_state_{SCOPE}.json" if SCOPE else ".daemon_state.json")


def pending_path() -> Path:
    return COMMS / (f"PENDING_{SCOPE}.md" if SCOPE else "PENDING.md")


def stop_path() -> Path | None:
    return COMMS / f"STOP_DAEMON_{SCOPE.upper()}" if SCOPE else None


def watched_parties() -> tuple[str, ...]:
    if SCOPE:
        return (SCOPE,)
    found = tuple(
        p.name[6:] for p in sorted(COMMS.glob("inbox_*")) if p.is_dir() and p.name.startswith("inbox_")
    )
    return found if found else PARTIES



def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_state() -> dict:
    p = state_path()
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {"seen": {}, "started": utc_now(), "ticks": 0}


def save_state(st: dict) -> None:
    state_path().write_text(json.dumps(st, indent=1) + "\n", encoding="utf-8")


def log_event(ev: dict) -> None:
    # Resilient: primary log may transiently be EROFS (bwrap + drvfs 9p lock) — fall back, never crash caller.
    for p in (LOG, Path("/tmp/comms-daemon.log.jsonl"), Path(f"/tmp/comms-{SCOPE or 'all'}.log.jsonl")):
        try:
            p.parent.mkdir(parents=True, exist_ok=True)
            with p.open("a", encoding="utf-8") as f:
                f.write(json.dumps(ev, ensure_ascii=False) + "\n")
            return
        except OSError:
            continue
    try:
        print(f"[comms-daemon] log_failed {ev}", file=sys.stderr, flush=True)
    except Exception:
        pass


def list_mail(party: str) -> list[Path]:
    d = COMMS / f"inbox_{party}"
    if not d.is_dir():
        return []
    return sorted(
        p for p in d.iterdir()
        if p.is_file() and p.suffix == ".md" and p.name != ".gitkeep"
    )


def scan(st: dict) -> tuple[list[dict], dict[str, list[dict]]]:
    """Return (new_events, pending_by_party)."""
    new: list[dict] = []
    parties = watched_parties()
    pending: dict[str, list[dict]] = {p: [] for p in parties}
    seen: dict = st.setdefault("seen", {})

    for party in parties:
        for path in list_mail(party):
            key = str(path.relative_to(ROOT)).replace("\\", "/")
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
                ev = {"ts": utc_now(), "event": kind, "scope": SCOPE or "all", **rec}
                new.append(ev)
                seen[key] = {"mtime": mtime, "size": size, "first_seen":
                             prev.get("first_seen", utc_now()) if prev else utc_now()}
    # drop seen entries for files that left the inbox (archived)
    live = {r["path"] for rows in pending.values() for r in rows}
    for k in list(seen.keys()):
        if k not in live:
            del seen[k]
    return new, pending


def write_pending(pending: dict[str, list[dict]], st: dict) -> None:
    scope = SCOPE or "all"
    lines = [
        f"# comms PENDING ({scope}) - daemon wake board",
        "",
        f"Updated: {utc_now()} | ticks={st.get('ticks', 0)} | "
        f"daemon since {st.get('started', '?')} | scope={scope}",
        "",
        "Agents: read your inbox (PROTOCOL section 8). Detection only.",
        "",
    ]
    total = 0
    for party in watched_parties():
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
    pending_path().write_text("\n".join(lines), encoding="utf-8")


def run_hook(hook: str, events: list[dict]) -> None:
    if not hook or not events:
        return
    env_payload = json.dumps(events)
    # Windows-friendly: pass JSON on stdin
    try:
        subprocess.run(
            hook, shell=True, input=env_payload.encode("utf-8"),
            cwd=str(ROOT), timeout=120, check=False,
        )
    except Exception as e:
        try:
            log_event({"ts": utc_now(), "event": "hook_error",
                       "scope": SCOPE or "all", "error": str(e)})
        except Exception:
            pass


def touch_heartbeat() -> None:
    party = SCOPE or "all"
    hb = COMMS / f".heartbeat_{party}"
    try:
        hb.touch(exist_ok=True)
    except Exception:
        pass


def tick(hook: str | None) -> list[dict]:
    touch_heartbeat()
    st = load_state()
    st["ticks"] = int(st.get("ticks", 0)) + 1
    st["last_tick"] = utc_now()
    new, pending = scan(st)
    write_pending(pending, st)
    for ev in new:
        try:
            log_event(ev)
        except Exception:
            pass
        print(f"[comms-daemon] {ev['event']} {ev['party']}: {ev['name']}", flush=True)
    if new and hook:
        run_hook(hook, new)
    save_state(st)
    return new



def should_stop() -> bool:
    if STOP_ROOT.exists() or STOP_ALL.exists():
        return True
    p = stop_path()
    return p.exists() if p else False


def main() -> int:
    global SCOPE
    ap = argparse.ArgumentParser(description="comms/ inbox watcher daemon")
    ap.add_argument("--once", action="store_true", help="single scan then exit")
    ap.add_argument("--loop", action="store_true", help="poll forever")
    ap.add_argument("--interval", type=int, default=30, help="seconds between scans")
    ap.add_argument("--hook", default="", help="shell command; new-mail JSON on stdin")
    ap.add_argument("--party", default=None,
                    help="watch only inbox_<party> (kimi|fable|grok|muse); "
                         "own state/board/stop file")
    args = ap.parse_args()
    if args.party:
        SCOPE = args.party.lower().strip()
    if not args.once and not args.loop:
        args.once = True

    COMMS.mkdir(parents=True, exist_ok=True)
    scope = SCOPE or "all"
    print(f"[comms-daemon] root={ROOT} interval={args.interval}s scope={scope}",
          flush=True)
    try:
        log_event({"ts": utc_now(), "event": "start", "mode": "once" if args.once else "loop",
                   "interval": args.interval, "scope": scope})
    except Exception:
        pass

    if args.once:
        tick(args.hook or None)
        return 0

    while True:
        if should_stop():
            print("[comms-daemon] STOP file present — exiting", flush=True)
            try:
                log_event({"ts": utc_now(), "event": "stop", "scope": scope})
            except Exception:
                pass
            return 0
        try:
            tick(args.hook or None)
        except Exception as e:
            try:
                print(f"[comms-daemon] tick_error {e}", file=sys.stderr, flush=True)
            except Exception:
                pass
        time.sleep(max(5, args.interval))


if __name__ == "__main__":
    sys.exit(main())
