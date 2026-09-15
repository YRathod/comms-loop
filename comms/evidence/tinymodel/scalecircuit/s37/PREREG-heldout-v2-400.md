# Pre-registration draft: held-out slice v2, n = 400 (needs a new human key; NOT built)

Why: at n = 30 / 100 every wiring's 95 percent interval straddles the +0.05 band (s21, s26, s30-s33).
A 400-question slice halves the interval width (about +-0.03) so a +0.05 claim can pass or fail
decisively. Key #7 names a 100-question slice and two eval runs on it; a 400-question slice is a new
scope and waits for key #8.

Construction, fixed now so it cannot drift: same as slice v1 (docs/PREREG-heldout-v1.md) with
seed 20260915, n = 400, drawn from the pool after excluding LongBench docs 0-199, slice v1 (100) and
DEV2 (100); contexts = own 10 paragraphs + 8 other pool rows' paragraphs, shuffled; sha256 frozen
before any model reads it. Never labelled, trained on, generator material or DEV.

Runs under key #8: ONE pre-registered eval run on v2 (about 3.5 h on the laptop GPU at 0.5 min per
question). Claimed wiring fixed NOW, before the slice exists: **iterative + notes** (s35/s36). Band,
with the statistics inside it (reviewer's rider, s36): PASS = mean delta >= +0.05 AND the 95 percent
bootstrap interval of the per-doc delta (20000 resamples, seed 0) excludes zero; otherwise NOT PASSED,
with the mean and interval reported. Prediction, written now: delta +0.03 to +0.08, P(PASS as
defined) about 0.45. Falsifier: delta <= +0.02. Everything else the script computes is diagnostic.
