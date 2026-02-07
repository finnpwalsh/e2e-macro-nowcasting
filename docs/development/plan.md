# V1 Plan

This document tracks short-term execution for the remaining V1 releases. It is intentionally tactical and may change as work progresses.

**Theme:** ML platform & infrastructure

---

## Version Philosophy

- Reproducibility over raw performance
- Explicit data, feature, and model contracts
- Infrastructure-first design before model complexity
- Clear ownership boundaries between pipeline stages

---

## Version Scope

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

---

## Current focus – V1.4.1

### Documentation
- Add reproducibility, deployment, and operations documentation

### Selection logic
- Decouple tracking and selection
    - Track -> log and register only
    - `jobs/select/promote.py`
    - Harden 

### Containerized orchestration
- Update Docker requirements to install from `requirements/runtimes/*.txt`
- Build images (ETL / Train / Track / Serve)
- Smoke test each image by running its primary job locally
- Swap DAG tasks to container execution (DockerOperator locally, ECSOperator later)

---

## Version Roadmap

### v1.4.2 — Contracts & Scalability Foundations
- Define dataset and artifact contracts
- Move validation logic to source-owned modules
- Add train-time merged dataset validation
- Add contract tests
- refactor data lakehouse

### v1.5.0 — Serving
- Implement FastAPI service for inference
- Deploy via ECS Fargate
- Load champion model via registry / pointer

### v1.6.0 — CI/CD
- Terraform infra modules
- Automated build and deploy pipeline
- Smoke tests post-deploy

### v1.7.0 – Promotion & rollback primitive
- Introduce a minimal, explicit mechanism to promote a trained model to "champion" and revert to a previous version, without policy or automation

### v1.8.0 – Ops hardening
- Establish baseline operational hygiene, including structured logging, health checks, and failure visibility to ensure the system can be run and debugged reliably