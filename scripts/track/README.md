# track/
Tracking scripts log and register **already-produced artifacts** into metadata systems (MLflow today). Tracking is **control-plane**: it should not retrain models and should not decide artifact schemas.

## `track/`
job entrypoints that:
  - read `run.json` (and referenced artifacts) from storage
  - call tracking backends in `src/track/track.py` (e.g., MLflow)
  - register/alias models as needed

---


## Implementation notes
- MLflow-specific logic lives in `src/track/mlflow.py` so scripts remain backend-agnostic.
- Tracking is best-effort; training artifacts are valid even if tracking fails.

---


## Example structure
```
track/
  track.py                # reads run.json + artifacts, calls src.track.mlflow
```
