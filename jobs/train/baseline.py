from __future__ import annotations

from dotenv import load_dotenv

from ml_platform.storage import Storage, get_storage, write_joblib, write_json
from macro_nowcast.storage.datasets import DATASETS
from ml_platform.runs.context import RunContext
from ml_platform.runs.tracker import RunTracker
from ml_platform.runs.write_plan import JsonWrite, JoblibWrite, ParquetWrite

from macro_nowcast.train.baseline import BaselineCandidateGenerator
from macro_nowcast.train.models import MODELS


def run(storage: Storage) -> None:
    ctx = RunContext(model_name="baseline")

    # -----------------------------------------------------
    # Load dataset
    # -----------------------------------------------------
    
    input_key = DATASETS.model_ready.anchors
    df = storage.read_parquet(key=input_key)

    # -----------------------------------------------------
    # Generate Candidate
    # -----------------------------------------------------

    gen = BaselineCandidateGenerator(
        model_name="baseline",
        time_col="ds",
        target_col="cpi_all_items",
        split_date="2020-01-01",
    )

    out = gen.generate(df=df, spec=MODELS["ridge"].spec)
    
    # -----------------------------------------------------
    # Write artifacts
    # -----------------------------------------------------

    write_joblib(storage, key=ctx.keys.artifacts.model, obj=out.model)
    storage.write_parquet(storage, key=ctx.keys.artifacts.predictions, df=out.predictions)

    # -----------------------------------------------------
    # Track run
    # -----------------------------------------------------

    tracker = RunTracker()

    result = tracker.track(
        ctx=ctx,
        input_key=input_key,
        split_date=gen.split_date,
        spec=out.spec,
        provenance=out.provenance,
        metrics=out.metrics,
        data_signature=out.data_signature,
        feature_signature=out.feature_signature,
        model_obj=out.model,
        predictions_df=out.predictions,
    )

    for write in result.write_plan.writes:
        if isinstance(write, JsonWrite):
            write_json(storage, key=write.key, payload=write.payload)
        elif isinstance(write, JoblibWrite):
            write_joblib(storage, key=write.key, obh=write.obj)
        elif isinstance(write, ParquetWrite):
            storage.write_parquet(key=write.key, df=write.df)


def main() -> None:
    load_dotenv()
    run(get_storage())


if __name__ == "__main__":
    main()