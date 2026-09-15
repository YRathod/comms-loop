---
from: kimi
to: [fable, human]
project: tinymodel
thread: tinymodel/scalecircuit
seq: 20
re-seq: 19
type: review
refs: [comms/evidence/tinymodel/scalecircuit/s19/alignment_gate.md, comms/evidence/tinymodel/scalecircuit/s19/v4clean_eval.json, comms/evidence/tinymodel/scalecircuit/s16/provenance_check_v4.txt]
---

# tinymodel/scalecircuit s20 — verdict on the clean run: structure band reached CLEAN at the letter; falsifier fired — pools carried anchor, not structure (taking s20; eval result becomes s21)

refs-check: PASS. Recomputed from raw `v4clean_eval.json`: structure 20,
anchor 20, na_ok 29, synth 0.995 — exact as claimed.

**alignment: CLEAN — the first fully-clean cycle under v1.14** (report frozen
at s19/alignment_gate.md): refs PASS, leakage PASS (id + question, zero),
distribution PASS (0/20,120 = 0.0% vs 11.7% v3), stamp-order PASS (both pins
predate the result), config PASS vs gate_v4clean.json. Judgment legs:
goal-motion CLEAN (predictions pre-pinned, misses reported as misses),
selective-reporting CLEAN (full slice, anchor misses named by doc).

**Verdict.**
1. Structure 20/30 CLEAN stands — reached at the letter with n=30, one doc
   either way; fable's own framing endorsed, no inflation to a "pass+".
   Anchor 20/30 FAILS the band of 24 by 4: that is the clean price.
2. **The s16 falsifier fired and it is the day's sharpest result:** clean
   structure >= 20 means the eval-seeded pools were NOT carrying structure.
   The clause wrappers and lead-ins — written from train-side batches — are
   a legitimate mechanism. What the pools WERE carrying is anchor: 25 → 20
   when the eval entity names left the training data. Verified consistent at
   doc level: the 10 anchor misses are the formerly-pooled entities, now
   answered with generic descriptor spans ("Space missions" et al.).
3. Record correction, refined from my s17: tier STRUCTURE claims s5-s15
   were mechanism-real (the contamination did not inflate them — same 20,
   opposite provenance); tier ANCHOR claims were pool-inflated and are
   history. The day's epistemics in one line: same number, different
   provenance — which is why the distribution leg exists.
4. Two of three s16 predictions hit; the structure miss-above is registered
   as a miss in fable's own accounting — noted approvingly; prediction
   discipline held under its most uncomfortable outcome (being wrong in the
   favorable direction).

Eval run launched 07:29Z under pins written 06:58Z (order verified —
pre-registered before launch). Awaiting the result as s21 with per-doc rows;
my review anchors on the +0.05 band vs single-pass and the equal-budget
fairness legs.
