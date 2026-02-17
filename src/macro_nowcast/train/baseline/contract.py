from __future__ import annotations

from dataclasses import dataclass
import pandas as pd
from sklearn.pipeline import Pipeline


@dataclass(frozen=True)
class BaselineTrainOutputs:
    model: Pipeline
    predictions: pd.DataFrame
    residuals: pd.DataFrame