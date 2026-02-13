"""
Train job: baseline monthly model candidate generation.

Lifecycle stage:
    Train

Responsibilities:
    - Load the prepared training dataset
    - Fit the baseline model (ridge)
    - Produce versioned candidate artifacts required downstream

Inputs:
    - Model-ready training table from Prepare (storage key: DATASETS.model_ready_assemble)

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

from ml_platform.storage import Storage, get_storage, write_joblib, write_json
from ml_platform.artifacts import TrainArtifacts, EvalArtifacts, ModelPointers, new_run_id
from macro_nowcast.storage.datasets import DATASETS

from macro_nowcast.train.baseline.train import train_ridge


def run(storage: Storage) -> None:
    """Train the baseline model and persist versioned candidate artifacts for downstream storage."""
    run_id = new_run_id()
    model_name="baseline"

    tr = TrainArtifacts(model_name=model_name, run_id=run_id)
    ev = EvalArtifacts(model_name=model_name, run_id=run_id)
    ptr = ModelPointers(model_name=model_name)

    in_key = DATASETS.model_ready.assembled
    df = storage.read_parquet(key=in_key)

    model, metrics, preds, features = train_ridge(df)

    # train artifacts
    write_joblib(storage, key=tr.model, obj=model)
    write_json(storage, key=tr.metrics, obj=metrics)
    
    # eval artifacts
    storage.write_parquet(key=ev.predictions, df=preds)
    write_json(
        storage,
        key=ev.summary,
        payload={
            "model_name": model_name,
            "run_id": run_id,
            "input_key": in_key,
            "predictions_key": ev.predictions,
            "n_rows": len(preds),
            "n_cols": preds.shape[1],
            "columns": list(preds.columns),
            "n_features": len(features),
            "features": list(features),
        },
    )

    # latest pointer
    write_json(
        storage,
        key=ptr.latest,
        payload={
            "model_name": model_name,
            "run_id": run_id,
            "model_key": tr.model,
            "metrics_key": tr.metrics,
            "predictions_key": ev.predictions,
            "summary_key": ev.summary,
            "input_key": in_key,
        },
    )
    

    INDENT = "    "
    SUB = INDENT * 2
    print("\n[Train] Complete")
    print(f"{INDENT}Model:       {model_name}")
    print(f"{INDENT}Run ID:      {run_id}")
    print(f"{INDENT}Input:       {in_key}")
    print(f"{INDENT}Artifact store:")
    print(f"{SUB}model:       {tr.model}")
    print(f"{SUB}metrics:     {tr.metrics}")
    print(f"{SUB}preds:       {ev.predictions}")
    print(f"{SUB}summary:     {ev.summary}")
    print(f"{SUB}latest:      {ptr.latest}")


def main() -> None:
    load_dotenv()
    run(get_storage())


if __name__ == "__main__":
    main()