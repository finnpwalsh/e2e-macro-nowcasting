"""
Train baseline ridge model and write canonical artifacts.

RESPONSIBILITIES:
- generate a unique run id (UTC)
- read model-ready dataset from storage
- train baseline ridge model
- write model artifacts and eval (canonical)

OUTPUTS:
- artifacts/models/baseline_ridge/<run_id>/model.joblib
- artifacts/models/basline_ridge/<run_id>/metrics.json
- artifacts/models/basline_ridge/latest.json
- artifacts/eval/baseline_ridge/<run_id>/predictions.parquet
- artifacts/eval/baseline_ridge/<run_id>/summary.json
"""

from __future__ import annotations

import json
from pathlib import Path

from dotenv import load_dotenv

from src.config.run import generate_run_id
from src.pipelines.baseline import train_ridge
from src.runs.io import write_run_meta, write_run_artifacts
from src.runs.tracking import setup_mlflow_local, log_run_to_mlflow

INPATH = Path("data/processed/merged.parquet")

def main() -> None:
    load_dotenv()
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