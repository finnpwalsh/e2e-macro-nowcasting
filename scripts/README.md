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
    sources/
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

- **`etl/sources/`**: source-specific jobs (raw boundary + processed features)
  - Each source owns its own ingestion and processed feature artifacts.
  - Pattern:
    - `ingest.py` → writes raw source data
    - `build_wide.py` (or `build_<freq>_features.py`) → writes processed feature tables

- **`etl/assemble/`**: cross-source assembly / alignment jobs
  - Combines source-level processed artifacts into a **model-ready dataset** used by training.
  - In V1 this is typically a monthly dataset builder (may be a pure “merge” today).
  - In V2 this is where frequency alignment can live (monthly anchors + intraday sensors), while keeping training scripts stable.

**Example structure**
```
etl/
  sources/
    fred/
      ingest.py
      build_wide.py
    yfinance/
      ingest.py
      build_wide.py
  assemble/
    merge_monthly.py        # V1: build model-ready monthly dataset
```

---

#### train/
Training scripts produce **canonical model artifacts** and evaluation outputs. They should be **MLflow-free** (tracking is a separate step).

- **`train/baseline/`**: slow-moving anchor model training (monthly macro)
  - Implementation may change (ridge → elastic net → state space), but the *role* stays “baseline”.
  - Outputs: model file, metrics, predictions, `run.json` (and optionally residuals later)

- **`train/residual/` (V2+)**: fast residual/corrector model training (intraday sensors)
  - Trains a second model on baseline residuals (or deltas) using high-frequency features.

- **`train/evaluate/` (optional, V2+)**: model comparison/backtesting utilities
  - Walk-forward backtests, leaderboard generation, selection logic (if you decide to separate it from `train.py`).

**Example structure**
```
train/
  baseline/
    train.py
  residual/
    train.py
  evaluate/
    backtest.py
```

---

#### track/
Tracking scripts log and register **already-produced artifacts** into metadata systems (MLflow today). Tracking is **control-plane**: it should not retrain models and should not decide artifact schemas.

- **`track/`**: job entrypoints that:
  - read `run.json` (and referenced artifacts) from storage
  - call tracking backends in `src/track/*` (e.g., MLflow)
  - register/alias models as needed

**Implementation notes**
- MLflow-specific logic lives in `src/track/mlflow.py` so scripts remain backend-agnostic.
- Tracking is best-effort; training artifacts are valid even if tracking fails.

**Example structure**
```
track/
  track.py                # reads run.json + artifacts, calls src.track.mlflow
```

---

#### serve/
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