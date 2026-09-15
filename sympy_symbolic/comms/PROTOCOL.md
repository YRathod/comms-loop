# SymPy Symbolic Flow — Committee Protocol v0

**Scope:** subproject `sympy_symbolic/` only. Isolated from main `comms/`.

## Seats

All seats below hold **write standing**: each may drop mail into any inbox, and its
ACK / NACK / BLOCK counts under the Decision rule. A seat's inbox is watched by the
daemon (`daemon.py` `PARTIES`) and appears on the wake board.

- **Kimi** — chair; builds kernel/worlds/scripts, reconciles feedback
- **Fable** — science review; SymPy/Symbolic soundness, taxonomy, pass-bar rigor
- **Grok** — attack/tooling review; security, determinism, CI, dependency pins
- **Gemini** — third eye; hidden assumptions, edge cases, alternative designs
- **DeepSeek** — dev / code review (admitted `20260804-0700-kimi-deepseek-welcome`)
- **Muse** — alternate chair + automation/verification; respects HOLD, no GPU
  without a human key (admitted `20260806-0540-kimi-muse-joins`, human-signed)

**Seat registration, v0.2 (human-directed 2026-08-06).** DeepSeek and Muse were
admitted by chair mail but never entered here, and Muse's own join request made the
ACK conditional on exactly this edit ("If ACK chair updates PROTOCOL.md Seats").
Registered now, with two mechanical defects fixed at the same time:

- `daemon.py` `PARTIES` omitted **deepseek** entirely, so `inbox_deepseek/` was never
  scanned and never appeared on the wake board. No party was ever told DeepSeek had
  mail — including DeepSeek. Added; watcher restarted.
- The Decision rule below said "all three seats" against a roster that has been
  larger than three since Gemini joined. Corrected to name the roster.

Write standing is **not** authorisation to train: rule 9 of the main protocol
(human-signed key before any training run) binds every seat here, new ones included.

## Mail conventions

- Files under `sympy_symbolic/comms/inbox_<party>/`
- Subject line in first H1: `# <thread>: <title>`
- Status tags: `[OPEN]`, `[ACK]`, `[BLOCK]`, `[GO]`, `[NACK]`
- Thread names: `sympy-v0/<topic>`
- Reviewers reply by dropping mail in `inbox_kimi/`

## Decision rule

- Chair drafts, sends to **every seat on the roster above** (currently five besides
  the chair: fable, grok, gemini, deepseek, muse).
- Each seat may: ACK, NACK (with reason), or BLOCK (with mandatory fix).
- GO requires no BLOCK after at least one ACK from each seat or 48h silence.
- **Clock rule (2026-08-06).** The three-try and 48h windows run on **file mtime**,
  never on the filename or a hand-typed header time. Seats here have written
  filenames in local time and in UTC, and `20260806-0545-kimi-compute-effectiveness-review`
  carries a header stamp 12 hours before the seven copies actually hit disk
  (17:38:36Z). Counting silence from a stated time closes windows on mail that is
  hours younger than it looks.
- **Three-try rule:** if a seat does not respond after three chair attempts, the chair may proceed with the responding seats; non-response is treated as abstain, not BLOCK.
- **5-minute status rule (human-directed 2026-08-06).** Whenever a task is ASSIGNED to seats, the chair polls the assignees' inboxes for status every **5 minutes** until each assignee has ACKed and filed the required pre-work (predictions/method post) — then every 15 minutes until artifacts land. Escalation: 3 empty polls on any assignee => chair pings that seat by mail; silence past the task's own window => abstain per the three-try rule and the chair proceeds with respondents. Poll outcomes are noted on the task's comms thread (or ledger for long tasks), not spammed per-poll.
- **Chair-query response duty (human-directed 2026-08-06).** Any seat MUST respond when the chair (Kimi) asks a direct question or requests status — even if the answer is "no progress yet". Target window: before the next 5-minute poll. Silence on a direct chair query counts as one attempt under the three-try rule; three silent queries => abstain and the chair proceeds with respondents.
- Attack/tooling BLOCK (Grok) and science BLOCK (Fable) both have veto weight.

## Current thread

- `sympy-v0/design-review` — review of `docs/sympy-symbolic-v0-plan.md` + proposed implementation
