from __future__ import annotations

import pandas as pd

from ml_platform.modeling._core import FeatureResolver, Trainer, TrainingWorkflow, TrainingResult
from ml_platform.modeling.engines import ENGINES

from .splitters import TimeSplitter
from .config import TimeSeriesTrainingConfig


def run_time_series_training(
    df: pd.DataFrame,
    config: TimeSeriesTrainingConfig,
) -> TrainingResult:
    splitter = TimeSplitter(
        time_col=config.time_col,
        split_date=config.split_date,
    )

    model_spec = ENGINES.get_spec(
        engine=config.spec.engine,
        model=config.spec.name,
    )

    trainer = Trainer(
        target_col=config.target_col,
        feature_resolver=FeatureResolver(),
        model_spec=model_spec,
        model_params=config.spec.params,
    )

    workflow = TrainingWorkflow(
        splitter=splitter,
        trainer=trainer,
    )

    return workflow.run(df=df)