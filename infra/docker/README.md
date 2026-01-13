# Docker

Container images for each stage of the ML lifecycle and supporting infrastructure.

This folder follows a layered image design:

- `base` defines the shared, invariant runtime environment
- Role images (`etl`, `train`, `track`, `serve`) layer role-specific dependencies on top of `base`
- Infrastructure images (`airflow`, `mlflow`) provide always-on control-plane services

Objectives:

- Fast builds via layer caching
- Clear separation of concerns
- Reproducible runtimes across local Docker, Airflow, and ECS

---

## Folder Layout

```
infra/docker/
  runtimes/
    base/Dockerfile
    etl/Dockerfile
    train/Dockerfile
    track/Dockerfile
    serve/Dockerfile
  services/
    airflow/Dockerfile
    mlflow/Dockerfile
```

---

## Conceptual Axes (Important)

This directory uses two distinct classification axes:

1. **Dependency axis (requirements)**
   - Airflow is a *runtime image* in dependency terms (it builds a Docker image with pinned deps)
2. **Operational axis (Docker)**
   - Airflow is an *infrastructure service* (always-on scheduler/control plane)

This is intentional and avoids overloading a single folder name with multiple meanings.

---

## Image Overview

### `base`
**Purpose:** shared runtime base image for all project job containers.

- Upstream: `python:3.11-slim`
- Installs: `requirements/base.txt`
- Sets: `PYTHONPATH=/opt/project`
- Default CMD: `bash`

Used as the parent image for:
- `etl`
- `train`
- `track`
- `serve`

---

### `etl`
**Purpose:** ETL job runtime (ingestion + preprocessing).

- Parent: `base`
- Installs: `requirements/runtimes/etl.txt` (incremental deps only)
- Copies project source into the image

Intended use:
- Local job runs via `docker run`
- Airflow `DockerOperator` tasks
- ECS batch jobs

---

### `train`
**Purpose:** model training and evaluation runtime.

- Parent: `base`
- Installs: `requirements/runtimes/train.txt` (incremental deps only)
- Copies project source into the image

Intended use:
- Local training runs
- Airflow / ECS training jobs

---

### `track`
**Purpose:** experiment tracking and model lifecycle runtime.

- Parent: `base`
- Installs: `requirements/runtimes/track.txt` (incremental deps only)
- Copies project source into the image

Examples:
- Logging metrics and artifacts to MLflow
- Running model-promotion scripts

---

### `serve`
**Purpose:** online inference service.

- Parent: `base`
- Installs: `requirements/runtimes/serve.txt` (incremental deps only)
- Copies project source into the image
- Exposes: `8000`
- Default CMD: `uvicorn src.serve.app:app ...`

Intended use:
- Local API serving
- ECS/Fargate service behind an ALB

---

### `airflow`
**Purpose:** Airflow scheduler and webserver image.

- Upstream: `apache/airflow:<version>-python3.11`
- Installs: `requirements/runtimes/airflow.txt`
- Copies project source into the image (for DAGs and imports)

Notes:
- Airflow is a runtime image in *dependency* terms, but an infrastructure service operationally.
- It intentionally does **not** install `requirements/base.txt` or ML job dependencies.

---

### `mlflow`
**Purpose:** MLflow tracking server image.

- Upstream: `ghcr.io/mlflow/mlflow:<version>`
- Installs:
  - Postgres driver (backend store)
  - AWS SDK (S3 artifact store)
- Exposes: `5000`

Notes:
- Hosts the MLflow **server** (not the client).
- MLflow client dependencies live in the `track` image.

---

## Build Contract

Docker is the source of truth for runtime behavior.

### Requirements coupling
- `base` installs `requirements/base.txt`
- `etl/train/track/serve` install only their respective `requirements/runtimes/*.txt`
- `airflow` installs only `requirements/runtimes/airflow.txt`
- `mlflow` extends its upstream image with minimal drivers only

### Rules
- Production images **must not** install `requirements/dev/*`
- `requirements/runtimes/*.txt` **must not** include `-r ../base.txt`

---

## Common Build Commands

```
# base
docker build -t nowcasting-base:latest -f infra/docker/base/Dockerfile .

# job runtimes
docker build -t nowcasting-etl:latest   --build-arg BASE_IMAGE=nowcasting-base:latest -f infra/docker/etl/Dockerfile .
docker build -t nowcasting-train:latest --build-arg BASE_IMAGE=nowcasting-base:latest -f infra/docker/train/Dockerfile .
docker build -t nowcasting-track:latest --build-arg BASE_IMAGE=nowcasting-base:latest -f infra/docker/track/Dockerfile .
docker build -t nowcasting-serve:latest --build-arg BASE_IMAGE=nowcasting-base:latest -f infra/docker/serve/Dockerfile .

# infra services
docker build -t nowcasting-airflow:latest -f infra/docker/airflow/Dockerfile .
docker build -t nowcasting-mlflow:latest  -f infra/docker/mlflow/Dockerfile .
```

---

## Runtime Expectations

- **ETL / Train / Track** images are batch-style job runners (invoked with `python -m ...`).
- **Serve** is a long-running API process.
- **Airflow** and **MLflow** are always-on infrastructure services.