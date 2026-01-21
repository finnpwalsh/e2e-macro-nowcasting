# Roadmap

Version history and planned evolution.

---

## Version Scopes

- **V0**: prototype ingestion and baseline modeling
- **V1**: production ML platform (infra, orchestration, serving)
- **V2** (planned): Accuracy optimization
- **V3** (planned): Production hardening (monitoring, reliability signals)
- **V4** (planned): Model governance and safe iteration

---

## V1 Roadmap

**Theme**: Infrastructure platform – MLOps

- **v1.4.2**: Contracts & scalability foundations
- **v1.5.0**: FastAPI + ECS Fargate serving
- **v1.6.0**: Terraform + CI/CD
- **v1.7.0**: Promotion & rollback primitive
- **v1.8.0**: Ops hardening

---

## V2 Scope

**Theme**: Accuracy optimization
**Objective**: Improve out-of-sample nowcast accuracy and stability relative to the v1 baseline, without changing infrastructure or deployment.

- Expand the set of anchor and shock indicators to improve predictive signal coverage
- Establish a standardized evaluation (backtesting) framework to measure forecasting performance consistently across time and versions
- Ensure models only use information that would have been available at the time of prediction, avoiding future data and revised values
- Train a small set of candidate models (3-4) and promote the best-performing model to champion using the standardized backtest protocol
- Add a two-stage correction approach where fast-moving signals adjust the baseline prediction

---

## V3 Scope

**Theme**: Production hardening
**Objective**: Ensure the nowcasting system operates reliably in production, degrades gracefully under failure, and provides clear signals when performance or data quality deteriorates.

- Add monitoring to track data freshness, model inputs, and prediction behavior over time
- Detect model and data drift to identify when accuracy is likely degrading
- Introduce health checks, structured logging, and clear failure signals across the pipeline
- Define alerting and runbook guidance for common operational issues
- Validate rollback and recovery paths to ensure safe operation during regressions or outages

---

## V4 Scope

**Theme**: Model governance and safe iteration
**Objective**: Enable continuous model improvement through controlled promotion, auditability, and rollback, without risking regressions in production behavior.
**Boundary**: V3 focuses on detecting when the system is unhealthy; V4 defines how model changes are evaluated, promoted, and rolled back safely.

- Introduce automated champion-challenger evaluation to govern when new models are eligible for promotion
- Add safe release mechanisms with explicit rollback paths
- Track full lineage from data inputs to model artifacts to support reproducibility and audits
- Define quality gates and service-level objectives to formalize what "acceptable model performance" means
- Standardize promotion and rollback workflows so model updates are routine, not risky events

---

## Version History
### V1
- **v1.4.1**: Lifecycle refactor
- **v1.4.0**: full S3-storage integration
- **v1.3.0**: yfinance integration
- **v1.2.0**: MLflow tracking
- **v1.1.0**: run identity, run-scoped artifacts
- **v1.0.1**: full documentation, docstrings, config refactor
- **v1.0.0**: reproducible macro data pipeline (Airflow + Docker)

### V0
- **v0.4.0**: baseline ridge training pipeline
- **v0.3.0**: model-ready FRED wide dataset
- **v0.2.0**: multi-series FRED ingestion
- **v0.1.0**: single-series FRED ingestion