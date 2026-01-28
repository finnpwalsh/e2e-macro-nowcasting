← [Back to Source](../README.md)

# Common

Shared domain utilities used across the nowcasting lifecycle.

---

## Contract

- Provides stage-independent logic reused by `etl/`, `train/`, `track/`, and `serve/`
- Must not assume or depend on a specific lifecycle stage

---

## Layout

```
common/
  evaluation/
  storage/
```

- **[Evaluation](./evaluation/README.md)** – shared model evaluation metrics and diagnostics
- **[Storage](./storage/README.md)** – shared storage abstractions and path helpers