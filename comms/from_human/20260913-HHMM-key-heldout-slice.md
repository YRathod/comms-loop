Key #7: fable may build a fresh HotpotQA held-out slice and evaluate on it
  (thread tinymodel/scalecircuit, continues s28). Scope: download the public HotpotQA
  distractor dev set (HF datasets "hotpot_qa", config "distractor", split validation) into
  tiny-model/data/ - the one network use beyond the HF model cache; freeze a slice of 100
  questions (fixed seed) that are NOT in LongBench hotpotqa docs 0-199, before any model
  reads it; that slice is never labelled, trained on, used as generator material or as DEV;
  at most 2 eval runs on it under this key, each pre-registered with a banded prediction,
  reviewer kimi; tagger LoRA training may continue under the key #6 rules (train-side docs
  only, provenance check CLEAN before every run, new hand labels only from downloaded docs
  outside the slice). Laptop GPU only, $0, no instances, no deletion of existing adapters or
  evidence, base models frozen. Expires 2026-09-15T00:00Z.