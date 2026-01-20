# jobs/

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