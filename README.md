# End-to-End Macro Nowcasting
## Overview
End-to-end inflation nowcasting system built with production-flavored MLOps pipeline.

## Status
**Dec 25, 2025**: Under active development

**v1.2.0** released — MLflow tracking

### Version Scopes
**V0**: prototype ingestion &rarr cleaning &rarr baseline training

**V1**: production-ready pipeline (infra, serving, cloud storage)

**V2** (planned): modeling improvements

**V3** (planned): production hardening (monitoring, CI/CD)

**V4** (planned): real-time nowcasting + performance/scale

### Version History
- **v1.2.0**: MLflow tracking
- **v1.1.0**: run identity, run-scoped artifacts
- **v1.0.1**: full documentation, docstrings, config refactor
- **v1.0.0**: reproducible macro data pipeline (Airflow + Docker)
- **v0.4.0**: baseline ridge training pipeline
- **v0.3.0**: model-ready FRED wide dataset
- **v0.2.0**: multi-series FRED ingestion
- **v0.1.0**: single-series FRED ingestion

### V1
**Goals:** A reproducible, production-style inflation nowcasting pipeline.

#### Scope
- Reliable macroeconomic and market data ingestion
- Data validation and schema contracts 
- Deterministic, s3-backed storage: raw → processed
- Run-scoped model artifacts with explicit run identity
- Mlflow tracking
- Pipeline orchestration with Apache Airflow
- Containerization with Docker
- Serving via FastAPI
- Full documentation

#### Data (FRED)
**Target**
- CPI (CPIAUCSL): headline CPI price level

**Anchor Indicators**
- Energy Prices (CPIENGSL)
- Housing Prices (CPIHOSSL)
- Federal Funds Rate (FEDFUNDS)
- Unemployment Rate (UNRATE)

#### Non-goals
Intentionally deferred to later versions:
- Model optimization tuning
- Real-time serving or latency guarantees
- Cloud deployment (compute / hosting)
- Monitoring, drift detection, CI/CD

## Quickstart
### Setup + Run
#### Prerequisites
- Docker + Docker Compose
- Make
- A FRED API key ([get one here](https://fred.stlouisfed.org/docs/api/api_key.html))

#### 1. Clone the repo
```
git clone https://github.com/finnpwalsh/e2e-macro-nowcasting.git
cd e2e-macro-nowcasting
```

#### 2. Set environment variables
Create a `.env` file in project root:
```
# FRED API
FRED_API_KEY=your_api_key_here

# Airflow Secret Key
AIRFLOW__WEBSERVER__SECRET_KEY=dev_secret_key

# suppress GitPython warnings for mlflow
GIT_PYTHON_REFRESH=quiet
```

#### 3. Build Docker image
```
make build
```

#### 4. Start Airflow
``` 
make up
```
This will:
- start Postgres
- initialize Airflow metadata database
- create an admin user
- launch the Airflow webserver and scheduler
Access the Airflow UI at: http://localhost:8080
**Login**: Username: `admin` | Password: `admin`

#### 5. Run pipeline
Trigger DAG `fred_pipeline` via:
```
make run
```

#### 6. Shut down
```
make down
```

#### Note: Local Dev
Use:
- `make ingest`
- `make clean`
- `make train`
- `make test` (data contract testing via pytest)


## Repo Structure
### V1 (Current)
```
├── airflow/
│   └── dags/           # DAG orchestration
├── scripts/            # program drivers
├── src/
│   ├── config/         # configuration and constants
│   ├── evaluation/     # model evaluation logic
│   ├── features/       # feature definitions / config
│   ├── ingestion/      # ingestion logic
│   ├── models/         # model implementations
│   ├── pipelines/      # end-to-end logic
│   ├── runs/           # run identity and artifact I/O
│   └── validation/     # data checks and contracts
└── tests/
```

## Roadmap
### V1
**Scope**: infra foundation


**1.3.0**: Daily market tickers via `yfinance`

**1.3.0**: FastAPI serving

**1.4.0**: S3-backed storage

### V2
**Scope**: Modeling

- Feature expansion (`FRED`, `yfinance`)
- Feature aggregation and lag structure
- Rolling and expanding-window backtests
- Stronger baseline models (ridge / elastic net)
- Model comparison and error diagnostics

### V3+ (Planned Architecture)
```
├── airflow/
│   └── dags/
│   ├── logs/
│   └── plugins/
├── api/
│   └── deployment/
├── data/
│   ├── external/
│   ├── interim/
│   ├── processed/
│   └── raw/
├── deploy/
│   ├── aws/
│   └── k8s/
├── docs/
├── infra/
│   ├── github-actions/
│   └── terraform/
├── mlflow/
│   ├── artifacts/
│   └── tracking/
├── monitoring/
│   ├── grafana/
│   └── prometheus/
├── notebooks/
├── scripts/
├── src/
│   ├── config/
│   ├── evaluation/
│   ├── feature_store/
│   │   ├── entities/
│   │   └── registry/
│   ├── features/
│   ├── ingestion/
│   ├── models/
│   ├── pipelines/
│   ├── serving/
│   └── validation/
├── tests
│   ├── api/
│   ├── data/
│   └── pipeline/
```