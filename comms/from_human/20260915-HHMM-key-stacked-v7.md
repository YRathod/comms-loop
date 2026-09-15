Key #14 (CONDITIONAL): fable may build held-out slice v7 and run ONE pre-registered eval on it
  (thread tinymodel/scalecircuit, continues s72), valid ONLY if the stacked wiring of
  tiny-model/docs/PREREG-2026-09-15-overnight-65.md reaches superset+notes-class F1 >= 0.60 on
  BOTH DEV2 and DEV3 (frozen jsons under comms/evidence/tinymodel/scalecircuit/s72), else void
  unused. Scope: from the already downloaded HotpotQA distractor dev set
  (tiny-model/data/hotpot_distractor_validation.jsonl, no new network use), freeze 400 questions
  (seed 20260922) disjoint from LongBench docs 0-199, slices v1-v6, DEV2 and DEV3, hashed before
  any model reads them; never labelled, trained on, generator material or DEV; exactly one eval
  run with the a-priori claim pinned in the prereg (stacked wiring >= single-pass + 0.05 AND 95%
  interval excluding zero; secondary: absolute F1 >= 0.65 reported PASS/FAIL); same reader,
  retriever and 3000-token budget for baseline and wiring; no training, no labels; reviewer kimi.
  Laptop GPU only, $0, no instances, no deletion of adapters or evidence, base models frozen.
  Expires 2026-09-16T00:00Z.