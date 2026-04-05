from __future__ import annotations

from dotenv import load_dotenv

from ml_platform.storage import Storage, get_storage, JsonWrite
from ml_platform.runs import RunContext, RunPointer

from ml_platform.modeling.engines import ENGINES
from ml_platform.modeling._core import (
    DefaultFeatureResolver,
    PredictionsBuilder,
    Trainer,
    TrainingWorkflow,
    TrainingTrackingAdapter
)

from ml_platform.modeling.regression import RegressionScorer
from ml_platform.modeling.time_series import TimeSplitter

from .cli import resolve_training_config
from .config import TrainingConfig


def run(
    storage: Storage,
    config: TrainingConfig,
) -> None:
    ctx = RunContext.create(run_family=config.run.run_family)

    # -----------------------------------------------------
    # Load dataset
    # -----------------------------------------------------
    
    df = storage.read_parquet(key=config.run.input_key)

    # -----------------------------------------------------
    # Train
    # -----------------------------------------------------

    splitter = TimeSplitter(
        time_col=config.split.time_col,
        split_date=config.split.split_date,
    )

    model_spec = ENGINES.get_spec(
        engine=config.model.engine,
        model=config.model.name,
    )

    trainer = Trainer(
        target_col=config.run.target_col,
        feature_resolver=DefaultFeatureResolver(),
        model_spec=model_spec,
        model_params=config.model.params,
    )

    workflow = TrainingWorkflow(
        splitter=splitter,
        trainer=trainer,
    )

    training_result = workflow.run(df=df)

    # -----------------------------------------------------
    # Evaluate
    # -----------------------------------------------------

    predictions = PredictionsBuilder(
        target_col=config.run.target_col,
        row_id_col=config.run.row_id_col,
    ).build(df=training_result.valid_df, y_hat=training_result.y_hat)

    metrics = RegressionScorer().score(predictions=predictions)

    # -----------------------------------------------------
    # Track run
    # -----------------------------------------------------

    tracking_result = TrainingTrackingAdapter().track(
        ctx=ctx,
        df=df,
        input_key=config.run.input_key,
        model_definition=config.model,
        predictions=predictions,
        training_result=training_result,
        metrics=metrics,
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
    config = resolve_training_config()
    run(storage=get_storage(), config=config)


if __name__ == "__main__":
    main()