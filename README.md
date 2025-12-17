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
**Dec 16, 2026**: Under active construction. V1 focus is reliable data ingestion &rarr validation &rarr storage with orchestration (Airflow) and containerization (Docker) coming next. 
**Goal**: An end-to-end inflation nowcasting pipeline that is reproducible and production-minded.

## Repo Structure
```
├── airflow
│   ├── dags
│   ├── logs
│   └── plugins
├── api
│   ├── deployment
│   └── openapi.yaml
├── data
│   ├── external
│   ├── interim
│   ├── processed
│   └── raw
├── deploy
│   ├── aws
│   └── k8s
├── docker-compose.yml
├── docs
│   ├── 00_overview.md
│   ├── 01_data_plan.md
│   ├── 02_architecture.md
│   ├── 03_model_plan.md
│   ├── 04_retraining_and_drift.md
│   ├── 05_api_dashboard.md
│   ├── 06_repo_structure.md
│   └── architecture_v1.png
├── infra
│   ├── github-actions
│   └── terraform
├── LICENSE
├── Makefile
├── mlflow
│   ├── artifacts
│   └── tracking
├── monitoring
│   ├── grafana
│   └── prometheus
├── notebooks
├── README.md
├── requirements.txt
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
└── tests
    ├── api
    ├── data
    └── pipeline
```