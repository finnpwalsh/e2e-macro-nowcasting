# src/

Reusable library code for the project.

`src/` contains pure logic that can be imported from:
- local scripts
- Docker containers
- Airflow tasks
- ECS services

No orchestration lives here.


---

## Rules

Code in `src/`:
- takes inputs and returns outputs
- is safe to import anywhere

Code in `src/` does not:
- read environment variables
- parse CLI arguments
- control execution flow
- print success messages

Those belong in `scripts/`.


---

## Structure

src/
  common/
  etl/
  train/
  track/


---

### common/
Shared utilities.

- evaluation/ — metrics
- storage/ — local + S3 helpers


### etl/
Data ingestion and transformation logic.

- anchors/ — low-frequency features
- shocks/ — high-frequency features
- assemble/ — dataset merging


### train/
Model training logic.

- baseline/ — baseline models and contracts


### track/
Experiment and artifact tracking helpers.

- mlflow/ — MLflow utilities


### serve/ (future)
Interface logic used by the FastAPI service.


---

## Testing

Tests mirror this structure under `tests/`.

---

## Summary

- `src/` = logic
- `scripts/` = execution
