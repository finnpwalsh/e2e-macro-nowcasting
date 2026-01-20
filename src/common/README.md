← [Back to Nowcast](../README.md)

# Common

Shared domain utilities used across the nowcasting lifecycle.

---

## Contract

- Provides stage-independent logic reused by `etl/`, `train/`, `track/`, and `serve/`
- Must not assume or depend on a specific lifecycle stage

---

## Layout

```
src/nowcast/common/
  evaluation/
  storage/
```

- **Evaluation** – shared model evaluation metrics and diagnostics
- **Storage** – shared storage abstractions and path helpers