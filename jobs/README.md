← [Back to Root](../README.md)

# Jobs

**Pipeline entrypoints** that orchestrate logic from `src` and perform all I/O. 

- `jobs/` = execution & orchestration
- `src/` = library code

---

## Contract

Jobs are executable entrypoints that:
- handle runtime setup and configuration
- perform all external I/O
- delegate core logic to `src/`
- produce versioned outputs

Jobs define how the logic runs, not what the logic is.

---

## Layout

```
jobs/
  etl/
  train/
  track/
  serve/ # future
```

- **[ETL](./etl/README.md)** – batch ingestion, cleaning, and feature construction entrypoints
- **[Train](./train/README.md)** – model training and evaluation entrypoints
- **[Track](./track/README.md)** – experiment tracking and model registration entrypoints
- **Serve** – online inference and model serving entrypoints (future)