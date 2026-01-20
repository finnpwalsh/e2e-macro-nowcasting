← [Back to Jobs](../README.md)

# Train
Training scripts produce **canonical model artifacts** and evaluation outputs. 

---

## Contract

- Train models and produce versioned artifacts (model, metrics, predictions, `run.json`)
- Write only training artifacts needed by downstream tracking and serving jobs

---

## Layout

```
jobs/train/
  baseline/
  residual/ # V2
  evaluate/ # V2
```