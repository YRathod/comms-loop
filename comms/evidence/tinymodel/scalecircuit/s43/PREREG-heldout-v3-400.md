# Pre-registration: held-out slice v3, n = 400, ONE run, claim = superset (needs key #9; NOT built)

Written 2026-09-13 23:40Z by fable, before key #9 exists and before the slice exists. Follows the
v2 form (docs/PREREG-heldout-v2-400.md) with the claim and the probability derived from v2's frozen
result (comms evidence s39: superset +0.062, 95 percent interval [+0.036, +0.090]).

Construction: same as v1/v2 with seed 20260916, n = 400, drawn from the downloaded HotpotQA distractor
dev set after excluding LongBench docs 0-199, slice v1 (100), DEV2 (100) and slice v2 (400); contexts =
own 10 paragraphs + 8 other pool rows' paragraphs, shuffled; sha256 frozen before any model reads it.
Never labelled, trained on, generator material or DEV. No new network use.

Run: ONE pre-registered eval run, pipeline_exec.py unchanged since s29, adapter
models/tagger_v4clean_0.5b, reader Qwen2.5-3B-Instruct, keyword top-6 within 3000 tokens for every
wiring, docs 0-399, greedy.

Claimed wiring, fixed now: **superset** = each hop answered over its own retrieval, hop answers fed
into the next hop's retrieval query; the final read of the original question sees the baseline's own
top-6 chunks FIRST, then the hop chunks last-hop-first, packed under the same 3000-token budget; no
notes, no fallback. Everything else the script computes is diagnostic.

Band (unchanged): PASS = mean delta >= +0.05 AND the 95 percent bootstrap interval of the per-doc
delta (20000 resamples, seed 0) excludes zero.

Prediction, derived from v2's superset interval rather than judgment: delta +0.03 to +0.09;
P(PASS as defined) about 0.6 (v2's point estimate +0.062 sits above the band with the interval's lower
end at +0.036; a fresh slice regresses toward the pooled mean, hence not higher). Falsifier: delta <=
+0.02. Result mail assembled from result_block.py output only.
