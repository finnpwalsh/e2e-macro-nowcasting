"""
Train job: baseline monthly model candidate generation.

Lifecycle stage:
    Train

Responsibilities:
    - Load the prepared training dataset
    - Fit the baseline model (ridge)
    - Produce versioned candidate artifacts required downstream

Inputs:
    - Model-ready training table from Prepare (storage key: processed_merged)

Outputs (versioned by run_id):
    - Model artifact (joblib)
    - Metrics (json)
    - Evaluation predictions (parquet)
    - Run summary metadata
    - Latest pointer metadata (json) for downstream Track/Select/Serve

Out of scope:
    - Publishing to external tracking/registry systems
    - Model selection, promotion, or rollback
    - Online serving or inference APIs

Notes:
    This job writes all artifacts to persistent storage. Downstream stages read
    `model_latest(model_name)` / `run.json`-style metadata to locate the exact
    artifacts for a given run.
"""
from __future__ import annotations

from dotenv import load_dotenv

from ml_platform.storage.base import Storage
from ml_platform.storage.factory import get_storage
from ml_platform.storage import paths
from macro_nowcast.storage.datasets import DATASETS

from macro_nowcast.train.baseline.train import train_ridge

def train(storage: Storage) -> None:
    """Train the baseline model and persist versioned candidate artifacts for downstream storage."""
    run_id = paths.utc_run_id()
    model_name="baseline"

    k_merged = DATASETS.model_ready.assembled

    k_model = paths.model_file(model_name, run_id)
    k_metrics = paths.model_metrics(model_name, run_id)
    k_preds = paths.eval_predictions(model_name, run_id)
    k_summary = paths.eval_summary(model_name, run_id)
    k_latest = paths.model_latest(model_name)

    merged = storage.read_parquet(k_merged)

    model, metrics, preds, features = train_ridge(merged)

    storage.write_joblib(model, k_model)
    storage.write_json(metrics, k_metrics)
    storage.write_parquet(preds, k_preds)
    storage.write_json(
        {
            "model_name": model_name,
            "run_id": run_id,
            "input_key": k_merged,
            "predictions_key": k_preds,
            "n_rows": len(preds),
            "n_cols": preds.shape[1],
            "columns": list(preds.columns),
            "n_features": len(features),
            "features": list(features),
        },
        k_summary,
    ) # eval summary

    storage.write_json(
        {
            "model_name": model_name,
            "run_id": run_id,
            "model_key": k_model,
            "metrics_key": k_metrics,
            "predictions_key": k_preds,
            "summary_key": k_summary,
            "input_key": k_merged,
        },
        k_latest,
    ) # latest pointer
    
    INDENT = "    "
    print()
    print("Train complete")
    print(f"{INDENT}Model:       {model_name}")
    print(f"{INDENT}Run ID:       {run_id}")
    print(f"{INDENT}Input:       {k_merged}")
    print(f"{INDENT}RMSE:        {metrics['rmse']:.4f}")
    print()
    print("Outputs (data store)")
    print(f"{INDENT}model:       {k_model}")
    print(f"{INDENT}metrics:     {k_metrics}")
    print(f"{INDENT}preds:       {k_preds}")
    print(f"{INDENT}summary:     {k_summary}")
    print(f"{INDENT}latest:      {paths.model_latest(model_name)}")
    print()


def main() -> None:
    """Execute baseline training using configured storage."""
    load_dotenv()
    storage = get_storage()
    train(storage)


if __name__ == "__main__":
    main()