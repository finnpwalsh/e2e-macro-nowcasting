# scripts/

This directory contains **pipeline entrypoints (jobs)** that orchestrate logic from `src` and perform all I/O. 

Scripts are stateless executors that adhere to the following 6-step process:

1. "load environment/config"
2. "resolve input/output paths"
3. "read inputs from storage"
4. "call reusable logic from `src/`"
5. "write versioned artifacts back to storage"
6. "print a clear success message"

**Rule of thumb**
- `scripts/` = *orchestration / jobs* (side effects: read/write, print logs)
- `src/` = *library code* (pure-ish transforms, validation, feature building, models)

These scripts are designed to be run:
- locally (`python -m ...`)
- in Airflow (DockerOperator now, ECSOperator later)
- inside container images (ETL / Train / Track / Serve)

---

## Layout

This directory is architected with scalability in mind. We divide folders by their respective functions in the ML lifecycle:

**etl → train → track → serve**

```
scripts/
  etl/
    anchors/
    shocks/
    assemble/
  train/
    baseline/
    residual/        # V2+
    evaluate/        # optional (V2+)
  track/
  serve/
```

### Subfolder Scopes

#### etl/
ETL scripts are responsible for producing **raw** and **processed** datasets and assembling **model-ready** training tables.

#### train/
Training scripts produce **canonical model artifacts** and evaluation outputs. They should be **MLflow-free** (tracking is a separate step).

#### track/
Tracking scripts log and register **already-produced artifacts** into metadata systems (MLflow today). Tracking is **control-plane**: it should not retrain models and should not decide artifact schemas.

#### serve/ (V1.5.0)
Serving scripts are entrypoints/utilities for running the inference service.

- **`serve/`**: start the API service and any local dev helpers
  - The actual FastAPI app should live in `src/serve/...`
  - Scripts here can:
    - run the service locally
    - perform a smoke test (`/health`, `/predict`)
    - print the deployed version/model pointer

**Example structure**
```
serve/
  run_local.py            # optional: local runner for FastAPI
  smoke_test.py           # optional: simple request to /health and /predict
```

---

## Style guidelines

- Each script should have a top-level docstring with:
  - purpose
  - responsibilities
  - outputs (keys/paths)
- Keep scripts short; push logic into `src/`.
- Print a single `[OK] ...` line on success with shape + destination key.
- Do not import MLflow in training scripts; tracking owns MLflow dependencies.