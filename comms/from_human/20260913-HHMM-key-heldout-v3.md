Key #9: fable may build held-out slice v3 and run ONE pre-registered eval on it
  (thread tinymodel/scalecircuit, continues s42). Scope: from the already downloaded HotpotQA
  distractor dev set (tiny-model/data/hotpot_distractor_validation.jsonl, no new network use),
  freeze 400 questions (seed 20260916) disjoint from LongBench docs 0-199, slice v1, DEV2 and
  slice v2, hashed before any model reads them; never labelled, trained on, generator material
  or DEV; exactly one eval run, claim and band as pinned in docs/PREREG-heldout-v3-400.md
  (superset wiring; mean >= +0.05 AND 95% interval excluding zero), reviewer kimi. Laptop GPU
  only, $0, no instances, no deletion of existing adapters or evidence, base models frozen.
  Expires 2026-09-15T12:00Z.