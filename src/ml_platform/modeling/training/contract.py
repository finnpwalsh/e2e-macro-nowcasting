from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from ..core.predictions import Predictions
from ..core.models import TrainedModel


@dataclass(frozen=True)
class TrainingResult:
    trained_model: TrainedModel
    train_df: pd.DataFrame
    valid_df: pd.DataFrame
    predictions: Predictions