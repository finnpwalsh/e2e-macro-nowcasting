from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from sklearn.pipeline import Pipeline

from .trainer import BaselineTrainer
from macro_nowcast.train import TimeSplitter
from macro_nowcast.train.models import ModelSpec
from macro_nowcast.eval.regression import regression_metrics


@dataclass(frozen=True)
class BaselineCandidateOutputs:
    model: Pipeline
    metrics: dict[str, float]
    predictions: pd.DataFrame
    summary: dict[str, ModelSpec]


@dataclass(frozen=True)
class BaselineCandidateGenerator:
    model_name: str
    time_col: str
    target_col: str
    split_date: str

    def generate(
            self,
            *,
            df: pd.DataFrame,
            spec: ModelSpec,
    ) -> BaselineCandidateOutputs:
        # 1) split
        splitter = TimeSplitter(time_col=self.time_col)
        train_mask, valid_mask = splitter.split_mask(df=df, split_date=self.split_date)

        train_df = df.loc[train_mask].copy()
        valid_df = df.loc[valid_mask].copy()

        if train_df.empty or valid_df.empty:
            raise ValueError(f"Empty split: train={len(train_df)}, valid={len(valid_df)}")
        
        # 2) fit + predict
        trainer = BaselineTrainer(spec=spec, target_col=self.target_col, time_col=self.time_col)
        model = trainer.fit(df=train_df)

        y_hat = trainer.predict(model=model, df=valid_df)

        # 3) eval table
        pred_df = valid_df[[self.time_col, self.target_col]].copy()
        pred_df["y_hat"] = y_hat

        # 4) metrics
        score_df = pred_df[[self.target_col, "y_hat"]].dropna(subset=[self.target_col, "y_hat"])
        metrics = regression_metrics(
            y=score_df[self.target_col],
            y_hat=score_df["y_hat"].to_numpy()
        )

        # 5) summary
        feature_cols = [c for c in df.columns if c not in {self.target_col}]

        summary = {
            "model_name": self.model_name,
            "split_date": self.split_date,
            "n_train": len(train_df),
            "n_valid": len(valid_df),
            "n_features": len(feature_cols),
            "features": feature_cols,
        }

        return BaselineCandidateOutputs(
            model=model,
            metrics=metrics,
            predictions=pred_df,
            summary=summary,
        )