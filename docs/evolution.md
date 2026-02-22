← [Back to Docs](../README.md)

# Evolution

Version history and planned evolution.

---

## Version Scopes

- **V0**: Prototype ingestion and baseline modeling
- **V1**: production ML platform (infra, orchestration, serving)
- **V2** (planned): Accuracy optimization
- **V3** (planned): Production hardening
- **V4** (planned): Model governance and controlled iteration

---

## V1 Roadmap

**Theme**: Infrastructure platform – MLOps

- **v1.5.0**: FastAPI + ECS Fargate serving
- **v1.6.0**: Terraform + CI/CD
- **v1.7.0**: Promotion & rollback primitive
- **v1.8.0**: Operations hardening

---

## V2 Scope

**Theme**: Accuracy optimization
**Objective**: Improve out-of-sample nowcast accuracy and stability relative to the v1 baseline, without changing the deployment architecture.

- Expand anchor and shock coverage to improve predictive signal
- Establish a standardized backtesting framework for consistent evaluation across time
- Ensure models only use information available at prediction time
- Train a small set of candidate models and promote the best-performing model via the standardized backtest protocol
- Introduce a two-stage correction approach where fast-moving signals adjust the baseline prediction

---

## V3 Scope

**Theme**: Production hardening
**Objective**: Ensure the system operates reliably in production and provides clear signals when behavior or data quality degrades.

- Monitor data freshness, inputs, and prediction behavior
- Detect data and model drift
- Add health checks, structured logging, and failure signals
- Define alerting and operational runbooks
- Validate recovery and rollback paths under failure scenarios

---

## V4 Scope

**Theme**: Model governance and controlled iteration
**Objective**: Introduce formal governance over 

V4 explicitly assumes that promotion, rollback, monitoring, and reliability already exist.

- Define explicit model governance policies
- Introduce human-in-the-loop sign-off for model promotion decisions
- Formalize model change management
- Maintain. immutable audit trails for model decisions and promotions
- Define and enforce model-level quality standards tied to business objectives
- Separate "experimental" vs. "production" model classes with different governance rules

---

## Version History
### V1
- **v1.4.1**: Lifecycle refactor
- **v1.4.0**: Full S3-backed storage integration
- **v1.3.0**: yfinance integration
- **v1.2.0**: MLflow tracking
- **v1.1.0**: run identity and run-scoped artifacts
- **v1.0.1**: Documentation and configuration refactor
- **v1.0.0**: Reproducible macro data pipeline (Airflow + Docker)

### V0
- **v0.4.0**: Baseline ridge training pipeline
- **v0.3.0**: Model-ready FRED wide dataset
- **v0.2.0**: Multi-series FRED ingestion
- **v0.1.0**: Single-series FRED ingestion