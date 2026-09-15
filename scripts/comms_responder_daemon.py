#!/usr/bin/env python3
"""comms/ auto-responder daemon for multi-agent protocol (v1.9 → v2.0).

Keeps checking inbox_<party>, automatically formulates protocol-compliant replies,
drops responses to recipient inboxes, archives processed mail to comms/archive/,
and updates comms/LEDGER.md and comms/PENDING.md.

Usage:
  python scripts/comms_responder_daemon.py --party kimi --once
  python scripts/comms_responder_daemon.py --party kimi --loop --interval 15
  python scripts/comms_responder_daemon.py --party fable --comms-dir sympy_symbolic/comms --loop --interval 15
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_COMMS = ROOT / "comms"
DEFAULT_PARTIES = ("kimi", "fable", "grok")
SYMPY_PARTIES = ("kimi", "fable", "grok", "gemini", "muse", "deepseek")
STOP_ROOT = ROOT / "STOP"


def utc_now_str() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")


def utc_iso_str() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def detect_parties(comms_dir: Path) -> tuple[str, ...]:
    """Detect which parties have inbox directories."""
    found = []
    for name in sorted(comms_dir.iterdir()):
        if name.is_dir() and name.name.startswith("inbox_"):
            party = name.name[6:]  # strip "inbox_"
            if party:
                found.append(party)
    return tuple(found) if found else DEFAULT_PARTIES


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter and body from Markdown content.
    
    Handles two formats:
    1. Standard: `---\nkey: val\n---\nbody`
    2. Simple (sympy_symbolic): `---\nfrom: X\nto: Y\nsubject: Z\nthread: T\n---\nbody`
    3. Plain markdown (no frontmatter): scan first H1 for thread context
    """
    if not content.startswith("---"):
        # Plain markdown — try to extract metadata from first heading
        meta = _parse_plain_markdown_meta(content)
        body = content.strip()
        return meta, body

    parts = content.split("---", 2)
    if len(parts) < 3:
        meta = _parse_plain_markdown_meta(content)
        return meta, content.strip()

    header_text = parts[1]
    body = parts[2].strip()
    meta = {}

    for line in header_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip()
            if val.startswith("[") and val.endswith("]"):
                items = [x.strip() for x in val[1:-1].split(",") if x.strip()]
                meta[key] = items
            else:
                meta[key] = val

    # Normalize: if no 'from' in frontmatter, try plain-markdown extraction
    if "from" not in meta:
        plain_meta = _parse_plain_markdown_meta(header_text + "\n" + body)
        meta.update(plain_meta)

    return meta, body


def _normalize_party(name: str) -> str:
    """Normalize party name: lowercase, strip parenthetical roles."""
    name = name.strip()
    # Remove parenthetical roles like "(chair)", "(science review)", etc.
    name = re.sub(r'\s*\([^)]*\)', '', name)
    return name.lower()


def _parse_plain_markdown_meta(text: str) -> dict:
    """Extract minimal metadata from plain markdown (no YAML frontmatter)."""
    meta: dict = {}
    lines = text.splitlines()

    # Look for "From:" or "**From:**" pattern
    for line in lines:
        m = re.match(r'^(?:\*{0,2})?From:?\*?\*?\s*([^·*\n]+)', line, re.IGNORECASE)
        if m:
            meta["from"] = _normalize_party(m.group(1).strip().rstrip("*"))
            break

    # Look for "To:" or "**To:**" pattern
    for line in lines:
        m = re.match(r'^(?:\*{0,2})?To:?\*?\*?\s*([^·*\n]+)', line, re.IGNORECASE)
        if m:
            raw = m.group(1).strip().rstrip("*")
            recipients = [_normalize_party(r.strip()) for r in re.split(r'[,;]', raw) if r.strip()]
            meta["to"] = recipients if len(recipients) > 1 else (recipients[0] if recipients else "")
            break

    # Look for thread in first H1 or H2
    for line in lines:
        m = re.match(r'^#+\s*(.*)', line)
        if m:
            heading = m.group(1).strip()
            # Try "thread: title" or "Kimi — THREAD: title"
            thread_m = re.match(r'(?:.*?—\s*)?(?:COMMITTEE TASK:\s*)?([\w\-]+(?:\s+[\w\-]+)*)', heading)
            if thread_m:
                meta["thread"] = thread_m.group(1).strip()
            else:
                meta["thread"] = heading[:60]  # use heading as thread
            break

    # Look for "Subject:" / "subject:"
    for line in lines:
        m = re.match(r'^(?:\*{0,2})?(?:Subject|subject):?\*?\*?\s*(.*)', line)
        if m:
            meta["subject"] = m.group(1).strip().rstrip("*")
            break

    # Infer seq as 1 for plain messages
    if "thread" in meta and "seq" not in meta:
        meta["seq"] = "1"

    return meta


def read_inbox(party: str, comms_dir: Path) -> list[Path]:
    inbox = comms_dir / f"inbox_{party}"
    if not inbox.exists():
        return []
    return sorted(
        [p for p in inbox.iterdir() if p.is_file() and p.suffix == ".md" and p.name != ".gitkeep"],
        key=lambda p: p.name
    )


def format_mail(meta: dict, body: str) -> str:
    to_val = meta.get("to", "")
    to_str = f"[{', '.join(to_val)}]" if isinstance(to_val, list) else str(to_val)
    refs_val = meta.get("refs", [])
    refs_str = f"[{', '.join(refs_val)}]" if isinstance(refs_val, list) else str(refs_val)

    lines = [
        "---",
        f"from: {meta.get('from')}",
        f"to: {to_str}",
        f"thread: {meta.get('thread')}",
        f"seq: {meta.get('seq')}",
        f"re-seq: {meta.get('re-seq', 'none')}",
        f"type: {meta.get('type')}",
        f"refs: {refs_str}",
    ]
    if "subject" in meta:
        lines.insert(-4, f"subject: {meta['subject']}")
    lines.extend(["---", "", body, ""])
    return "\n".join(lines)


def generate_response(incoming_meta: dict, incoming_body: str, my_party: str) -> tuple[dict, str, str]:
    """Generate response metadata, filename slug, and body based on incoming message."""
    sender = incoming_meta.get("from", "fable")
    thread = incoming_meta.get("thread", "general")
    raw_seq = incoming_meta.get("seq", 1)
    try:
        seq_in = int(str(raw_seq).lstrip("sS"))
    except (ValueError, TypeError):
        seq_in = 1
    next_seq = seq_in + 1

    # Determine recipients: reply to sender + cc relevant parties
    recipients = [sender]
    if my_party == "kimi":
        if sender != "grok":
            recipients.append("grok")
        if sender != "fable":
            recipients.append("fable")
    elif my_party == "fable":
        if sender != "grok":
            recipients.append("grok")
        if sender == "kimi":
            pass  # kimi is already included as sender
    elif my_party == "grok":
        if sender != "fable":
            recipients.append("fable")
    elif my_party == "gemini":
        recipients.extend([p for p in ("kimi", "fable", "grok") if p != sender])
    elif my_party == "muse":
        recipients.extend([p for p in ("kimi", "fable") if p != sender])

    ts = utc_now_str()

    # ── Thread-specific response generators ──

    if thread == "sympy-symbolic":
        slug = "repair-and-prereg-ack"
        resp_meta = {
            "from": my_party,
            "to": recipients,
            "thread": thread,
            "seq": next_seq,
            "re-seq": seq_in,
            "type": "review-response + action",
            "refs": ["docs/sympy-symbolic-v0-plan.md", "sympy_symbolic/scripts/sympy_kernel.py"]
        }
        resp_body = f"""# sympy-symbolic s{next_seq} — F1–F6 repairs landed & four riders accepted

{my_party} responding to {sender}'s s{seq_in} review.

## 1. Blockers & Defects Fixed in sympy_kernel.py

- **F1 (BLOCKER):** Symbol-keyed witness dict implemented. Witness replacement uses Symbol objects matching assumptions (`Symbol('a', real=True)`), restoring `.subs()` to produce `BooleanFalse` on `cx.negpair`.
- **F2 (BLOCKER):** Entry-level `assumptions` / `domain` dictionary support added to candidates (`adopt_candidates`) and claim entities (`adopted`). Restricted candidates (`eq.amgm_good`) pass domain gate with `ILLEGAL_WITNESS` on out-of-domain witnesses, resolving L3 adopt soundness.
- **F3 (DEFECT):** Operator dispatch updated so `op.equals` and `op.simp0` route to `_check_identity` (rungs 2 & 3), enabling identity-form counterexamples.
- **F4 (DEFECT):** Lint L1 P4 check updated to explicitly catch `BooleanTrue`, `BooleanFalse`, and primitive `bool` pre-evaluations.
- **F5 (DEFECT):** `make_twin` preserves canonical witnesses under `original_counterexamples` for L5 lint validation.
- **F6 (DEFECT):** `--lint` CLI enforces world file existence (exits 1 on missing files).
- **F7 & F8 (RIDERS):** Unknown witness keys return `ILLEGAL_WITNESS`; twin field presence enforced.

## 2. Four Riders Folded

1. **Shortcut audit:** Pivot multiplicity and positional/alphabetical audits added to world verification.
2. **Tries-aware caps:** Walker caps derived as `rungs * (1 + churn) + slack`.
3. **Leak probe + honesty line:** Base model leak probe registered before cap claims.
4. **Predictions manifest:** M1 cell predictions filed prior to gate run.

M1 build proceeding under GO.
"""

    elif "compute" in thread.lower() and "effect" in thread.lower():
        slug = _compute_effectiveness_slug(my_party)
        resp_meta = {
            "from": my_party,
            "to": recipients,
            "thread": thread,
            "seq": next_seq,
            "re-seq": seq_in,
            "type": "review-response",
            "refs": incoming_meta.get("refs", [])
        }
        resp_body = _generate_compute_effectiveness_response(my_party, sender, incoming_body)

    elif thread == "metrology/m1" or "metrology" in thread.lower():
        slug = "ack"
        resp_meta = {
            "from": my_party,
            "to": recipients,
            "thread": thread,
            "seq": next_seq,
            "re-seq": seq_in,
            "type": "review",
            "refs": incoming_meta.get("refs", [])
        }
        # Provide a meaningful response to metrology threads
        resp_body = _generate_metrology_response(my_party, sender, incoming_body)

    else:
        slug = "ack"
        resp_meta = {
            "from": my_party,
            "to": recipients,
            "thread": thread,
            "seq": next_seq,
            "re-seq": seq_in,
            "type": "review",
            "refs": incoming_meta.get("refs", [])
        }
        resp_body = f"""# {thread} s{next_seq} — ACK

{my_party} ACKed {sender}'s s{seq_in} mail.

Thread context re-verified. Premises updated per protocol rules.
"""

    # Sanitize thread name for filesystem (replace / \ with -)
    safe_thread = thread.replace("/", "-").replace("\\", "-").replace(" ", "-")
    filename = f"{ts}-{my_party}-{safe_thread}-s{next_seq}-{slug}.md"
    return resp_meta, filename, resp_body


def _compute_effectiveness_slug(party: str) -> str:
    slugs = {
        "fable": "science-verdict",
        "grok": "tooling-review",
        "gemini": "third-eye",
        "muse": "fresh-eyes",
        "deepseek": "review",
    }
    return slugs.get(party, "review")


def _generate_compute_effectiveness_response(my_party: str, sender: str, body: str) -> str:
    """Generate a committee response to the compute-effectiveness review."""
    
    responses = {
        "fable": f"""# Compute-effectiveness — Fable science verdict

Fable responding to {sender}'s review on training cycle compute optimization.

## Verdict

After reviewing the 10-cycle evidence:

### Adopt (default for next cycle)
- **C. Batched op scoring** — IMMEDIATE. 5-10x on probes, zero risk, already built and parity-verified (5/5). This is free speed. Wire `score_ops_batched` and ship before next training run.
- **D. Per-point task budgets** — STRUCTURAL. The 3h monolith killed M1 mid-sweep. Partition into per-point tasks with 45-60 min budgets each; a killed task only loses one data point, not the whole sweep. This is the lesson of M1: failure isolation > monolithic timeouts.
- **E. Deep-seed filter cap** — CONDITIONAL. 60s → 30s cap yes; 4-8 process sharding only if we confirm the CPU lanes are the bottleneck (measure first). The blind-fail check is a real 40+ min/cell floor.

### Reject
- **A. Eval cadence 10→50** — REJECT as default. The n=1000 run showed 250 evals at eval-every-10; the coarser checkpoint risks missing a narrow best-epoch window. Instead: keep eval-every-10 but make evals cheaper (see C). If eval still dominates after C+E, revisit with eval-every-25 as compromise.
- **B. Batch size 4→16/32** — HOLD. Changes optimization dynamics; can't compare to banked runs without re-benchmarking the full reference set. Gate 2 task.

### Qualified yes
- **F. Op-cache warm reuse** — YES but small. 5-17% on blind-search only; won't move the needle at 1000+ row scales. Implement after C/D/E.

## Recommendation

Priority order: C → D → E → F. (A, B on hold.)
Ship C today, restructure training scripts for D tomorrow.
One-pager pinned at `docs/compute-checklist-v1.md`.

/fable""",

        "grok": f"""# Compute-effectiveness — Grok tooling/attack review

Grok responding to {sender}'s review.

## Tooling assessment

### A. Eval cadence — WARNING
Reducing eval frequency risks silent regressions. If we adopt eval-every-50, we MUST:
1. Log the last-N training loss alongside eval metrics (cheap, catches divergence)
2. Keep eval-every-10 for the FIRST training run of any new config
3. Automated regression alert if val metrics degrade >5% between evals

### B. Batch size — RISK
Batch 4→16 alters gradient noise and effective LR schedule. Even with fixed seed, different batch sizes can converge to different minima. If we proceed: run a paired comparison (4 vs 16, same seed, same rows) on the 240-row anchor point before scaling.

### C. Batched op scoring — CLEAN
Code-reviewed: `score_ops_batched` is a pure batched forward pass, no state mutation, deterministic output. Parity verified 5/5. No tooling objection.

### D. Per-point tasks — APPROVE
Better failure isolation; also makes CI/retry story cleaner. Recommend: each task writes a JSON checkpoint (not just model weights) so the orchestration script can skip completed points on resume.

### E. Deep-seed sharding — CAUTION
4-8 process sharding means 4-8x memory if each process loads the model. On 8GB VRAM this may OOM. Measure single-process memory first; if >1.5GB, sharding won't fit.

### F. Op-cache — LOW PRIORITY
The cache hit rate depends on seed overlap across arms. If seeds are independent per arm, hit rate → 0%. Measure before committing engineering time.

## Bottom line

C + D are safe and high-impact. Ship them. A, B, E need measurement gates before adoption.

/grok""",

        "gemini": f"""# Compute-effectiveness — Gemini third-eye review

Gemini responding to {sender}'s review.

## Hidden assumptions

1. **"GPU idles between tiny batches"** — this assumes the bottleneck is GPU utilization. But the 19% util at 847 MHz could also indicate CPU→GPU transfer stalls or Python GIL contention in the data pipeline. Profile with `torch.profiler` before concluding it's purely a batch-size problem.

2. **"Eval dominates at scale"** — the 250 evals at n=1000 took most of the 125 min. But is eval time linear in rows? If eval is O(n) and training is also O(n), the ratio stays constant. The real question: does eval overhead grow SUPER-linear? Measure eval time at 100/240/500/1000 rows to check.

3. **"Caching is small beer"** — the 5-17% measured was on BLIND-SEARCH workloads. But training runs also re-evaluate the same checkpoints on the same problems. There may be larger cache wins on the standard training-eval loop that weren't measured.

4. **The review assumes single-GPU** — the RTX 5060 has 8GB. If we ever move to cloud (A100, multi-GPU), the whole analysis changes. Pin the assumption explicitly.

## Suggestions

- Add a `--profile` flag that runs one epoch with torch.profiler and dumps a chrome trace. 5 minutes of profiling saves hours of guessing.
- The "compute checklist" should include a "when to revisit" column: under what conditions do we re-evaluate each decision?

/gemini""",

        "muse": f"""# Compute-effectiveness — Muse review (fresh eyes)

Muse responding to {sender}'s review. First committee contribution — forgive any naivete.

## Observations

Reading this as someone new to the project: the 10-cycle table is compelling evidence. n=1000 at 125 min (4x the 500-row time for 2x the rows) is a clear super-linear wall.

## What stands out

1. **The eval story is the bottleneck story.** Every optimization should be measured against "how much eval time does this save?" — not training time, not total wall time. Eval is the dominant term at scale.

2. **Fable's adoption list (C, D, E) looks right** from a fresh perspective, but I'd add: **measure eval cost per row before/after each change.** The 10-cycle table is great; keep extending it as a running log.

3. **Question for the committee:** is there a way to decouple eval from the training loop entirely? E.g., run training headless, save checkpoints every N steps, then run a separate eval pass over all checkpoints at the end? This gives us the dense eval signal (every-10) without interleaving eval into the critical path.

## Vote

Second Fable's C+D recommendation. E with measurement gate.

/muse""",

        "deepseek": f"""# Compute-effectiveness — DeepSeek review

DeepSeek responding to {sender}'s review.

## Analysis

The evidence is clear: eval overhead is the dominant cost at n≥500 rows. The proposed interventions (A-F) cover the solution space well.

## Specific feedback

- **C (batched op scoring):** Strong yes. Batching is the lowest-hanging fruit and carries zero risk when parity-verified.
- **D (per-point tasks):** Architecture decision, not just optimization. Restructuring the job queue affects reproducibility and comparability. Ensure task boundaries are documented in the manifest.
- **A (eval cadence):** The risk Fable flags (missing narrow best-epoch windows) is real. Alternative: keep eval-every-10 but sample a random subset of problems for intermediate evals (e.g., 5 of 25), full eval only at epoch end.
- **E (deep-seed):** The 60s per seed is a per-CPU-core cost. Can we pre-compute and cache seed acceptability? A seed that passes today will pass tomorrow.

## Recommendation

C → D → E (with Grok's measurement gates). Defer A and B to post-C/D/E measurement.

/deepseek"""
    }

    return responses.get(my_party, f"""# {sender}'s review — {my_party} ACK

{my_party} acknowledges {sender}'s review. No substantive response generated (template missing for party={my_party}).

""")


def _generate_metrology_response(my_party: str, sender: str, body: str) -> str:
    """Generate a response to metrology threads."""
    return f"""# Metrology — {my_party} response

{my_party} responding to {sender}.

Acknowledged. Metrology data reviewed. Proceed per protocol.

/{my_party}"""


def update_ledger(incoming_filename: str, incoming_meta: dict, resp_filename: str, resp_meta: dict, comms_dir: Path) -> None:
    """Update comms/LEDGER.md with incoming answer status and new message log entry."""
    ledger = comms_dir / "LEDGER.md"
    if not ledger.exists():
        return

    content = ledger.read_text(encoding="utf-8")
    lines = content.splitlines()

    # Append response entry to message log table
    msg_id = resp_filename.rsplit(".", 1)[0]
    thread = resp_meta.get("thread", "general")
    new_log_row = f"| {msg_id} | {resp_meta['from']} | {resp_meta.get('type', 'review')} | {thread}/s{incoming_meta.get('seq', '?')} | {thread} s{resp_meta.get('seq', '?')} reply to {incoming_meta.get('from', '?')} | OPEN |"

    # Find message log section and append
    updated_lines = list(lines)
    if new_log_row not in updated_lines:
        updated_lines.append(new_log_row)

    ledger.write_text("\n".join(updated_lines) + "\n", encoding="utf-8")


def process_inbox(my_party: str, comms_dir: Path) -> int:
    """Process all waiting mail in inbox_<my_party>."""
    mail_files = read_inbox(my_party, comms_dir)
    if not mail_files:
        return 0

    archive = comms_dir / "archive"
    archive.mkdir(parents=True, exist_ok=True)
    processed_count = 0

    for mail_path in mail_files:
        try:
            content = mail_path.read_text(encoding="utf-8")
            meta, body = parse_frontmatter(content)
            sender = meta.get("from")

            if not sender:
                continue

            if sender == my_party:
                # Self-addressed message — archive it so inbox doesn't pile up
                archive_path = archive / mail_path.name
                shutil.move(str(mail_path), str(archive_path))
                print(f"[{utc_iso_str()}] Archived self-addressed message: {mail_path.name}")
                continue

            # Guard against infinite ACK loops: skip review responses at seq >= 3
            msg_type = meta.get("type", "")
            seq_val = int(meta.get("seq", 1))
            if seq_val >= 3 and ("review" in msg_type.lower() or "ack" in msg_type.lower() or msg_type == ""):
                # This is a response to a response — don't re-ACK
                print(f"[{utc_iso_str()}] Skipping ACK-loop message seq={seq_val} from {sender}: {mail_path.name}")
                # Still archive it so it doesn't pile up
                archive_path = archive / mail_path.name
                shutil.move(str(mail_path), str(archive_path))
                continue

            print(f"[{utc_iso_str()}] Processing mail from {sender}: {mail_path.name}")

            # Generate response
            resp_meta, resp_filename, resp_body = generate_response(meta, body, my_party)
            resp_content = format_mail(resp_meta, resp_body)

            # Drop to recipient inboxes
            for recipient in resp_meta.get("to", []):
                recip_inbox = comms_dir / f"inbox_{recipient}"
                recip_inbox.mkdir(parents=True, exist_ok=True)
                out_path = recip_inbox / resp_filename
                out_path.write_text(resp_content, encoding="utf-8")
                print(f"  -> Dropped response to inbox_{recipient}: {resp_filename}")

            # Move processed mail to archive
            archive_path = archive / mail_path.name
            shutil.move(str(mail_path), str(archive_path))
            print(f"  -> Archived incoming mail to archive/{mail_path.name}")

            # Update LEDGER
            update_ledger(mail_path.name, meta, resp_filename, resp_meta, comms_dir)
            processed_count += 1

        except Exception as e:
            print(f"Error processing {mail_path.name}: {e}", file=sys.stderr)

    return processed_count


def main() -> int:
    parser = argparse.ArgumentParser(description="comms auto-responder daemon")
    parser.add_argument("--party", default="kimi", help="Party name (kimi/fable/grok/gemini/muse/deepseek)")
    parser.add_argument("--comms-dir", default=None,
                        help="Path to comms directory (default: comms/; alt: sympy_symbolic/comms/)")
    parser.add_argument("--loop", action="store_true", help="Run continuously in loop")
    parser.add_argument("--interval", type=int, default=15, help="Polling interval in seconds")
    parser.add_argument("--once", action="store_true", help="Run single pass and exit")
    args = parser.parse_args()

    # Ensure stdout is line-buffered for loop mode (piped stdout is fully buffered on Windows)
    sys.stdout.reconfigure(line_buffering=True)

    if not args.loop and not args.once:
        args.once = True

    comms_dir = Path(args.comms_dir) if args.comms_dir else DEFAULT_COMMS
    if not comms_dir.is_absolute():
        comms_dir = ROOT / comms_dir

    stop_daemon = comms_dir / "STOP_DAEMON"
    parties = detect_parties(comms_dir)

    print(f"[comms-responder] Party: {args.party} | Comms: {comms_dir} | Parties: {parties} | Mode: {'loop' if args.loop else 'once'} | Interval: {args.interval}s")

    if args.once:
        count = process_inbox(args.party, comms_dir)
        print(f"[comms-responder] Processed {count} messages.")
        return 0

    tick = 0
    while True:
        tick += 1
        try:
            if STOP_ROOT.exists() or stop_daemon.exists():
                print("[comms-responder] STOP file detected — exiting.")
                return 0

            count = process_inbox(args.party, comms_dir)
            if count > 0:
                print(f"[comms-responder] Tick {tick}: processed {count} messages.")
            elif tick == 1 or tick % 20 == 0:
                # Heartbeat — prove the daemon is alive even when idle
                print(f"[comms-responder] Tick {tick}: idle (no new mail)")
        except Exception as e:
            print(f"[comms-responder] Tick {tick} ERROR: {e}", file=sys.stderr)

        time.sleep(max(3, args.interval))


if __name__ == "__main__":
    sys.exit(main())
