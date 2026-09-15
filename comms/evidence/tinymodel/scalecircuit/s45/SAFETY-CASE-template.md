# Safety case, per cycle (template; assembled mechanically by scripts/safety_case.py)

Top claim: this cycle's result is trustworthy and the run caused no harm. Each sub-claim is SUPPORTED
only by a file the assembler read; an UNSUPPORTED sub-claim is a HOLD until fixed or ruled by the reviewer.

| sub-claim | evidence the assembler reads | gate that enforces it |
|---|---|---|
| 1 authority | KEYS.md row + from_human file, expiry vs result time | trainer/pipeline refuse without a key in scope (manual today; expiry check in the assembler) |
| 2 no contamination | <train>.provenance.json (sha + verdict), slice meta hash | trainer refuses unstamped or FAIL; SUSPECT needs --allow-suspect + disclosure |
| 3 no goal motion | mtimes: pre-registration and gate before the result artifact | alignment gate stamp-order leg |
| 4 honest numbers | frozen result block re-derived from the result JSON | result_block.py; mails paste blocks |
| 5 bounded resources | heartbeat elapsed vs cap; key expiry | --max-seconds wall-clock kill in trainer and pipeline |
| 6 data safety | <generated>.content_filter.json counts | content_filter.py drops PII / harmful rows before training |
| 7 reversibility | gate.json (base, seeds, config); adapters and evidence kept | never delete; determinism check between runs |

Reviewer signs at cycle close. Proposed protocol clause (v1.18): a cycle does not bank until its safety
case is assembled from artifacts and every sub-claim is SUPPORTED or explicitly ruled by the reviewer.
