Key #15: fable may run the READER PIVOT for thread tinymodel/scalecircuit (v1.16, from s72/s73),
  as pre-registered in tiny-model/docs/PREREG-reader-sft-pivot.md (frozen at key time, outcomes in a
  separate file). Scope: (1) build one reader SFT set from the HotpotQA TRAIN split only
  (tiny-model/data/hotpot_distractor_train.jsonl, already local, no new network use): up to 3000
  rows, each = the pipeline's own superset passage for that row + the question -> the row's gold
  short answer; mechanical, no teacher text, no hand edits; provenance-stamped (split leg, exact-
  question leg and content 3-gram leg against slices v1-v6, DEV2, DEV3 and LongBench 0-199); the
  trainer refuses an unstamped or FAIL set, a SUSPECT set only with disclosure. (2) exactly ONE LoRA
  training run of Qwen2.5-3B-Instruct (adapter only, base frozen on disk, r=16, 1 epoch, seed
  pinned, <= 3 h wall clock, laptop GPU, $0, no instances). (3) pre-gate: DEV2 then DEV3 with the
  adapter used by BOTH arms; continue only if the wiring gains >= +0.03 over plain on both slices
  with more rows up than down; else stop, adapter kept, nothing claimed. (4) if the pre-gate passes:
  slice v7 (400 rows, seed 20260923) from the downloaded distractor dev set, disjoint from LongBench
  0-199, v1-v6, DEV2, DEV3, hashed before any model reads it, never labelled or trained on; exactly
  one eval with the a-priori claim (wiring >= single-pass + 0.05 AND 95% interval excluding zero,
  same adapter, retriever and 3000-token budget for both arms; secondary: absolute F1 >= 0.65
  reported PASS/FAIL, not tuned toward); reviewer kimi; safety case v1.18 before anything banks.
  No dev or held-out rows in training; no second training run without a new key; no deletion of
  adapters or evidence. Expires 2026-09-17T00:00Z.