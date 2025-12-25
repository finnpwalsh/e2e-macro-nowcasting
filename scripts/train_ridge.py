"""
Train baseline ridge model, generate run_id, and write model,
metrics, and predictions to artifacts/{run_id}.

RESPONSIBILITIES:
- generate run id
- call train_ridge
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
from src.pipelines.paths import get_paths

def main() -> None:
    # generate run id
    run_id = generate_run_id()

    # train
    model, metrics, preds = train_ridge()

    # add run_id to metrics
    metrics["run_id"] = run_id

    # get directories
    run_dir, model_dir, metrics_dir, preds_dir = get_paths(run_id)

    # make directories
    model_dir.mkdir(parents=True, exist_ok=True)
    metrics_dir.mkdir(parents=True, exist_ok=True)
    preds_dir.mkdir(parents=True, exist_ok=True)

    # write run metadata to run directory
    run_meta = {
        "run_id": run_id,
        "pipeline": "baseline_ridge",
        "target": metrics.get("target"),
        "split_date": metrics.get("split_date"),
        "alpha": metrics.get("alpha"),
    }
    (run_dir / "run.json").write_text(
        json.dumps(run_meta, indent=2) + "\n"
    )

    # save model
    joblib.dump(model, model_dir / "baseline_ridge.joblib")

    # save metrics
    (metrics_dir / "baseline_ridge.json").write_text(
        json.dumps(metrics, indent=2) + "\n"
    )

    # save preds (plotting + EDA)
    preds.to_parquet(preds_dir / "baseline_ridge.parquet", index=False)

    # output
    print(f"Run: {run_id}")
    print(f"Baseline ridge RMSE: {metrics['rmse']:.4f}")
    print("Saved:", model_dir / "baseline_ridge.joblib")
    print("Saved:", metrics_dir / "baseline_ridge.json")
    print("Saved:", preds_dir / "baseline_ridge.parquet")


if __name__ == "__main__":
    main()