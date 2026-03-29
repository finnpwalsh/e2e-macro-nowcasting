from __future__ import annotations

from dotenv import load_dotenv

from ml_platform.storage import Storage, get_storage

from ml_platform.runs import RunContext, RunPointer
from ml_platform.storage.persistence import JsonWrite

from ml_platform.modeling.regression import RegressionScorer
from ml_platform.modeling.time_series import run_time_series_training, TimeSeriesTrainingConfig, TimeSeriesEvaluator, TimeSeriesTrackingAdapter

from .cli import parse_args
from .config import TrainingRunConfig


def run(
    storage: Storage,
    run_config: TrainingRunConfig,
    training_config: TimeSeriesTrainingConfig,
) -> None:
    ctx = RunContext.create(run_family=run_config.run_family)

    # -----------------------------------------------------
    # Load dataset
    # -----------------------------------------------------
    
    df = storage.read_parquet(key=run_config.input_key)

    # -----------------------------------------------------
    # Train
    # -----------------------------------------------------

    training_result = run_time_series_training(
        df = df,
        config=training_config,
    )

    # -----------------------------------------------------
    # Evaluate
    # -----------------------------------------------------

    eval_result = TimeSeriesEvaluator(
        training_result=training_result,
        scorer=RegressionScorer(),
    ).evaluate(
        df=df,
        target_col=training_config.target_col,
        time_col=training_config.time_col,
    )

    # -----------------------------------------------------
    # Track run
    # -----------------------------------------------------
    
    tracking_result = TimeSeriesTrackingAdapter().track(
        ctx=ctx,
        df=df,
        input_key=run_config.input_key,
        config=training_config,
        result=eval_result,
        primary_metric_name=training_config.primary_metric,
    )

    # -----------------------------------------------------
    # Update latest pointer
    # -----------------------------------------------------

    pointer = RunPointer(
        run_identity=ctx.identity,
        manifest_key=ctx.keys.run.manifest,
        summary_key=ctx.keys.run.summary,
        primary_artifact_key=ctx.keys.models.model,
    )

    pointer_write = JsonWrite(
        key=ctx.keys.pointers.latest,
        payload=pointer,
    )

    plan = tracking_result.persistence_plan.extend([pointer_write])

    # -----------------------------------------------------
    # Persist
    # -----------------------------------------------------

    plan.persist(storage=storage)


def main() -> None:
    load_dotenv()
    run_config, training_config = parse_args()
    run(storage=get_storage(), run_config=run_config, training_config=training_config)


if __name__ == "__main__":
    main()