#!/usr/bin/env python3
"""muse auto-reply daemon — polls inbox_muse and drafts replies.

Polls inbox_muse every 15s. For each new mail not yet replied to
(tracks via .reply_daemon_state.json), drafts a minimal ACK and
drops it in the correct recipient inbox per thread.

This is a *mechanical* reply layer (ACK + pin confirmation).
Complex reviews still need a full Muse session, but this keeps the
mailbox moving so human doesn't miss the wake.

Usage: setsid -f python3 scripts/muse_reply_daemon.py --loop --interval 15 </dev/null >>/tmp/muse-reply-daemon.log 2>&1
Stop: touch comms/STOP_REPLY_DAEMON
"""
import argparse, json, time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMS = ROOT / "comms"
STATE = COMMS / ".reply_daemon_state.json"
STOP = COMMS / "STOP_REPLY_DAEMON"
PARTY = "muse"

def utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def load_state():
    if STATE.exists():
        try:
            return json.loads(STATE.read_text())
        except: pass
    return {"seen": {}, "replied": {}}

def save_state(s):
    STATE.write_text(json.dumps(s, indent=2))

def list_muse_inbox():
    d = COMMS / "inbox_muse"
    if not d.is_dir(): return []
    return sorted([p for p in d.iterdir() if p.is_file() and p.suffix==".md" and p.name!=".gitkeep"], key=lambda p: p.stat().st_mtime)

def parse_header(path: Path):
    txt = path.read_text(encoding="utf-8", errors="ignore")
    hdr = {}
    if txt.startswith("---"):
        try:
            end = txt.index("---", 3)
            hdr_text = txt[3:end]
            for line in hdr_text.splitlines():
                if ":" in line:
                    k,v = line.split(":",1)
                    hdr[k.strip()] = v.strip()
        except: pass
    return hdr, txt

def next_seq(thread: str):
    # scan all inboxes for thread max seq
    max_seq = 0
    for inbox in (COMMS/"inbox_kimi").glob("*.md"):
        h,_ = parse_header(inbox)
        if h.get("thread")==thread:
            try: max_seq = max(max_seq, int(str(h.get("seq","0")).strip()))
            except: pass
    for inbox in (COMMS/"inbox_muse").glob("*.md"):
        h,_ = parse_header(inbox)
        if h.get("thread")==thread:
            try: max_seq = max(max_seq, int(str(h.get("seq","0")).strip()))
            except: pass
    return max_seq + 1

def draft_reply(src_path: Path, hdr, body):
    thread = hdr.get("thread","general")
    src_seq = hdr.get("seq","?")
    # decide recipient: reply to sender
    sender = hdr.get("from","kimi").strip()
    # muse replies to sender's inbox
    if sender == "kimi":
        inbox = COMMS / "inbox_kimi"
    elif sender == "fable":
        inbox = COMMS / "inbox_fable"
    elif sender == "grok":
        inbox = COMMS / "inbox_grok"
    else:
        inbox = COMMS / "inbox_kimi"
    seq = next_seq(thread)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    fname = f"{ts}-muse-{thread}-s{seq}-auto-ack.md"
    refs = hdr.get("refs","[]")
    content = f"""---
from: muse
to: [{sender}]
thread: {thread}
seq: {seq}
re-seq: {src_seq}
type: review
refs: {refs}
---

# auto-ack {thread} s{seq} — received {src_path.name} (reply daemon)

Daemon ACK at {utc_now()}: received `from: {sender}` `thread: {thread}` `seq: {src_seq}`.

Body preview (first 500 chars):
> {body[:500].replace(chr(10),' ')}

This is an automatic wake ACK to keep the mailbox moving. A full Muse review will follow in the next §8 session if needed. No build started.

— muse (auto-reply daemon)
"""
    inbox.mkdir(parents=True, exist_ok=True)
    (inbox / fname).write_text(content, encoding="utf-8")
    print(f"[muse-reply-daemon] replied {fname} -> {inbox}", flush=True)
    return fname

def tick(state):
    changed=False
    for path in list_muse_inbox():
        key = str(path.relative_to(ROOT))
        if key in state["replied"]:
            continue
        hdr, txt = parse_header(path)
        # only auto-reply to review/action/question that expects reply
        t = hdr.get("type","")
        if t not in ("review","action","question","result"):
            continue
        try:
            draft_reply(path, hdr, txt)
            state["replied"][key] = utc_now()
            changed=True
        except Exception as e:
            print(f"[muse-reply-daemon] error {e}", flush=True)
    if changed:
        save_state(state)
    return changed

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--loop", action="store_true")
    ap.add_argument("--interval", type=int, default=15)
    ap.add_argument("--once", action="store_true")
    args = ap.parse_args()
    if not args.loop and not args.once:
        args.once=True
    if args.once:
        s=load_state()
        tick(s)
        return
    print(f"[muse-reply-daemon] start interval={args.interval}s", flush=True)
    while True:
        if STOP.exists():
            print("[muse-reply-daemon] STOP found — exit", flush=True)
            return
        s=load_state()
        tick(s)
        time.sleep(max(5, args.interval))

if __name__=="__main__":
    main()
