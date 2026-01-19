# runtimes/

Containerized execution environments for each stage of the ML lifecycle. Each runtime is built for a single phase and layered on top of a shared `base` image.

Runtimes are designed to:

- Stay lightweight via incremental dependencies
- Run the same way locally, in Airflow, and on ECS/Fargate
- Scale cleanly as new pipeline stages are added

---

## Layout

```
infra/docker/runtimes/
  base/
  etl/
  train/
  track/
  serve/
```

---

## Images
### `base`
**Role:** Shared foundation for all job runtimes

- Based on: `python:3.11-slim`
- Installs: `requirements/base.txt`
- Sets: `PYTHONPATH=/opt/project`
- Default CMD: `bash`

Used by all runtime stages.

---

### `etl`
**Role:** Data ingestion and preprocessing jobs

- Extends: `base`
- Installs: `requirements/runtimes/etl.txt`

---

### `train`
**Role:** Model training and evaluation jobs

- Extends: `base`
- Installs: `requirements/runtimes/train.txt`

---

### `track`
**Role:** Experiment tracking and model lifecycle runtime

- Parent: `base`
- Installs: `requirements/runtimes/track.txt`

---

### `serve`
**Purpose:** Online inference API runtime

- Parent: `base`
- Installs: `requirements/runtimes/serve.txt` 
- Exposes: `8000`
- Default CMD: `uvicorn src.serve.app:app ...`

---

## Mental Model

- **Runtimes** = execution environments for pipeline jobs
- **Services** = long-running infrastructure