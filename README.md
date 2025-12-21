# End-to-End Macro Nowcasting
## Overview
End-to-end inflation nowcasting system built with production-flavored MLOps pipeline.

## Status
**Dec 21, 2025**: Under active development. FRED ingestion → cleaning → model-ready wide dataset completed (5 indicators). Pipeline is fully containerized and reproducible with Docker.

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
- **v0.3.0**: model-ready FRED wide dataset
- **v0.2.0**: multi-series FRED ingestion
- **v0.1.0**: single-series FRED ingestion

## Quickstart
1. Install Docker Desktop.
2. `make build` to create Docker image.
3. `make ingest` to ingest raw macro data.
4. `make test` to validate data contracts.
5. `make run` to run end-to-end pipeline.

## Repo Structure
### V1 (Current)
```
├── airflow/
│   └── dags/
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
- S3 Storage (AWS)
- Model tracking with MLFlow

### V3 or V4 (Planned)
```
├── airflow
│   └── dags
│   ├── logs
│   └── plugins
├── api
│   └── deployment
├── data
│   ├── external
│   ├── interim
│   ├── processed
│   └── raw
├── deploy
│   ├── aws
│   └── k8s
├── docs
├── infra
│   ├── github-actions
│   └── terraform
├── mlflow
│   ├── artifacts
│   └── tracking
├── monitoring
│   ├── grafana
│   └── prometheus
├── notebooks
├── scripts
├── src
│   ├── config
│   ├── evaluation
│   ├── feature_store
│   │   ├── entities
│   │   └── registry
│   ├── features
│   ├── ingestion
│   ├── models
│   ├── pipelines
│   ├── serving
│   └── validation
├── tests
│   ├── api
│   ├── data
│   └── pipeline
```