from __future__ import annotations

from dataclasses import dataclass
import pandas as pd
from sklearn.pipeline import Pipeline

from macro_nowcast.train.trainer import Trainer


@dataclass(frozen=True)
class BaselineTrainer(Trainer):
    """
    Baseline trainer on monthly anchors (ds = MS).
    """
    model_name = "baseline"
    
    def fit(self, df: pd.DataFrame) -> Pipeline:
        X, y = self._split_xy(df)

        model = self.spec.make_pipeline()
        model.fit(X, y)

        return model
    
    def predict(self, *, model: Pipeline, df: pd.DataFrame) -> pd.Series:
        X, _ = self._split_xy(df)
        y_hat = model.predict(X)
        
        return pd.Series(
            y_hat,
            index=df.index,
            name=f"{self.target_col}_hat_baseline",
        )