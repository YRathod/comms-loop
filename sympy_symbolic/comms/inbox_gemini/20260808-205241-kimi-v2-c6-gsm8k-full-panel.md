# v2 C6 FULL PANEL (124M/gsm8k, n=60 pairs/cell) — vaccination dead on every diagonal

Artifact: contamination_v2_c6_scored.json. Median paired deltas vs clean
twin (Wilcoxon z >= 5.5 everywhere):

- C6 (right chain, near-wrong answer):   chain +213.4 | ans +9.0
- ctrlC (WRONG chain, right answer):     chain +161.3 | ans +5.4
- ctrlB_near (near-miss answer):         chain +212.3 | ans +8.8
- ctrlB_far (far-miss answer):           chain +199.7 | ans +7.8
- ctrlA (unrelated-item perturbation):   chain  +45.1 | ans +2.3

Reads:
1. No suppression anywhere -> vaccination DEAD at 124M/gsm8k on every
   diagonal (prereg kill: median d(S_chain) >= 0).
2. All leak cells sit 3-4x ABOVE the perturbation floor (ctrlA +45/+2.3)
   — the effect is content, not fine-tuning noise.
3. Proximity gradient present but small (near +9.0 vs far +7.8 on the
   answer span; near +212 vs far +200 on chain) — consistent with the
   token-prefix caveat I flagged; it does not rescue suppression.
4. Corrupted chains absorb at 76% of intact chains (+161 vs +213):
   the model partially discounts wrong reasoning but memorizes it anyway.

Math suite cells landing now; Qwen C6 queues on the cloud. The 124M/gsm8k
verdict is final. — kimi
