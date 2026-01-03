# Requirements Overview

This directory defines dependency boundaries by execution context. Each file is intentionally scoped to a specific runtime to keep images small, builds reproducible, and responsibilities clear.

## Files

### `base.txt`
Core dependencies shared across **training, evaluation, and serving**.

Used by:
- local training scripts
- batch jobs
- CI test environment (via `dev.txt`)
- FastAPI serving (via `serve.txt`)

Includes:
- data processing (`pandas`, `pyarrow`)
- modeling (`scikit-learn`, `joblib`)
- artifact tracking (`mlflow`)
- cloud access (`boto3`)

---

### `serve.txt`
Dependencies required to **serve models in production**.

Used by:
- FastAPI inference service
- ECS / Fargate runtime container

Includes:
- FastAPI
- Uvicorn
- all shared deps via `base.txt`

Does NOT include:
- pytest
- airflow
- orchestration or dev-only tools

---

### `dev.txt`
Dependencies for **local development and CI**.

Used by:
- GitHub Actions
- local testing

Includes:
- pytest
- all shared deps via `base.txt`

This file is never installed in production containers.

---

### `orchestrate.txt`
Dependencies for **workflow orchestration only**.

Used by:
- Airflow scheduler
- Airflow workers

Includes:
- apache-airflow (pinned)
- database drivers (e.g. psycopg2)

Airflow is intentionally isolated here to avoid polluting training or serving environments.

---

## Installation Matrix
| Context | Install Matrix |
| ------- | -------------- |
| Local dev/CI | `pip install -r requirements/dev.txt` |
| Training scripts | `pip install -r requirements/base.txt` |
| FastAPI serving | `pip install -r requirements/serve.txt` |
| Airflow runtime | `pip install -r requirements/orchestrate.txt` |

---

## Design Principles

- **Orchestration \neq execution**
Airflow is an orchestrator, not a runtime dependency.

- **Serving stays minimal**
No pytest, no airflow, no unused tooling.

- **CI mirrors execution, not production**
CI installs dev dependencies, production does not.

This separation supports clean separation between training, orchestration, serving, and testing.