← [Back to Root](../README.md)

# Source

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

- **[Common](./common/README.md)** – shared utilities
- **[ETL](./etl/README.md)** – ingestion and feature logic
- **Train** – model training logic
- **Track**  – experiment and artifact tracking
- **Serve** – inference interfaces