# src/

Reusable library code for the project shared across all execution environments.

---

## Contract

- `src/` contains reusable logic only
- How and when that logic runs is decided outside `src/`

---

## Layout

```
src/
  common/
  etl/
  train/
  track/
  serve/ #future
```

- `common/` – shared utilities
- `etl/` – ingestion and feature logic
- `train/` – model training logic
- `track/`  – experiment and artifact tracking
- `serve/` – inference interfaces