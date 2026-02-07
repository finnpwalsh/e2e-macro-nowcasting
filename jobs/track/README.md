← [Back to Jobs](../README.md)

# Track

Tracking entrypoints log and register already-produced artifacts into metadata systems. Tracking is control-plane: it should not retrain models nor define artifact schemas.

---

## Contract

Tracking jobs are executable entrypoints that:
- Read `run.json` and referenced artifacts from storage
- Delegate backend-specific tracking to `src`
- Treat tracking as best-effort: training artifacts remain valid even if tracking fails

Tracking jobs are not responsible for:
- training or retraining models
- mutating model artifacts or metrics
- selecting, promoting, or retiring models
- defining artifact schemas or storage layout

---

## Layout

```
jobs/track/
  publish.py
```