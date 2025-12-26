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

OUTPUTS (Local):
- artifacts/{run_id}/run.json
- artifacts/{run_id}/models/baseline_ridge.joblib
- artifacts/{run_id}/metrics/baseline_ridge.json
- artifacts/{run_id}/predictions/baseline_ridge.parquet

OUTPUTS (MLflow):
- artifacts/mlflow/mlflow.db
- artifacts/mlflow/{run_id}/models/baseline_ridge.joblib
- artifacts/mlflow/{run_id}/metrics/baseline_ridge.json
- artifacts/mlflow/{run_id}/predictions/baseline_ridge.parquet

"""

from __future__ import annotations

import json
from pathlib import Path

from src.config.run import generate_run_id
from src.pipelines.baseline import train_ridge
from src.runs.io import write_run_meta, write_run_artifacts
from src.runs.tracking import setup_mlflow_local, log_run_to_mlflow

INPATH = Path("data/processed/merged.py")

def main() -> None:
    # generate run id
    run_id = generate_run_id()

    # train
    model, metrics, preds = train_ridge(infile=INPATH)
    metrics["run_id"] = run_id

    # write run metadata, return run path
    run_meta_path = write_run_meta(
        run_id=run_id,
        metrics=metrics,
        pipeline="baseline_ridge",
    )

    # write run artifactsm return artifact paths
    artifact_paths = write_run_artifacts(
        run_id=run_id,
        model=model,
        metrics=metrics,
        preds=preds,
        artifact_name="baseline_ridge",
    )

    # MLflow tracking index and UI
    setup_mlflow_local(experiment="baseline_ridge")
    mlflow_run_id = log_run_to_mlflow(
        run_name=run_id,
        run_id=run_id,
        pipeline="baseline_ridge",
        metrics=metrics,
        artifact_paths=artifact_paths,
    )

    # link mlflow run id into run.json
    run_meta = json.loads(run_meta_path.read_text())
    run_meta["mlflow_run_id"] = mlflow_run_id
    run_meta_path.write_text(json.dumps(run_meta, indent=2) + "\n")

    print(f"Run: {run_id}")
    print(f"MLflow run: {mlflow_run_id}")
    print(f"Baseline ridge RMSE: {metrics['rmse']:.4f}")


if __name__ == "__main__":
    main()