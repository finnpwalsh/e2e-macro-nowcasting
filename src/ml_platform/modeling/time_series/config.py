from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from ml_platform.runs import RunSpec


@dataclass(frozen=True)
class TimeSeriesTrainingConfig:
    time_col: str
    target_col: str
    split_date: pd.Timestamp
    spec: RunSpec
    primary_metric: str