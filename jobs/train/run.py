from __future__ import annotations

from dotenv import load_dotenv

from ml_platform.storage import Storage, get_storage
from ml_platform.storage.persistence import JsonWrite, JoblibWrite, ParquetWrite

from ml_platform.runs import (
    TrackingOrchestrator,
    TrackingInput,
    RunContext,
    RunPointer,
    RunArtifacts,
)

from ml_platform.modeling.engines import ENGINES
from ml_platform.modeling._core import Trainer, TrainingWorkflow, FeatureResolver, PredictionsBuilder
from ml_platform.modeling.regression import RegressionScorer
from ml_platform.modeling.time_series import TimeSplitter, TimeSeriesTrainingConfig

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

    splitter = TimeSplitter(
        time_col=training_config.time_col,
        split_date=training_config.split_date,
    )

    model_spec = ENGINES.get_spec(
        engine=training_config.spec.engine,
        model=training_config.spec.name,
    )

    trainer = Trainer(
        target_col=training_config.target_col,
        feature_resolver=FeatureResolver(),
        model_spec=model_spec,
        model_params=training_config.spec.params,
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
        target_col=training_config.target_col,
        row_id_col=training_config.time_col,
    ).build(df=training_result.valid_df, y_hat=training_result.y_hat)

    metrics = RegressionScorer().score(predictions=predictions)

    # -----------------------------------------------------
    # Track run
    # -----------------------------------------------------
    
    artifacts = RunArtifacts(
        primary = ctx.keys.models.model,
        extras={
            "predictions": ctx.keys.datasets.predictions,
        }
    )

    artifact_writes = [
        JoblibWrite(
            key=ctx.keys.models.model,
            obj=training_result.trained_model.model,
        ),
        ParquetWrite(
            key=ctx.keys.datasets.predictions,
            df=predictions.to_frame(),
        ),
    ]

    tracking_input = TrackingInput(
        ctx=ctx,
        input_key=run_config.input_key,
        spec=training_config.spec,
        metrics = metrics,
        full_df = df,
        train_df=training_result.train_df,
        valid_df=training_result.valid_df,
        feature_cols=training_result.trained_model.feature_cols,
        artifacts=artifacts,
        artifact_writes=artifact_writes,
        run_config=training_config,
    )

    tracking_result = TrackingOrchestrator().run(
        tracking_input=tracking_input,
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