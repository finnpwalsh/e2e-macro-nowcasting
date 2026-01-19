from __future__ import annotations

from dotenv import load_dotenv

from src.track.mlflow.artifacts import log_and_register_model

from src.common.storage.base import Storage
from src.common.storage.paths import model_latest
from src.common.storage.factory import get_storage
from src.common.storage.io import read_joblib, read_json

def track_mlflow(storage: Storage) -> None:
    model_name = "baseline"

    # resolve I/O paths
    k_latest = model_latest(model_name)
    
    # read from storage
    latest = read_json(storage, k_latest)
    
    model = read_joblib(storage, latest["model_key"])
    metrics = read_json(storage, latest["metrics_key"])
    preds = storage.read_parquet(latest["predictions_key"])
    summary = read_json(storage, latest["summary_key"])
    
    # log via MLflow
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

    # confirm task ran successfully
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

    track_mlflow(storage)


if __name__ == "__main__":
    main()