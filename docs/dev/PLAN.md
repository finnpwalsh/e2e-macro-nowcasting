# Short-Term Plan

This document tracks short-term execution for the remaining V1 releases. It is intentionally tactical and may change as work progresses.

---

## Current focus – V1.4.1

### Documentation

- Update architecture, lifecycle, contracts, reproducibility, deployment, and operations documentation


### Tests refactor

- update modular `test/` calls with refactored `src/` directory naming, e.g. `src.config.baseline` -> `src.train.baseline.contracts`
- add missing unit/contract tests for refactored modules


### Containerized orchestration

- Update Docker requirements to install from `requirements/runtimes/*.txt`
- Build images (ETL / Train / Track / Serve)
- Smoke test each image by running its primary job locally
- Swap DAG tasks to container execution (DockerOperator locally, ECSOperator later)

---

## V1 version scopes

### v1.4.2 — Contracts & Scalability Foundations

- Define dataset and artifact contracts
- Move validation logic to source-owned modules
- Add train-time merged dataset validation

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