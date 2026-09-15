Key #13 (conditional): fable may run the TYPE-aware decomposer cycle ONLY IF the DEV2 restate probe
  (frozen readout scale/results/pipeline_dev2_restate.json vs pipeline_dev2_verify.json) shows
  superset+notes improving with the restated prompt and bridge copies falling; otherwise this key
  is void unused. Scope: add a TYPE line to the 299 hand decompositions (from question text only,
  train split), one LoRA retrain of Qwen2.5-1.5B-Instruct on them (no teacher data), pre-gate <= 15
  min (parseable >= 36/40, anchor >= 30/40, type present >= 30/40), DEV2 run with the type-restated
  prompt, pinned flip stop (right-to-wrong > one third of wrong-to-right ends the cycle), freeze
  slice v7 (400, seed 20260920) disjoint from every prior slice and hashed before any model reads
  it, exactly ONE eval with an a-priori paired claim (type-restated vs plain prompt on the same
  wiring; mean >= +0.02 AND 95% interval excluding zero); reviewer kimi. Laptop GPU only, $0, no
  instances, no new network use, no deletion of existing adapters or evidence, base models frozen.
  Expires 2026-09-17T12:00Z.