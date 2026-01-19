# Activity Log

Doc for keeping track of development activity. Split by version + day.

--- 

## Template

For easy copy/paste logging:

### January XX, 2026

**CONTEXT**

- 

**NEXT**

- 

**DONE**

- 

---

## V1

Production-flavored infra hardening.

---

### January 19, 2026

**CONTEXT**

- Continued V1.4.1 cleanup and consolidation
- Repo-level clarity and presentation
- Goal: lock in final layout + documentation boundaries before moving forward

**NEXT**

- Add thin README.md files for `docs/`, `orchestration/`, `tests/`, and `src/` components `etl/`, `track/`, and `train/`
- Resume implementation work toward V1.5.0 (FastAPI serving + ECS/Fargate)

**DONE**

- Finalized root `README.md` as a lean platform entrypoint
- Locked in top-level repo layout (`docs / infra / jobs / orchestration / requirements / src / tests`)
- Improved documentation for `docs/`, `infra/docker`, `jobs/` 

---

### January 13, 2026

**CONTEXT**

- Continued v1.4.1 refactor with focus on infra and dependency hygiene
- Goal: lock down requirements + Docker convention before finishing images

**DONE**

- Finalized requirements folder structure (`base`, `runtimes`, `dev`)
- Finalized `infra/docker` folder structure (`runtimes`, `services`)
- Wrote + aligned `requirements/README.md` and `infra/docker/README.md`

---

### January 12, 2026

**CONTEXT**

- Resumed work after gap
    - Note that work from Dec 30 -> now has been ongoing but has not been logged. All work has been focused on v1.4.1 refactor.
- Focus: v1.4.1 refactor, infra + requirements + docker

**DONE**

- finalized requirements split (base + runtimes)
- standardized docker layout (infra/docker/*)
- clarified MLflow vs track responsibilities

**NEXT**

- finish Dockerfiles
- smoke test pipeline

---

### December 30, 2025

**NEXT**

- v1.5.0 – cloud-native serving

**DONE**

- configured MLflow to support remote (S3) artifact storagr
- create data and artifact S3 buckets via terraform
- S3-backed storage for data

---

### December 29, 2025

**NEXT**

- implement S3-backed storage

**DONE**

- Create Storage generic class
- implement Local Storage

---

### December 28, 2025

**NEXT**

- start 1.4.0 – S3-backed storage

**DONE**

- update Makefile, airflow DAG
- finalize docs
- tag + ship 1.3.0

---

### December 27, 2025

**NEXT**

- update airflow DAG
- update Makefile
- finalize docs
- tag v1.3.0

**DONE**

- merge
- update train
- update docs

---

### December 26, 2025

**NEXT**

- merge
- update train infile

**DONE**

- yf ingestion
- yf clean

---

### December 25, 2025

**NEXT**

- integrate yfinance

**DONE**

- refactored train_ridge into a clean driver script
- implemented run-scoped I/O (`src/runs/io.py`) for models, metrics, preds, and `run.json`
- added MLflow tracking layer (`src/runs/tracking.py`) for params, metrics, and artifacts
- integrated MLflow with Airflow/Docker (SQLite backend, local artifact store)
- ignored `mlruns/` noise
- tag v1.2.0

---

## December 24, 2025

**NEXT**

- mlflow

**DONE**

- full documentation
- docstrings
- config refactor
- push v1.0.1
- run identity
- run-scoped artifacts
- push v1.1.0

---

### December 23, 2025

**NEXT**

- docstrings for all necessary modules and functions

**DONE**

- split src/fred_clean functions to respective directories in features, validation, and pipelines
- add metrics-computing file to src/evaluation for scalability
- add docstrings to fred_clean functions

---

## V0

MVP end-to-end ML pipeline.

---

### December 22, 2025

**NEXT**

- begin v1 -> v2
- ingest yfinance

**DONE**

- add tests on baseline model
- v0.4.0 release
- add docker-compose for Airflow + PostgreSQL
- fred_pipeline_v1 DAG live + successful
- v1.0.0 release

---

### December 21, 2025

**NEXT**

- add tests on baseline model
- v0.4.0 tag/release

**DONE**

- wide-form, model-ready FRED dataset
- v0.3.0 tag/release
- make repo public
- add baseline model on FRED

---

### December 20, 2025

**NEXT**

- wide-form, model-ready FRED dataset

**DONE**

- raw -> clean stage for FRED series
- clean FRED data contract test
- refactor README

---

### December 18, 2025

**NEXT**

- raw → clean stage for FRED series

**DONE**

- ingest multiple FRED series
- store FRED series list in config
- incl. test for all global FRED series
- move raw FRED test to tests/data
- remove non-V1 directories + files
- v0.2.0 tag

---

### December 17, 2025

**NEXT**

- ingest multiple FRED series
- raw → clean stage for FRED series

**DONE**

- enforce FRED schema
- raw FRED data contract test (passed)
    - Takes multiple series
- added docstrings to ingest_fred, fred, raw FRED data test for clarity
- v0.1.0 tag

---

### December 16, 2025

**NEXT**

- enforce FRED schema
- data tests
- scale fred ingest to take multiple series

**DONE**

- finalize Dockerfile + Makefile
- move all workflow to Docker
- add smoke test to ensure pytest is functional
- ingestion writes parquet