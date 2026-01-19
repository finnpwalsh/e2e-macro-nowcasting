# Roadmap
## Version Scopes
- **V0**: prototype ingestion and baseline modeling
- **V1**: production ML platform (infra, orchestration, serving)
- **V2** (planned): Applied regression + governed modeling lifecycle
- **V3** (planned): Production hardening (monitoring, reliability)
- **V4** (planned): Real-time nowcasting and performance scaling

---

## V1 Roadmap
**Theme**: infrastructure platform – MLOps

- **1.5.0**: FastAPI + ECS Fargate serving
- **1.6.0**: Terraform + CI/CD
- **1.7.0**: Model promotion Loop
- **1.8.0**: Ops hardening + Docs

---

## V2 Scope
**Theme**: Applied regression with governed model lifecycle

- SQL-first analytical layer (Postgres/Snowflake) producing reproducible, versioned feature and prediction tables
- Deterministic feature pipeline with explicit schemas, manifests, and training-serving parity checks
- Small, governed regression model set (OLS, Ridge, Elastic Net) with a unified interface
- Walk-forward evaluation with strict temporal split and explicit promotion rules
- Champion model selection integrated with the existing serving layer
- Diagnostics, visuals, and documentation for modeling analysis and ops context