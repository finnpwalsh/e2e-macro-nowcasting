# jobs/

**Pipeline entrypoints** that orchestrate logic from `src` and perform all I/O. 

- `jobs/` = execution & orchestration
- `src/` = library code

---

## Contract

Jobs adhere to the following 6-step contract:

1. load environment / config
2. resolve input / output paths
3. read inputs from storage
4. call reusable logic from `src/`
5. write versioned artifacts back to storage
6. print a clear success message

---

## Layout

```
jobs/
  etl/
  train/
  track/
  serve/
```

---

## Job categories
### etl/
**Role:** Produce raw, processed, and model-ready datasets

- ingest external sources
- clean and validate data
- build features
- assemble training tables
- write datasets

---

### train/
**Role:** Produce canonical model artifacts and evaluation outputs

- fit models
- compute metrics
- write artifacts (models, predictions, summaries)

---

### track/
**Role:** log and register artifacts into metadata systems

- log metrics and artifacts
- register models
- update aliases / pointers

---

### serve/
**Role:** Run and validate the inference service

- start the API service
- perform smoke tests (`/health`, `/predict`)
- print active model pointer / version