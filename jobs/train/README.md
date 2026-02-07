← [Back to Jobs](../README.md)

# Train
Training jobs produce canonical model artifacts and training-time evaluation outputs. 

---

## Contract

Training jobs are executable entrypoints that:
- Train models and produce versioned artifacts (model, metrics, predictions, `run.json`)
- Write only training artifacts consumed by downstream tracking, selection, and serving jobs

Training jobs are not responsible for:
- selecting, promoting, or retiring models
- performing online or serving-time inference
- mutating datasets produced by `prepare/`
- publishing models to external systems (handled by `track/`)

---

## Layout

```
jobs/train/
  baseline.py
```