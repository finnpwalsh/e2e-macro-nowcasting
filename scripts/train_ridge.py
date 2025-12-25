"""
Train baseline ridge model, generate run_id, and write model,
metrics, and predictions to artifacts/{run_id}.

RESPONSIBILITIES:
- generate a unique run id
- call train_ridge() to produce model, metrics, and preds
- save artifacts/{run_id}:
    - model to models/
    - metrics to metrics/
    - preds to predicions/
- write run metadata to artifacts/{run_id}/run.json
- confirm run successful

OUTPUTS:
- artifacts/{run_id}/run.json
- artifacts/{run_id}/models/baseline_ridge.joblib
- artifacts/{run_id}/metrics/baseline_ridge.json
- artifacts/{run_id}/predictions/baseline_ridge.parquet
"""

from __future__ import annotations

import json
import joblib

from src.config.run import generate_run_id
from src.pipelines.baseline import train_ridge
from src.runs.io import write_run_meta, write_run_artifacts

def main() -> None:
    # generate run id
    run_id = generate_run_id()

    # train
    model, metrics, preds = train_ridge()
    metrics["run_id"] = run_id

    # write run metadata
    write_run_meta(
        run_id=run_id,
        metrics=metrics,
        pipeline="baseline_ridge",
    )

    # write run artifacts
    write_run_artifacts(
        run_id=run_id,
        model=model,
        metrics=metrics,
        preds=preds,
        artifact_name="baseline_ridge",
    )

    print(f"Run: {run_id}")
    print(f"Baseline ridge RMSE: {metrics['rmse']:.4f}")


if __name__ == "__main__":
    main()