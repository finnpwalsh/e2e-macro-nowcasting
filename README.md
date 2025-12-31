# End-to-End Macro Nowcasting
## Overview
End-to-end inflation nowcasting system built as a production-grade ML platform emphasizing reproducibility and governed model lifecycle management.

This repository demonstrates how to design, version, evaluate and operate a macroeconomic ML system end-to-end, with explicit separation between infrastructure, modeling, and serving responsibilities. 

### Status
**Dec 31, 2025**: Under active development

**v1.4.0** released — full S3-backed storage integration


## Contents
- [V1 Overview](#v1-overview)
- [Quickstart](#quickstart)
- [Repo Structure](#repo-structure--v1-current)
- [Roadmap](#roadmap)
- [Version History](#version-history)


## V1 Overview
**Theme:** ML platform & infrastructure

### Version Philosophy
- Reproducibility over raw performance
- Explicit data, feature, and model contracts
- Infrastructure-first design before model complexity
- Clear ownership boundaries between pipeline stages

### Scope
- Reliable macroeconomic and market data ingestion 
- Deterministic, S3-backed storage: raw → processed
- Data validation and schema contracts
- Run-scoped model artifacts with explicit run identity
- Experiment tracking and artifact logging with MLflow
- Pipeline orchestration with Apache Airflow
- Containerization with Docker
- Model serving via FastAPI
- Cloud-native deployment (ECS Fargate, IaC via Terraform)
- Promotion and rollback mechanisms
- Production-oriented documentation (architecture, ops, contracts)

### Non-goals (V1)
Intentionally deferred to later versions:
- Model selection or hyperparameter optimization
- Online learning or real-time retraining
- Latency or throughput optimization

### Data – FRED
**Target**
- CPI (CPIAUCSL): headline CPI price level

**Anchor Indicators**
- Energy Prices (CPIENGSL)
- Housing Prices (CPIHOSSL)
- Federal Funds Rate (FEDFUNDS)
- Unemployment Rate (UNRATE)

### Data – yfinance
**Daily financial market tickers (end-of-month)**
- Equities risk (SPY)
- Volatility (^VIX)
- Rates Expectations (IEF)
- Energy Prices (CL=F)
- USD Strength (UUP)


## Quickstart
**Note**: Docker is the source of truth for runtime behavior. This runs the full pipeline locally using Airflow and S3-backed storage

**Prerequisites**
- Docker + Docker Compose
- Make
- A FRED API key ([get one here](https://fred.stlouisfed.org/docs/api/api_key.html))

### 1. Clone the repository
```
git clone https://github.com/finnpwalsh/e2e-macro-nowcasting.git
cd e2e-macro-nowcasting
```

### 2. Configure environment variables
Copy the example file and fill in required values:

```
cp .env.example .env
```

At minimum, set:
`FRED_API_KEY` • `AIRFLOW__WEBSERVER__SECRET_KEY` • `AWS_S3_BUCKET_DATA` • `AWS_S3_BUCKET_ARTIFACTS` • `AWS_S3_REGION` • `AWS_PROFILE`

### 3. Build Containers
```
make build
```

### 4. Start Airflow
``` 
make up
```

Access the Airflow UI at: http://localhost:8080
**Login**: Username: `admin` | Password: `admin`

Access the MLflow UI at: http://localhost:5000

### 5. Run the pipeline
```
make run
```

This executes the full pipeline end-to-end

### 6. Shut down
```
make down
```

### Optional: Run individual stages
These targets run individual pipeline stages inside containers without requiring a full DAG execution.

- `make ingest`
- `make clean`
- `make train`
- `make merge`
- `make test` (data contract testing via pytest)


## Repo Structure – V1 (Current)
```
├── airflow/
│   └── dags/           # DAG orchestration
├── docs/
├── infra/
│   ├── mlflow/         # mlflow tracking infra (service config)
│   └── terraform/      # IaC for cloud-native deployment
│       └── s3/
├── scripts/            # program drivers
├── src/
│   ├── config/         # configuration and constants
│   ├── evaluation/     # model evaluation logic
│   ├── features/       # feature definitions / config
│   ├── ingestion/      # ingestion logic
│   ├── materialization # write model artifacts to storage
│   ├── models/         # model implementations
│   ├── pipelines/      # end-to-end logic
│   ├── storage/        # Storage interface with local, S3 implementations
│   └── validation/     # data checks and contracts
└── tests/
```


## Roadmap
### Version Scopes
- **V0**: prototype ingestion and baseline modeling
- **V1**: production ML platform (infra, orchestration, serving)
- **V2** (planned): Applied regression + governed modeling lifecycle
- **V3** (planned): Production hardening (monitoring, reliability)
- **V4** (planned): Real-time nowcasting and performance scaling

### V1 Roadmap
**Theme**: infrastructure platform – MLOps

- **1.4.0**: S3-backed storage
- **1.5.0**: FastAPI + ECS Fargate serving
- **1.6.0**: Terraform + CI/CD
- **1.7.0**: Model promotion Loop
- **1.8.0**: Ops hardening + Docs

### V2 Scope
**Theme**: Applied regression with governed model lifecycle

- SQL-first analytical layer (Postgres/Snowflake) producing reproducible, versioned feature and prediction tables
- Deterministic feature pipeline with explicit schemas, manifests, and training-serving parity checks
- Small, governed regression model set (OLS, Ridge, Elastic Net) with a unified interface
- Walk-forward evaluation with strict temporal split and explicit promotion rules
- Champion model selection integrated with the existing serving layer
- Diagnostics, visuals, and documentation for modeling analysis and ops context

**Non-Goals (V2)**
- New infrastructure services
- Online learning or streaming ingestion
- Complex ensembles or deep learning models

### Version History
#### V1
- **v1.4.0**: full S3-storage integration
- **v1.3.0**: yfinance integration
- **v1.2.0**: MLflow tracking
- **v1.1.0**: run identity, run-scoped artifacts
- **v1.0.1**: full documentation, docstrings, config refactor
- **v1.0.0**: reproducible macro data pipeline (Airflow + Docker)

#### V0
- **v0.4.0**: baseline ridge training pipeline
- **v0.3.0**: model-ready FRED wide dataset
- **v0.2.0**: multi-series FRED ingestion
- **v0.1.0**: single-series FRED ingestion