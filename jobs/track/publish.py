from __future__ import annotations

from dotenv import load_dotenv

from ml_platform.storage.base import Storage
from ml_platform.storage.factory import get_storage
from ml_platform.storage import paths
from ml_platform.storage.io import read_joblib, read_json

from ml_platform.tracking.mlflow import log_and_register_model


def publish(storage: Storage) -> None:
    model_name = "baseline"

    k_latest = paths.model_latest(model_name)
    
    latest = read_json(storage, k_latest)
    
    model = read_joblib(storage, latest["model_key"])
    metrics = read_json(storage, latest["metrics_key"])
    preds = storage.read_parquet(latest["predictions_key"])
    summary = read_json(storage, latest["summary_key"])
    
    run_id = latest["run_id"]
    features = summary["features"]
    input_key = summary["input_key"]
    predictions_key = latest["predictions_key"]

    written = log_and_register_model(
        model_name=model_name,
        run_id=run_id,
        model=model,
        metrics=metrics,
        preds=preds,
        features=features,
        input_key=input_key,
        predictions_key=predictions_key,
        promote=True,
    )

    INDENT = "    "
    print()
    print("MLflow tracking complete")
    print(f"{INDENT}Model:           {model_name}")
    print(f"{INDENT}MLflow Run ID:   {written['mlflow_run_id']}")
    print(f"{INDENT}Experiment ID:   {written['experiment_id']}")
    print(f"{INDENT}Registry Name:   {written['registry_model_name']}")
    print(f"{INDENT}Version:         {written['registry_model_version']}")
    print(f"{INDENT}Alias:           {written['alias']}")
    print(f"{INDENT}Model URI:       {written['model_uri']}")
    print(f"{INDENT}Promoted:        {written['promoted']}")
    print(f"{INDENT}Predictions Key: {written['predictions_key']}")


def main() -> None:
    load_dotenv()
    storage = get_storage()
    publish(storage)


if __name__ == "__main__":
    main()