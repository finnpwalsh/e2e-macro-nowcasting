from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from ml_platform.runs import RunSpec
from ml_platform.modeling._core import TrainingResult
from ml_platform.modeling.regression import Predictions, RegressionMetrics


@dataclass(frozen=True)
class TimeSeriesTrainingConfig:
    time_col: str
    target_col: str
    split_date: pd.Timestamp
    spec: RunSpec
    primary_metric: str


@dataclass(frozen=True)
class TimeSeriesEvalResult:
    training_result: TrainingResult
    predictions: Predictions
    metrics: RegressionMetrics