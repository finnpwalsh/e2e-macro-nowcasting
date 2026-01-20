# V1.4.1 Plan

Near-term execution plans and task breakdown.

## Documentation

- Add thin README.md files for `docs/`

---

## Tests refactor

- update modular `test/` calls with refactored `src/` directory naming, e.g. `src.config.baseline` -> `src.train.baseline.contracts`
- add missing unit/contract tests for refactored modules

---

## Containerized orchestraction

- Update Docker requirements to install from `requirements/runtimes/*.txt`
- Build images (ETL / Train / Track / Serve)
- Smoke test each image by running its primary job locally
- Swap DAG tasks to container execution (DockerOperator locally, ECSOperator later)