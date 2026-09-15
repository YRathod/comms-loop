Key #8: fable may build held-out slice v2 and run ONE pre-registered eval on it
  (thread tinymodel/scalecircuit, continues s37). Scope: from the already downloaded HotpotQA
  distractor dev set (tiny-model/data/hotpot_distractor_validation.jsonl, no new network use),
  freeze 400 questions (seed 20260915) disjoint from LongBench docs 0-199, slice v1 and DEV2,
  hashed before any model reads them; never labelled, trained on, generator material or DEV;
  exactly one eval run, claim and band as pinned in docs/PREREG-heldout-v2-400.md (iterative +
  notes; mean >= +0.05 AND 95% interval excluding zero), reviewer kimi. Laptop GPU only, $0,
  no instances, no deletion of existing adapters or evidence, base models frozen.
  Expires 2026-09-15T12:00Z.