Key #12: fable may develop and evaluate the VERIFY reader arm of docs/PREREG-verify-arm.md
  (thread tinymodel/scalecircuit, continues s59). Scope: development on DEV2 only (100 questions,
  never a held-out slice): mechanical constraint extraction (years, dates, numbers, ordinals,
  role nouns), verbatim-quote check, constraint-filtered retry, applied identically to the
  single-pass baseline and to the wiring; pinned stop if right-to-wrong flips exceed one third
  of wrong-to-right; no training, no new network use, frozen models only (Qwen2.5-3B-Instruct
  reader, the existing key-#10 decomposer adapter); freeze slice v6 (400 questions, seed
  20260919) disjoint from every prior slice, hashed before any model reads it; exactly ONE eval
  run with the a-priori paired claim and band pinned in the pre-registration; reviewer kimi.
  Laptop GPU only, $0, no instances, no deletion of existing adapters or evidence.
  Expires 2026-09-17T00:00Z.