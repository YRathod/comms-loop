# Eval run pre-registration (the one remaining eval run of 2026-09-13), pinned 06:58Z before the run

- adapter: models/tagger_v4clean_0.5b (clean generator v4, s16/s18), whatever its tier numbers turn out to be
  (they are reported, not a gate for this run; the s16 prediction stands: structure 14-18)
- claimed wiring: iterative + shape fallback (s15 definition, unchanged; pipeline_exec.py frozen at s15)
- baseline: single-pass, same reader / retrieval / 3000-token budget; expected to reproduce s10's 0.370 exactly
- band: claimed wiring >= single-pass + 0.05 (GOAL, 04:30Z)
- prediction: claimed wiring at single-pass +0.02 to +0.08; PASS ~40 percent (s15)
- falsifier: <= single-pass +0.02 -> the iterative mechanism does not transfer; D2 report is the day's result
- all other wirings computed by the script are diagnostic, not claimed
- gate_eval_v4clean.json pins the script args
