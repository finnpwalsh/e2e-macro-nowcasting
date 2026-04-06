from __future__ import annotations

from dotenv import load_dotenv

from ml_platform.storage import Storage, get_storage, JsonWrite
from ml_platform.runs import RunContext, RunPointer

from ml_platform.modeling.engines import ENGINES
from ml_platform.modeling._core import (
    DefaultFeatureResolver,
    Trainer,
    TemporalSplitter,
)
from ml_platform.modeling.regression import RegressionScorer
from ml_platform.modeling.workflows import TrainingWorkflow
from ml_platform.modeling.tracking import TrainingRunTracker

from .cli import resolve_training_config
from .config import TrainingConfig


def run(
    storage: Storage,
    config: TrainingConfig,
) -> None:
    ctx = RunContext.create(run_family=config.run.run_family)

    # -----------------------------------------------------
    # load dataset
    # -----------------------------------------------------
    
    df = storage.read_parquet(key=config.run.input_key)

    # -----------------------------------------------------
    # splitter, model spec, trainer
    # -----------------------------------------------------

    splitter = TemporalSplitter(
        time_col=config.split.time_col,
        split_at=config.split.split_date,
    )

    model_spec = ENGINES.get_spec(
        engine=config.model.engine,
        model=config.model.name,
    )

    trainer = Trainer(
        target_col=config.run.target_col,
        feature_resolver=DefaultFeatureResolver(exclude_cols=[config.split.time_col]),
        model_spec=model_spec,
        model_params=config.model.params,
    )

    # -----------------------------------------------------
    # train + compute metrics
    # -----------------------------------------------------

    training_result = TrainingWorkflow(
        splitter=splitter,
        trainer=trainer,
    ).run(df=df)

    metrics = RegressionScorer().score(predictions=training_result.predictions)

    # -----------------------------------------------------
    # track run
    # -----------------------------------------------------

    tracking_result = TrainingRunTracker().track(
        ctx=ctx,
        df=df,
        input_key=config.run.input_key,
        model_definition=config.model,
        training_result=training_result,
        metrics=metrics,
    )

    # -----------------------------------------------------
    # update latest pointer
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
    # persist
    # -----------------------------------------------------

    plan.persist(storage=storage)


def main() -> None:
    load_dotenv()
    config = resolve_training_config()
    run(storage=get_storage(), config=config)


if __name__ == "__main__":
    main()