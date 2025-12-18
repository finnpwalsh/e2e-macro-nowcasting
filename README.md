# End-to-End Macro Nowcasting
## Overview
Real-time inflation nowcasting system built on a full MLOps stack. Serves as both an applied exploration of end-to-end pipeline development and a practical introduction to modern deployment and monitoring best practices.

## Status
**Dec 18, 2026**: Under active construction. 
### V1 Focus
**Goal:** An end-to-end inflation nowcasting pipeline that is reproducible and production-flavored.

**Specs**
- Reliable macro ingestion
- Data validation and contracts 
- Storage: raw → interim → processed
- Orchestration with apache Airflow
- Containerization with Docker

### Non-goals (V1)
Planned for later versions:
- Model optimization tuning
- Real-time serving or latency guarantees
- Cloud deployment
- Monitoring, drift detection, CI/CD

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
│   ├── interim/
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