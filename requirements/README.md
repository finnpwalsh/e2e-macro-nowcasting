# Requirements

Role-specific dependency files for each stage of the ML lifecycle.

Follows layered runtime image design:

- `base.txt` defines shared runtime dependencies
- Role-specific files (`etl`, `train`, `track`, `serve`) define only **incremental** dependencies
- Docker images install `base.txt` in the base image then layer role-specific deps on top

Objectives:

- Fast builds
- Clean separation of concerns
- Reproducible runtimes

---

## Folder Layout

```
requirements/
    base.txt
    
    runtimes/
        etl.txt
        train.txt
        track.txt
        serve.txt
        airflow.txt
    
    dev/
        dev.txt
        # optional later:
        # test.txt
        # lint.txt
        # cicd.txt
```

- `runtimes/`: ship/build images
- `dev`: local + CI tooling, never used in production images

---

## `base.txt`
Shared runtime dependencies for all job containers.

Installed in:

- `nowcasting-base` Docker image

Inherited by:
- ETL
- Train
- Track
- Serve

Examples:

- core Python libs
- numpy / pandas
- common IO, config, logging utils

---

## `runtimes/`

Layered runtime dependencies for building and shipping images. 

Notes:

- Files do NOT extend `base.txt`
- Base dependencies will be inherited from base Docker image
- contain only job-specific libraries

---

### `etl.txt`
Data ingestion and preprocessing dependencies.

Used by:

- ETL job containers
- Airflow tasks / ECS batch jobs

---

### `train.txt`
Model training and evaluation dependencies.

Used by:

- Training job containers

---

### `track.txt`
Experiment tracking and model lifecycle dependencies.

Used by:

- Tracking jobs
- Model-promotion scripts
- Evaluation logging

---

### `serve.txt`
Online inference dependencies.

Used by:

- FastAPI / inference service containers

---

### `airflow.txt`
Airflow scheduler and webserver dependencies only.

Used by:

- Airflow image

Notes:

- Does NOT extend base image
- Is intentionally isolated from ML/runtime dependencies
- Contains only Airflow-specific providers and operations

---

## `dev/`

Local development and CI utilities.

Notes:

- Not used to build production images
- May directly inherit `base.txt` dependencies

Optional future files (V2+):
- `test.txt`
- `lint.txt`
- `cicd.txt`

---

### `dev.txt`

Union of job dependencies for local development.

Inherits:

- `base.txt`
- `etl.txt`
- `train.txt`
- `track.txt`
- `serve.txt`