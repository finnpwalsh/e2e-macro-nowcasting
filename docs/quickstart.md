← [Back to Docs](../README.md)

# Quickstart

This guide explains how to run the full pipeline locally using Docker, Airflow, and S3-backed storage.

The pipeline executes:
```
Prepare → Train → Track → Select
```

## 0. Prerequisites

Required: 
- Docker + Docker Compose
- Make
- FRED API key ([get one here](https://fred.stlouisfed.org/docs/api/api_key.html))
- Tiingo API token ([get one here](https://www.tiingo.com/account/api/token))
- AWS CLI installed
- AWS credentials configured locally (e.g., `aws configure`)
- Terraform installed

Docker is the source of truth for runtime behavior. All stages execute inside containers.

Containers rely on standard AWS credential resolution. If AWS is not configured, S3 read/writes will fail.

---

## 1. Clone Repository

```bash
git clone https://github.com/finnpwalsh/e2e-macro-nowcasting.git
cd e2e-macro-nowcasting
```

---

## 2. AWS + Terraform setup

This project uses AWS S3 for dataset and artifact storage. AWS resources are provisioned and managed via Terraform.

From the Terraform directory:
```bash
terraform init
terraform apply
```

---

## 3. Configure environment

Copy the example file:

```bash
cp .env.example .env
```

Populate required values:
- FRED_API_KEY
- TIINGO_API_KEY
- AIRFLOW__WEBSERVER__SECRET_KEY
    - Replace with a random string of 32+ characters
- AIRFLOW__CORE__FERNET_KEY
    - Replace with a random string of 32+ characters

---

4. Build Containers

```bash
make build
```

Builds all lifecycle runtime images.

---

5. Start Infrastructure

``` bash
make up
```

Services started:
- Airflow: http://localhost:8080
    - Login: admin / admin
- MLflow: http://localhost:5000

Storage is backed by the configured S3-compatible backend

---

6. Execute full pipeline

```bash
make run
```

Triggers the full DAG:
- Anchor ingestion
- Dataset assembly
- Baseline training
- Metric logging
- Model version registration
- Model selection

Artifacts and datasets are persisted to the configured storage backend.

---

## 7. Run individal stages

These commands execute the full lifecycle stages without running the full DAG:

```bash
make prepare
make train
make track
make select
make test
```

Useful for debugging and iteration

---

## 8. Shut down

```bash
make down
```

Stops containers. Persistent volumes are preserved unless explicitly removed.