# End-to-End Macro Nowcasting
## Overview
Real-time inflation nowcasting system built on a full MLOps stack. Serves as both an applied exploration of end-to-end pipeline development and a practical introduction to modern deployment and monitoring best practices.

### Contents
1.  [Overview](#overview)
2.  [Status](#status)
3.  [Quickstart](#quickstart)
4.  [Repo Structure](#repo-structure)
5.  [Roadmap](#roadmap)

## Status
**Dec 18, 2026**: Under active construction. V1 focus is reliable data ingestion &rarr validation &rarr storage with orchestration (Airflow) and containerization (Docker) coming next. 
**Goal**: An end-to-end inflation nowcasting pipeline that is reproducible and production-minded.

## Repo Structure
### V1
```
├── airflow/
│   └── dags/
├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
├── scripts/
├── src/
│   ├── config/
│   ├── features/
│   ├── ingestion/
│   ├── models/
│   ├── pipelines/
│   ├── serving/
│   └── validation/
└── tests
    └── data
```

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