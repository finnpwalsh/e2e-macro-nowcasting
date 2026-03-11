← [Back to Docs](../README.md)

# Roadmap

Planned evolution.

---

## V1

Production ML platform

---

### v1.5.1 – Shocks corrector
- Train high-frequency shocks on baseline training residuals
- Produce nowcast inference

---

### v1.6.0 — Serving
- Implement FastAPI service for inference
- Deploy via ECS Fargate
- Load champion model via pointer

---

### v1.7.0 — CI/CD
- Automated build and deploy pipeline
- Smoke tests post-deploy

---

### v1.8.0 – Ops hardening
- Establish baseline operational hygiene, including structured logging, health checks, and failure visibility to ensure the system can be run and debugged reliably

---

## V2

Accuracy optimization

**Objective**: Improve out-of-sample nowcast accuracy and stability relative to the v1 baseline, without changing the deployment architecture.

Scope:
- Expand anchor and shock coverage to improve predictive signal
- Establish a standardized backtesting framework for consistent evaluation across time
- Ensure models only use information available at prediction time
- Train a small set of candidate models and promote the best-performing model via the standardized backtest protocol
- Introduce a two-stage correction approach where fast-moving signals adjust the baseline prediction

---

## V3

Production hardening

**Objective**: Ensure the system operates reliably in production and provides clear signals when behavior or data quality degrades.

Scope:
- Monitor data freshness, inputs, and prediction behavior
- Detect data and model drift
- Add health checks, structured logging, and failure signals
- Define alerting and operational runbooks
- Validate recovery and rollback paths under failure scenarios

---

## V4

Model governance and controlled iteration

**Objective**: Introduce formal governance

Scope:
- Define explicit model governance policies
- Introduce human-in-the-loop sign-off for model promotion decisions
- Formalize model change management
- Maintain. immutable audit trails for model decisions and promotions
- Define and enforce model-level quality standards tied to business objectives
- Separate "experimental" vs. "production" model classes with different governance rules