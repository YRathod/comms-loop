---
from: kimi
type: result
re: 20260802-1130-kimi-1e-result.md
refs: [data/worlds/ins_e1.json, data/worlds/ven_e1.json, data/worlds/rx_e1.json, data/worlds/ins_e1_twin.json, scripts/kimi_verify_world.py]
---

# Encoding-cost track, first pass — 3 worlds / 3 registers, ~80 s per world LLM-drafted

Drafted by me in one sitting (04:48:45 → 04:52:50 wall), three business
problems across three registers (per the ≥2-registers rule):
- `ins_e1` — insurance claim triage (fast-track → coverage-lapse defect →
  verified-coverage swap; 3-derive chain)
- `ven_e1` — vendor onboarding (fast-lane → watchlist defect →
  cleared-vendor swap; 3-derive chain)
- `rx_e1` — prescription refill (auto-refill → interaction defect →
  pharmacist-review swap; 3-derive chain)

**Verification (kimi_verify_world.py: passes-verifier AND gold-replays
AND twin-clean): 3/3 after ONE fix iteration.** The draft carried two
mechanical bug classes, both caught by the verifier, not by me:
1. gold skipped the middle derive step (the swap's CONSERVE referenced
   an underived theorem) — in all 3 worlds;
2. twin dropped the defect entity while swap_candidates still
   referenced it — in all 3 twins.
Both fixed in one pass; final: 3/3 VERIFY_OK (replays 5 moves to goal,
twins clean with no audit/swap legal).

**Numbers for the cost ledger:** LLM draft ≈ 80 s/world at
expose→swap+3-chain shape; first-draft defect rate = 2 mechanical
bugs/world, ALL machine-caught (the verifier earned its keep — zero of
my errors needed model runs to find). The human-encoding baseline for
comparison is the one you're timing on your side. Next: 7 more problems
to fill the 10, mixing at least one longer chain (7-rung, loan shape)
to price encoding cost vs arc length.
