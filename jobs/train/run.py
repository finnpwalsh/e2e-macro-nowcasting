from __future__ import annotations

from dotenv import load_dotenv

from ml_platform.storage import Storage, get_storage
from macro_nowcast.storage.datasets import DATASETS

from ml_platform.runs.context import RunContext
from ml_platform.runs.tracker import RunTracker

from macro_nowcast.train.baseline import BaselineRunBuilder
from macro_nowcast.train.models import MODELS


def run(storage: Storage) -> None:
    ctx = RunContext(model_name="baseline")

    # -----------------------------------------------------
    # Load dataset
    # -----------------------------------------------------
    
    input_key = DATASETS.model_ready.anchors
    df = storage.read_parquet(key=input_key)

    # -----------------------------------------------------
    # Build candidate
    # -----------------------------------------------------

    builder = BaselineRunBuilder(
        model_name="baseline",
        time_col="ds",
        target_col="cpi_all_items",
        split_date="2020-01-01",
    )

    out = builder.run(df=df, spec=MODELS["ridge"].spec)

    # -----------------------------------------------------
    # Track run
    # -----------------------------------------------------

    tracker = RunTracker()

    result = tracker.track(
        ctx=ctx,
        input_key=input_key,
        split_date=builder.split_date,
        spec=out.spec,
        provenance=out.provenance,
        metrics=out.metrics,
        data_signature=out.data_signature,
        feature_signature=out.feature_signature,
        model_obj=out.model,
        predictions_df=out.predictions,
    )

    # -----------------------------------------------------
    # Persist
    # -----------------------------------------------------

    result.persistence_plan.persist(storage=storage)


def main() -> None:
    load_dotenv()
    run(get_storage())


if __name__ == "__main__":
    main()