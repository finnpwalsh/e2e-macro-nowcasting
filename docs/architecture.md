# Architecture
## V1 Overview
**Theme:** ML platform & infrastructure

### Version Philosophy
- Reproducibility over raw performance
- Explicit data, feature, and model contracts
- Infrastructure-first design before model complexity
- Clear ownership boundaries between pipeline stages

### Scope
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

### Non-goals (V1)
Intentionally deferred to later versions:
- Model selection or hyperparameter optimization
- Online learning or real-time retraining
- Latency or throughput optimization