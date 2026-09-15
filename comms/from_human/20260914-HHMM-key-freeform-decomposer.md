Key #10: fable may build and evaluate the free-form decomposer of docs/PREREG-freeform-decomposer.md
  (thread tinymodel/scalecircuit, continues s44). Scope: LoRA fine-tune of Qwen2.5-1.5B-Instruct
  (0.5B fallback) on hand labels and teacher labels drawn ONLY from the HotpotQA distractor TRAIN
  split already in the HF cache (no new network use); the frozen local Qwen2.5-3B-Instruct may
  write teacher decompositions for train-split questions and those may enter training data - a
  one-time exception to "model outputs never enter training data", limited to the teacher and
  the train split; provenance check CLEAN before every run; pre-gate <= 15 min then one full run;
  freeze slice v4 (400 questions, seed 20260917) disjoint from every prior slice, hashed before
  any model reads it; exactly one eval run on it with the claim rule and band pinned in the
  pre-registration; reviewer kimi. Laptop GPU only, $0, no instances, no deletion of existing
  adapters or evidence, base models frozen. Expires 2026-09-16T00:00Z.