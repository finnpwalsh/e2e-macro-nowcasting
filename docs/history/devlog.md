← [Back to Docs](../README.md)

# Activity Log

Doc for keeping track of development activity. Split by major version + day.

--- 

## Template

For easy copy/paste logging:

### April XX, 2026

**CONTEXT**

- v1.5.1 – shock corrector:

**DONE**

- 

**NEXT**

- 

---

## V1

Production-flavored infra hardening.

---

### April 7, 2026

**CONTEXT**

- v1.5.1 – shock corrector: `ml_platform` refactor

**DONE**

- `ml_platform` split
    - `modeling`
    - `platform` – reusable concepts
    - `services` – anything that coordinates multiple domains
- move `residuals` from `ml_platform` -> `macro_nowcast`
- make `runs` generic (not dependent upon `modeling`)

**NEXT**

- make storage, persistence generic
- update services

---

### April 6, 2026

**CONTEXT**

- v1.5.1 – shock corrector: `residuals`

**DONE**

- `modeling` audit
- created + validated:
    - `jobs/prepare/residuals`
    - `ml_platform/datasets/residuals`
- we now have the target ready to go for shock correction 

**NEXT**

- shock corrector feature engineering

---

### April 5, 2026

**CONTEXT**

- v1.5.1 – shock corrector: `select` audit

**DONE**

- create `configs`
- `jobs/select`: add CLI
- completed full run throughs of baseline `train`, `select`

---

**NEXT**

- `residuals`

---

### April 4, 2026

**CONTEXT**

- v1.5.1 – shock corrector: `promotion`

**DONE**

- mv `macro_nowcast/select` -> `ml_platform/promotion`
- made promotion domain-agnostic

**NEXT**

- update State Machines with new CLI
- decouple prepare from train/track/select (new state machine)
- training run with new CLI
- then finally add shock corrector logic

---

### March 30, 2026

**CONTEXT**

- v1.5.1 – shock corrector: `modeling` audit

**DONE**

- confirm `_core` generics
- slim `regression`, time_series
- add tracking workflow to generic _core
- finalize train CLI

**NEXT**

- confirm successful training run
- `residuals`
- `select` inside `ml_platform`

---

### March 29, 2026

**CONTEXT**

- v1.5.1 – shock corrector: `modeling` refactor

**DONE**

- consolidated evaluation, training into `modeling/_core`
- consolidated `regression` modeling extensions
- created `time_series` modeling extensions
- decoupled `engines` from `regression`
- created `engines` + `specs` nested registries for easy model spec querying
- added `cli` for training job

**NEXT**

- confirm full train runthrough
- residuals modeling
- select move to ml_platform?

---

### March 28, 2026

**CONTEXT**

- v1.5.1 – shock corrector: `runs` refactor

**DONE**

- created `ml_platform/signatures`
- made `runs` model-agnostic
- harden `runs` metadata contracts

**NEXT**

- `macro_nowcast/train` adapters for `ml_platform` generics
- move `macro_nowcast/select` generics to `ml_platform`

---

### March 27, 2026

**CONTEXT**

- v1.5.1 – shock corrector: train refactor

**DONE**

- `ml_platform/train/`
- `ml_platform/evaluation/`

**NEXT**

- deal with training metadata (currently stored in `ml_platform/_deprecated/`)

---

### March 23, 2026

**CONTEXT**

- v1.5.1 – shock corrector: `artifact` contract hardening

**DONE**

- created `predictions` and `residuals` artifacts

**NEXT**

- implement `residuals`

---

### March 10, 2026

**CONTEXT**

- v1.5.0 – execution + contract hardening: finalization

**DONE**

- bug fixes
- full successful Step Functions run!
- docs audit
- build+push all runtime images
- final StepFunctions test
- PR + tag/release v1.5.0

**NEXT**

- v1.5.1 – shock corrector

---

### March 9, 2026

**CONTEXT**

- v1.5.0 – execution + contract hardening: `select` orchestration

**DONE**

- `select` refactor
- terraform: add `network`, `orchestration`, `scheduler`

**NEXT**

- final `jobs` tests
- docs audit
- PR!!

---

### March 8, 2026

**CONTEXT**

- v1.5.0 – execution + contract hardening: training

**DONE**

- add `tracker`, `write_plan`
- update baseline run builder class + outputs
- update baseline train job accordingly

**NEXT**

- `select` refactor

---

### March 5, 2026

**CONTEXT**

- v1.5.0 – execution + contract hardening: tracking

**DONE**

- remove `Track`
- remove `mlflow`, `airflow`, `orchestration/`
- refactor storage keys, add runs directory

**NEXT**

- add `tracker`, `write_plan`, `selection` to `mlplatform/runs`
- fix dockerfile deps after `dependencies` rename

---

### March 4, 2026

**CONTEXT**

- v1.5.0 – execution + contract hardening: AWS via `terraform`

**DONE**

- init `tasks`, `compute`
- add `orchestration`, `scheduler`

**NEXT**

- remove `airflow`, `mlflow`
- remove `Track`
- refactor `Train`, `Select` (S3 + SSM)
- init `orchestration`, `scheduler`

---

### March 2, 2026

**CONTEXT**

- v1.5.0 – execution + contract hardening: AWS via `terraform`

**DONE**

- refactor terraform modules:
    `compute | config | network | runtimes | services | storage | tasks`

**NEXT**

- init `tasks`, `network`, `compute`, `services`

---

### February 27, 2026

**CONTEXT**

- v1.5.0 – execution + contract hardening: AWS via `terraform`

**DONE**

- refactor IAM stages to a single module with a stage map
- add ECR Repositories + tag Docker images
- add ECS
    - Execution Role, Security Groups, Cluster, Service (Fargate)
- add
    - CloudWatch logs, RDS Postgres, MLflow service

**NEXT**

- Airflow Webserver, Scheduler deployed on ECS

---

### February 26, 2026

**CONTEXT**

- v1.5.0 – execution + contract hardening: AWS via `terraform`

**DONE**

- wire IAM runtime policy

**NEXT**

- ECR module

---

### February 23, 2026

**CONTEXT**

- v1.5.0 – execution + contract hardening: AWS + `terraform`

**DONE**

- Created AWS organization + user + nowcasting-dev & nowcasting-prod users
- Refactored terraform-managed S3 buckets
- configured + implemented AWS SSM Parameter Store + Secrets Manager

**NEXT**

- wire IAM runtime policy

---

### February 22, 2026

**CONTEXT**

- v1.5.0 – execution + contract hardening: docs + Airflow DAG

**DONE**

- `docs/` audit

**NEXT**

- `DockerOperator`

---

### February 20, 2026

**CONTEXT**

- v1.5.0 – execution + contract hardening: `train` hardening

**DONE**

- `candidate` train generator
- finalize baseline `train` job
- finalize `track` + `select`

**NEXT**

- `DockerOperator` DAG

---

### February 16, 2026

**CONTEXT**

- v1.5.0 – execution + contract hardening: `train` hardening

**DONE**

- align `anchors` on month start
- align `shocks` on day

**NEXT**

- `train` refactor:
```
prepare → train baseline → compute residual → train corrector → combine → version → promote
```

---

### February 15, 2026

**CONTEXT**

- v1.5.0 – execution + contract hardening: `prepare` finalization

**DONE**

- remove `yfinance`, add `tiingo`
- finalize `shocks` prep jobs
- confirm all `prepare` jobs run
- rename version to operational baseline (more accurate)


**NEXT**

- `train` finalization: remove `assemble` step -> two-model system (`baseline` + `residuals`)

---

### February 14, 2026

**CONTEXT**

- v1.5.0 – execution + contract hardening: dev hardening

**DONE**

- refactor data lake (minor)
    - add source-specific directories inside domain-specific (anchor, shock) canon
- created `docker-compose.dev.yml` with stage-specific images
- added `nowcasting-base` image to `docker-compose.yml`
- updated `Makefile` accordingly
- added `registry` to `anchors`
- added `assembler`, `canonicalizer`, `feature_builder`, and `provider` interfaces to `interfaces` + implementations to `anchors`
- finalized `anchors` prep jobs:
    - `source/<source>.py`, `assemble.py`, `build_features.py`

**NEXT**

- remove `yfinance`, add `tiingo`
- remove `assemble` step -> two-model system (`baseline` + `residuals`)
- finalize `shocks` prep jobs

---

### February 13, 2026

**CONTEXT**

- v1.5.0 – execution + contract hardening: `Prepare` hardening

**DONE**

- add Source, Contract interfaces
- refactor `anchors`
- refactor `shocks`

**NEXT**

- refactor `assemble`
- refactor data lake (minor)
    - add source-specific directories inside domain-specific (anchor, shock) canon

---

### February 12, 2026

**CONTEXT**

- v1.5.0 – execution + contract hardening: storage refactor

**DONE**

- rename `price_nowcast` -> `macro_nowcast/`
- begin moving storage paths out of `ml_platform/` into `macro_nowcast/storage`
- divide `jobs/prepare/` jobs into `anchors/`, `shocks/`, and `assemble/` subdirectories
- Create `datasets.py` in macro_nowcast storage
    - `Datasets` (wrapper), `RawDatasets`, `CanonicalDatasets`, `ModelReadyDatasets`
- refactor `data` lakehouse into
    - `raw`, `canonical`, `model_ready`

**NEXT**

- split features + targets at canonicalization phase of prepare
    - add target canonicalize job + src code
- update assemble to pivot+merge+attach features + join target
- continue to refactor `ml_platform/storage/paths.py` into:

```
src/ml_platform/storage/
  ids.py              # run_id helpers
  layout.py           # ArtifactKey builders (models/eval/datasets)
  pointers.py         # latest.json, champion pointer semantics
```

- add/update relevant READMEs

---

### February 10, 2026

**CONTEXT**

- v1.5.0 – execution + contract hardening: Docker, requirements audit

**DONE**

- Docker refactor
    - added select.Docker
- `.env` audit
- `docker-compose.yml` audit
- NOTE: all services healthy

**NEXT**

- `DockerExecutor` -> run dag
- move `storage/paths.py` -> `price_nowcast`
- `Makefile` audit

---

### February 9, 2026

**CONTEXT**

- v1.5.0 – execution + contract hardening: Select

**DONE**

- decoupled Track and Select
- renamed `ml_platform/track` -> `ml_platform/mlflow`
- renamed `mlflow/mlflow.py` -> `mlflow/publish.py`
- created:
    - `mlflow/promote.py`
    - `jobs/select/promote.py`
    - `jobs/select/README.md`

**NEXT**

- `Track` audit

---

### February 7, 2026

**CONTEXT**

- v1.5.0 – execution + contract hardening: `jobs/` audit

**DONE**

- flatten `jobs/`
- conglomerate all `shocks/` and `anchors/` jobs into `prepare/shocks.py` and `prepare/anchors.py`
- update all jobs with new `src/` naming conventions
- `jobs/` docs + docstrings audit

**NEXT**

- add selection logic + job

---

### February 5, 2026

**CONTEXT**

- v1.5.0 – execution + contract hardening: `src/` audit

**DONE**

- created `ml_platform/` package
- moved `storage/` from `price_nowcast/common/` to `ml_platform/`
- `src/` docs audit
- rename `price_nowcast/etl/` -> `price_nowcast/prepare/`
- update `tests/test_smoke.py` imports with new package names

**NEXT**

- `jobs/` audit

---

### February 2, 2026

**CONTEXT**

- v1.5.0 – execution + contract hardening: hardening docs

**DONE**

- finalized `docs/lifecycle/`
- planned lifecycle relabel (`etl | train | track | serve` → `prepare | train | select | serve`)
- delayed `docs/contract.md` until v1.4.2
- moved quickstart from `README.md` to `docs/quickstart.md`

**NEXT**

- `docs/architecture/`
- `docs/getting_started/`
- `docs/evolution/`

---

### February 1, 2026

**CONTEXT**

- v1.5.0 – execution + contract hardening: hardening docs

**DONE**

- created `docs/contracts.md`
- added to contracts doc:
    - storage contract
    - dataset, artifact contract skeletons

**NEXT**

- finishg dataset, artifact contract documentation

---

### January 28, 2026

**CONTEXT**

- v1.5.0 – execution + contract hardening

**DONE**

- tests refactor
    - remove all current tests
    - add minimal smoke test
    - full tests refactor planned for later v1.4.x
- update docs
    - add lifecycle, architecture
    - move V1 info to plan

**NEXT**

- update old src names to reflect price_nowcast nesting
- add docs
    - contracts, reproducibility, deployment, operations

---

### January 21, 2026

**CONTEXT**

- Clarifying long-term system evolution in ROADMAP
- Introduced new documentation structure

**DONE**

- Finalized V0-V4 roadmap
- Defined V2 (accuracy), V3 (production hardening), V4 (governance)

**NEXT**

- Finish v1.4.1 execution

---

### January 20, 2026

**CONTEXT**

- Ongoing v1.4.1 refactor focused on architectural clarity and long-term scalability

**DONE**

- Added and refined READMEs for all applicable `src/` folders

**NEXT**

- Add and refine READMEs for:
    - `requirements/dev` and `requirements/runtimes`
- Ensure ALL READMEs have links to parent and child READMEs

---

### January 20, 2026

**CONTEXT**

- Ongoing v1.4.1 refactor focused on repo structure and documentation hygeine
- Goal: align project with clean ML system abstractions before moving into v1.5.0 (serving)

**DONE**

- Standardize README pattern across the repo
    - overview-contract-layout
    - links to parent and child READMEs
    - thin, contract-based, boundary-focused
- Added and refined READMEs for
    - `infra/` and all applicable subfolders
    - `requirements/`
    - `src/`
    - `jobs/`
    - `orchestration/`
- Finalized Terraform split: `storage/` vs `serving/`

**NEXT**

- Add and refine READMEs for:
    - `requirements/dev` and `requirements/runtimes`
    - All applicable `src/` subfolders
- Ensure ALL READMEs have links to parent and child READMEs

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