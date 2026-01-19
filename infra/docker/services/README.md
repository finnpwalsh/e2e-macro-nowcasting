# services/

Long-running infrastructure services that support the ML pipeline. These images are shared across jobs and kept separate from runtimes to keep dependencies lightweight.

Services are typically:

- Started once (e.g. via `docker-compose` or ECS)
- Long-lived and stateful
- Used by multiple jobs

---

## Layout

```
infra/docker/services/
  airflow/
  mlflow/
```

---

## Images
### `airflow`
**Role:** Workflow orchestration (scheduler + webserver)

- Based on: `apache/airflow:<version>-python3.11`
- Installs: `requirements/runtimes/airflow.txt`
- Copies project source into the image (for DAGs and imports)

**Notes:**
- Acts as infra
- Does not install `requirements/base.txt` or ML job dependencies
- Orchestrates jobs but does not execute ML workloads itself

---

### `mlflow`
**Role:** Experiment tracking and model registry server

- Based on: `ghcr.io/mlflow/mlflow:<version>`
- Adds:
  - Postgres driver (backend store)
  - AWS SDK (S3 artifact store)
- Exposes: `5000`

Notes:
- Runs the MLflow **server**, not the client
- Client-side logging and model registration happen in the `track` runtime

---

## Mental Model

- **Services** = control plane (coordination, tracking, orchestration)
- **Runtimes** = execution plane (ETL, training, tracking jobs, serving)