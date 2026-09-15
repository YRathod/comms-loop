# Instance teardown inventory — archiving task for you (fable)

Full inventory: docs/instance-teardown-inventory.md (in-repo). Summary:

MUST PARK before the instance is deleted:
- B1: 13 remote-only trained checkpoints, ~18.6G (list in doc: arcdiv4x750
  x2, arcdiv8 gpt2 x2, loanrc2 x3, qwen05-arcdiv8 x2, v17-gpt2-brw-s777,
  v17-qwen05-brw x2). R2 upload recommended (creds via tmp_r2.env +
  scripts/_r2_*.py). Note kimi-gpt2-loanrc2-warm may duplicate the
  models/frozen/ copy — verify before uploading.
- B2: session logs at instance root (brw_*.{py,log}, v17r/v18/v19/v20/v21
  *.log) — the only process narratives of the v17-v21 batches, <50M.
- B3: baselines manifest diff (149 non-contamination files remote; v81-era
  set confirmed local — pull stragglers only).

SAFE already (verified): all contamination_v1/v2 artifacts (pulled),
models/frozen (identical 12 dirs local), data/{tasks,worlds,v20,...},
scripts (local is source), base models (HF re-downloadable).

DISPOSABLE (dies with instance): scratch/ checkpoints (probed, disposable
per dispatch), upload residue, queue logs.

Deleting the instance is the human's call after your archiving completes.
— kimi
