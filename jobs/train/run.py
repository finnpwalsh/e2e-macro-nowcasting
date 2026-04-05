from __future__ import annotations

from dotenv import load_dotenv

from ml_platform.storage import Storage, get_storage, JsonWrite
from ml_platform.runs import RunContext, RunPointer

from ml_platform.modeling.engines import ENGINES
from ml_platform.modeling._core import (
    ModelDefinition,
    DefaultFeatureResolver,
    PredictionsBuilder,
    Trainer,
    TrainingWorkflow,
    TrainingTrackingAdapter
)

from ml_platform.modeling.regression import RegressionScorer
from ml_platform.modeling.time_series import TimeSplitter

from .cli import parse_args
from .config import TrainingRunConfig


def run(
    storage: Storage,
    run_config: TrainingRunConfig,
    model_definition: ModelDefinition,
) -> None:
    ctx = RunContext.create(run_family=run_config.run_family)

    # -----------------------------------------------------
    # Load dataset
    # -----------------------------------------------------
    
    df = storage.read_parquet(key=run_config.input_key)

    # -----------------------------------------------------
    # Train
    # -----------------------------------------------------

    splitter = TimeSplitter(
        time_col=run_config.row_id_col,
        split_date=run_config.extras["split_date"],
    )

    model_spec = ENGINES.get_spec(
        engine=model_definition.engine,
        model=model_definition.name,
    )

    trainer = Trainer(
        target_col=run_config.target_col,
        feature_resolver=DefaultFeatureResolver(),
        model_spec=model_spec,
        model_params=model_definition.params,
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
        target_col=run_config.target_col,
        row_id_col=run_config.row_id_col,
    ).build(df=training_result.valid_df, y_hat=training_result.y_hat)

    metrics = RegressionScorer().score(predictions=predictions)

    # -----------------------------------------------------
    # Track run
    # -----------------------------------------------------

    tracking_result = TrainingTrackingAdapter().track(
        ctx=ctx,
        df=df,
        input_key=run_config.input_key,
        model_definition=model_definition,
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
    run_config, model_definition = parse_args()
    run(storage=get_storage(), run_config=run_config, model_definition=model_definition)


if __name__ == "__main__":
    main()