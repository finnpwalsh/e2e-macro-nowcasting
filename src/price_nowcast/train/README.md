← [Back to Source](../README.md)

# Train

Model training logic.

---

## Contract

- Consumes model-ready datasets produced by `etl/`
- Does not perform experiment tracking or serving

---

## Responsibilities

- Train task-specific models
- Compute training/evaluation metrics and summaries
- Write versioned model artifacts and metadata for downstream `track/` and `serve/`

---

## Layout

```
train/
  baseline/
  residual/ # V2
  evaluate/ # V2
```