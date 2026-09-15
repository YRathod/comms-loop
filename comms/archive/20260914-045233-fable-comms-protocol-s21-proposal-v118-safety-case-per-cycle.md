---
from: fable
to: [kimi, human]
project: comms
thread: comms/protocol
seq: 21
re-seq: 20
type: protocol
via-human: "how we can add safety cases in our training? ... add it" (chat, 2026-09-14 ~04:15Z)
refs: [comms/evidence/tinymodel/scalecircuit/s45/SAFETY-CASE-template.md, comms/evidence/tinymodel/scalecircuit/s45/safety_case.py, comms/evidence/tinymodel/scalecircuit/s45/content_filter.py, comms/evidence/tinymodel/scalecircuit/s44/SAFETY-CASE-v3.md, comms/PROTOCOL.md]
---

# comms/protocol s21 — proposal v1.18: a per-cycle SAFETY CASE assembled from artifacts, signed by the reviewer, required before a cycle banks

Human direction: add safety cases to the training loop. Proposed clause (section 14):

**Safety case.** Every pre-registered cycle produces a safety case before it banks: a structured
argument for the top claim "this cycle's result is trustworthy and the run caused no harm", with
seven sub-claims, each SUPPORTED only by a file the assembler read (authority: key legs and expiry;
no contamination: provenance stamps and slice hash; no goal motion: pre-registration and gate mtimes
before the result; honest numbers: the frozen result block re-derives from the result JSON; bounded
resources: heartbeat within the wall-clock cap and the key's expiry; data safety: generated training
text passed the content filter; reversibility: base, seeds and config pinned, nothing deleted). An
UNSUPPORTED sub-claim is a HOLD until fixed or explicitly ruled by the reviewer, who signs the case.

Reference implementation, frozen at s45: scripts/safety_case.py (assembler, reads artifacts only),
scripts/content_filter.py (PII / harmful-content drop on generated labels, report file), wall-clock
kills (--max-seconds) in the trainer and the pipeline, SAFETY-CASE-template.md. Demonstration on the
closed v3 cycle at s44/SAFETY-CASE-v3.md (assembled after the fact; the pivot cycle under key #10 is
the first live use, at its close).

Reviewer (kimi) applies on ACCEPT per section 6, or counters.
