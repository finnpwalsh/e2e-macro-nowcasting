← [Back to Source](../README.md)

# Nowcast

Domain logic for macroeconomic nowcasting.

---

## Contract

- Contains domain-specific, reusable logic only
- Logic is runtime-agnostic and free of orchestration concerns
- How and when logic executes is decided outside `src/`

---

## Layout

```
src/nowcast/
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