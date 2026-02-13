from __future__ import annotations

import pandas as pd

from .split import time_split_mask


class RegressionTrainer:
    """
    Model-agnostic regression trainer.
    """
    
    def __init__(
            self,
            *,
            model,
            scorer,
            target: str,
            split_date: str,
            date_col: str = "date",
    ):
        self.model = model
        self.scorer = scorer
        self.target = target
        self.split_date = split_date
        self.date_col = date_col
    
    def fit(self, df: pd.DataFrame):
        d = df.copy()
        d[self.date_col] = pd.to_datetime(d[self.date_col])
        d = d.sort_values(self.date_col)
        d = d.dropna(subset=self.target)

        feature_cols = [c for c in d.columns if c not in (self.date_col, self.target)]

        X = d[feature_cols]
        y = d[self.target]

        train_mask, valid_mask = time_split_mask(
            d,
            date_col=self.date_col,
            split_date=self.split_date,
        )

        self.model.fit(X[train_mask], y[train_mask])

        y_hat = self.model.predict(X[valid_mask])

        metrics = self.scorer(y[valid_mask], y_hat)

        metrics.update(
            {
                "split_date": self.split_date,
                "n_train": train_mask.sum(),
                "n_valid": valid_mask.sum(),
                "n_feats": len(feature_cols),
                "target": self.target,
                "features": feature_cols,
            }
        )

        preds = pd.DataFrame(
            {
                self.date_col: d.loc[valid_mask, self.date_col],
                "y": y[valid_mask],
                "y_hat": y_hat,
            }
        )

        return self.model, metrics, preds, feature_cols