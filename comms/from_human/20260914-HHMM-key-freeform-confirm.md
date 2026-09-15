Key #11: fable may run the confirmation cycle of docs/PREREG-freeform-v2-confirm.md
  (thread tinymodel/scalecircuit, continues s53). Scope: regenerate teacher decompositions with
  the frozen local Qwen2.5-3B-Instruct on HotpotQA TRAIN-split questions only (HF cache, no new
  network use; the one-time exception of key #10 renewed for this key, never held-out rows,
  never the student's outputs), content-filtered and provenance-checked; one LoRA retrain of
  Qwen2.5-1.5B-Instruct on the 299 hand labels plus those teacher rows; pre-gate <= 15 min with
  the pinned one-hop check, fallback to the existing key-#10 pre-gate adapter if it fails; freeze
  slice v5 (400 questions, seed 20260918) disjoint from every prior slice, hashed before any model
  reads it; exactly ONE eval run with the a-priori claim (superset + notes, free-form hops) and
  the band pinned in the pre-registration; reviewer kimi. Laptop GPU only, $0, no instances, no
  deletion of existing adapters or evidence, base models frozen. Expires 2026-09-16T12:00Z.