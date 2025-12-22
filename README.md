# End-to-End Macro Nowcasting
## Overview
End-to-end inflation nowcasting system built with production-flavored MLOps pipeline.

## Status
**Dec 22, 2025**: Under active development. v1.0.0 is released.

### V1
**Goal:** A reproducible, production-style inflation nowcasting pipeline.

#### Specs
- Reliable macro ingestion
- Data validation and contracts 
- Storage: raw → processed
- Orchestration with Apache Airflow
- Containerization with Docker

#### Data (FRED)
**Target**
- CPI (CPIAUCSL): headline CPI price level

**Anchor Indicators**
- Energy Prices (CPIENGSL)
- Housing Prices (CPIHOSSL)
- Federal Funds Rate (FEDFUNDS)
- Unemployment Rate (UNRATE)

#### Non-goals
Planned for later versions:
- Model optimization tuning
- Real-time serving or latency guarantees
- Cloud deployment
- Monitoring, drift detection, CI/CD

#### Version History
- **v1.0.0** (current): reproducible macro data pipeline (Airflow + Docker)
- **v0.4.0**: baseline ridge pipeline implemented
- **v0.3.0**: model-ready FRED wide dataset
- **v0.2.0**: multi-series FRED ingestion
- **v0.1.0**: single-series FRED ingestion

## Quickstart
### Setup + Run
#### Prerequisites
- Docker + Docker Compose
- Make
- A FRED API key ([get one here](https://fred.stlouisfed.org/docs/api/api_key.html))

#### 1. Clone the repo
```
git clone https://github.com/<your-username>/e2e-macro-nowcasting.git
cd e2e-macro-nowcasting

```

#### 2. Set environment variables
Create a `.env` file in project root:
```
# FRED API
FRED_API_KEY=your_api_key_here

# Airflow Secret Key
AIRFLOW__WEBSERVER__SECRET_KEY=dev_secret_key
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
Access the Airflow UI at http://localhost:8080
**Login**: Username: admin | Password: admin

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
Use `make ingest`, `make clean`, and `make train` for local dev use + `make test` for data contract testing via pytest.


## Repo Structure
### V1 (Current)
```
├── airflow/
│   ├── dags/
│   └── logs/
├── artifacts/
│   └── models/         # saved models
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/          # exploratory analysis ONLY
├── scripts/            # program drivers
├── src/
│   ├── config/         # series lists and constants
│   ├── features/       
│   ├── ingestion/      
│   ├── models/         
│   ├── pipelines/      # end-to-end logic
│   ├── serving/        # API
│   └── validation/     # data checks
└── tests/
    └── data/
```

## Roadmap
### V2
- Intraday market shock sensors via yfinance
- Stronger baseline models(regularized regression, rolling backtests)
- Experiment tracking and model registry via MLflow
- FastAPI serving (minimal)

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