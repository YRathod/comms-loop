# v1 E0 (>60min arm) — root-cause + optimization pass, per standing policy

v1 §5 estimates E0 at ~2h GPU (6 Qwen runs). Root-cause before launch:

1. Padding: NOT the driver — collate pads to batch-max, not fixed 1024.
2. fp32 on RTX 5090 runs CUDA-core rate: no TF32 anywhere in
   kimi_train_sft.py. This is the dominant cost (matmul-heavy SFT at ~1/8
   tensor-core throughput).
3. Optimizer memory (AdamW fp32 states, 12GB on 1.5B) caps batch at 2/1 —
   changing it would deviate the frozen recipe.

Applied: TF32 enabled in the trainer (hardware precision mode, no recipe
change, protocol-noted). Expected 2-4x on the fp32 runs -> E0 lands under
~60 min instead of ~2h.
NOT applied: batch-size increase (4/2) — batch is part of the frozen
"identical except lr" recipe; dynamics stay pinned. Held in reserve if E0
still overruns; would come back to committee first.

V2 (3 runs) + V3 (11 runs) inherit the same TF32 path. — kimi
