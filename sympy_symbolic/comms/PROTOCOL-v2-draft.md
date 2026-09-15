# SymPy Symbolic Flow — Committee Protocol v2 (DRAFT)

**Scope:** subproject `sympy_symbolic/` only. Supersedes PROTOCOL.md (v0.2) on adoption.
**Status:** DRAFT for member review — dry-run in progress.

## 1. Seats

Six seats, all with **write standing** (may drop mail into any inbox; daemon watches each):

- **Kimi** — chair; builds, reconciles, executes unassigned lanes
- **Fable** — science review; soundness, taxonomy, pass-bar rigor. **Science BLOCK has veto weight.**
- **Grok** — attack/tooling review; security, determinism, CI, pins. **Tooling BLOCK has veto weight.**
- **Gemini** — third eye; hidden assumptions, edge cases, alternative designs
- **DeepSeek** — dev / code review
- **Muse** — alternate chair + automation/verification; respects HOLD; no GPU without human key

Write standing is **not** authorization to train: rule 9 (human-signed key before any training run) binds every seat.

## 2. Mail conventions

- Files under `sympy_symbolic/comms/inbox_<party>/`
- First H1: `# <thread>: <title>`; status tags `[OPEN] [ACK] [BLOCK] [GO] [NACK] [PING] [ABSTAIN]`
- Reviewers reply in `inbox_kimi/`
- **Clock rule:** all windows run on **file mtime**, never filename or header stamps.

## 3. Decision rule

- Chair drafts, sends to every seat. Each seat may: ACK, NACK (reason), BLOCK (mandatory fix).
- GO requires no BLOCK after at least one ACK from each seat or 48h silence.
- **Three-try rule:** a seat not responding after three chair attempts is **ABSTAIN** (recorded on ledger); chair proceeds with respondents.

## 4. Assignment lifecycle (binding order)

1. **Assign** — chair posts the taskcard with seat, deliverable, timebox.
2. **Predictions + method** — assignee files both before executing (anti-postdiction).
3. **Review** — designated reviewer ACKs or BLOCKs the method.
4. **Execute** — only after review ACK.
5. **Artifact + results note** — with denominators, seeds, SHAs as applicable.
6. **Verdict** — reviewer scores; ledger line cut.

## 5. Liveness rules (human-directed 2026-08-06)

- **5-minute status rule.** While an assignment is active, the chair polls assignees' inboxes every 5 min until pre-work (predictions/method) lands, then every 15 min until artifacts. Poll outcomes noted on the thread, not spammed. When no task is assigned, polling is paused.
- **Chair-query response duty.** Any seat MUST respond to a direct chair question/status request — even "no progress yet" — before the next poll. A silent seat on a direct query = one attempt under the three-try rule. Three silent queries = ABSTAIN.
- **Ping escalation.** 3 empty polls => PING (attempt counter in subject). 3 pings unanswered by substance => ABSTAIN + reassignment or chair-execute.
- **Content-ACK rule (anti-ackstorm).** An ACK with no thread-specific content ("ACKed s1 mail") does not count as engagement for assignments — only as receipt confirmation. Escalation counts **substantive** replies only.

## 6. Compute discipline

`docs/compute_checklist.md` (L1–L7) is binding on every cycle: unbounded-inner-call check, space-not-construction metrics, eval cadence, cache honesty, per-point resumable tasks, instrument dynamic range, **60-minute arm rule** (any arm >60 min or >2× estimate triggers a 5-why root-cause before continuing, finding posted to the committee).

## 7. Reserved tokens

`data/manifests/reserved_op_tokens.json` + `scripts/reserved_tokens.py` are binding: generation-time blacklist, loud failure, never unreserve.

## 8. Housekeeping

- Daemon (`comms/daemon.py`) watches all six inboxes; PENDING.md is the wake board; archive/ holds processed mail.
- LEDGER.md archives to `LEDGER.<tag>-<date>.md` on protocol version changes; fresh ledger starts per version.
- Zombie processes (duplicate daemons, stale responders) are killed on sight by the chair — they caused GPU contention OOMs on 2026-08-06.
