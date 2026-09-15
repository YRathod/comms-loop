# Retro of the third window (key #8, 2026-09-13 21:49Z - 2026-09-14 01:10Z), fable

Direction: "added key #8 and KEYS.md row 8 - verify and go". Scope: slice v2 (n = 400) and ONE eval run
with the claim and a statistical band pinned before the key existed (docs/PREREG-heldout-v2-400.md, 20:22Z).

## Outcome (numbers pasted from the frozen s39 block and band-verdict file; reviewer recomputed from raw)

| item | value | status |
|---|---|---|
| slice v2 | 400 questions, seed 20260915, disjoint from LongBench 0-199, slice v1 and DEV2; 326 bridge / 74 comparison; contexts ~51K chars; sha256 a30290cc... frozen 21:49Z before any model read it; reviewer overlap check 0 | clean |
| single-pass baseline | 0.423 | |
| claimed: iterative + notes | 0.461, +0.038, 62 up / 33 down | mean < +0.05 |
| 95% interval of the delta | [+0.006, +0.071] | excludes zero |
| pinned band (mean >= +0.05 AND interval excludes zero) | **NOT PASSED** | one leg met, one not; verdict by criterion, no adjudication needed |
| prediction +0.03 to +0.08, P(PASS) ~0.45 | HIT; realised P 0.24 | third consecutive prediction hold; the P estimate is a calibration datum |
| diagnostic, not claimed: superset | +0.062, [+0.036, +0.090], 47 / 16 | would have met both legs; never a candidate; on v1 it ranked below notes |
| reviewer ruling (kimi s41) | NOT PASSED, decisive; mechanism real (+0.04); alignment CLEAN | thread parked |

## The two-day arc, closed
- Day-one question: does decomposition beat single-pass by +0.05 on held-out HotpotQA? Answer, at
  n = 400 with everything pre-registered: the mechanism is worth about +0.04 F1 (decisively above
  zero) and the +0.05 goal is NOT met by the claimed wiring. Both sentences are measured.
- Every number that reached a mail in this window came from a frozen file rendered by
  scripts/result_block.py; zero corrections this window (two in window 2, five disclosures across
  the windows, zero reviewer-detected violations).
- Seq races: my s38 and s39 raced the reviewer's s38 verdict and were retro-assigned s39 and s40;
  ledger ids keep the archived filenames, titles carry the retro-assignment.

## What worked
- The statistical band fixed a priori: the decisiveness question was answered by criterion. The
  reviewer had nothing to adjudicate except arithmetic.
- Hash before read, key before build, claim before key: the order of events is verifiable, not
  just the numbers.
- The result-block tool: the first window with zero corrections.

## What did not
- The claim chosen on n = 100 (notes) was not the best arm at n = 400 (superset). Rankings at n = 100
  are noise, as ruled twice before; the a-priori claim paid the price of being fixed early, which is
  the right price.
- The P(PASS) estimate (0.45) was high against a realised 0.24; the delta prediction was fine, the
  probability was optimistic. Next pre-registration should derive P from the previous slice's
  interval rather than from judgment.

## If there is a next window (key #9)
- Slice v3 from the remaining pool (about 6600 questions unused), n = 400, new seed; claim fixed now:
  superset (baseline chunks first, then hop chunks, same budget); band unchanged (mean >= +0.05 AND
  interval excludes zero); prediction derived from v2's superset interval: +0.03 to +0.09, P(PASS) about
  0.6; falsifier <= +0.02. One run, ~3 hours.
- Tagger anchor gap (20/30 clean) stays open; the pipeline's gain does not depend on it strongly
  (comparison questions are NA either way), so it is second priority.
