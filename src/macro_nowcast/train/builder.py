from __future__ import annotations

from dataclasses import dataclass, asdict
from hashlib import sha256
from typing import Any

import pandas as pd
from sklearn.pipeline import Pipeline

from ml_platform.artifacts.predictions import Predictions, PredictionsBuilder

from .trainer import Trainer
from .splitter import TimeSplitter
from macro_nowcast.train.models import ModelSpec
from macro_nowcast.eval.regression import regression_metrics


@dataclass(frozen=True)
class TrainingOutputs:
    spec: dict[str, Any]
    provenance: dict[str, Any]
    model: Pipeline
    metrics: dict[str, float]
    predictions: Predictions
    data_signature: dict[str, Any]
    feature_signature: dict[str, Any]


@dataclass(frozen=True)
class TrainingBuilder:
    model_name: str
    time_col: str
    target_col: str
    split_date: str

    def run(
            self,
            *,
            df: pd.DataFrame,
            spec: ModelSpec,
    ) -> TrainingOutputs:
        # ---------------------------------------------------------------
        # Split
        # ---------------------------------------------------------------

        splitter = TimeSplitter(time_col=self.time_col)
        train_mask, valid_mask = splitter.split_mask(df=df, split_date=self.split_date)

        train_df = df.loc[train_mask].copy()
        valid_df = df.loc[valid_mask].copy()

        if train_df.empty or valid_df.empty:
            raise ValueError(f"Empty split: train={len(train_df)}, valid={len(valid_df)}")
        
        # ---------------------------------------------------------------
        # Define features
        # ---------------------------------------------------------------

        feature_cols = [c for c in df.columns if c not in {self.target_col, self.time_col}]

        # ---------------------------------------------------------------
        # Fit + predict
        # ---------------------------------------------------------------
        
        trainer = Trainer(
            spec=spec,
            target_col=self.target_col,
            time_col=self.time_col
        )

        model = trainer.fit(df=train_df)
        y_hat = trainer.predict(model=model, df=valid_df)

        # ---------------------------------------------------------------
        # Predictions
        # ---------------------------------------------------------------

        predictions = PredictionsBuilder(
            time_col=self.time_col,
            target_col=self.target_col,
        ).build(
            df=valid_df,
            y_hat=y_hat,
        )

        pred_df = predictions.df

        # ---------------------------------------------------------------
        # Metrics
        # ---------------------------------------------------------------

        score_df = pred_df[[self.target_col, "y_hat"]].dropna(subset=[self.target_col, "y_hat"])
        metrics = regression_metrics(
            y=score_df[self.target_col],
            y_hat=score_df["y_hat"].to_numpy()
        )

        # ---------------------------------------------------------------
        # Spec
        # ---------------------------------------------------------------
        spec_payload = asdict(spec)

        # ---------------------------------------------------------------
        # Provenance
        # ---------------------------------------------------------------
        provenance = {
            "generator": self.__class__.__name__,
            "trainer": trainer.__class__.__name__,
            "model_name": self.model_name,
            "time_col": self.time_col,
            "target_col": self.target_col,
            "split_date": self.split_date,
        }
        
        # ---------------------------------------------------------------
        # Data signature
        # ---------------------------------------------------------------

        data_signature = self._build_data_signature(
            df=df,
            train_df=train_df,
            valid_df=valid_df,
        )

        # ---------------------------------------------------------------
        # Feature signature
        # ---------------------------------------------------------------
        feature_signature = self._build_feature_signature(
            df=df,
            feature_cols=feature_cols,
        )

        return TrainingOutputs(
            spec=spec_payload,
            provenance=provenance,
            metrics=metrics,
            data_signature=data_signature,
            feature_signature=feature_signature,
            model=model,
            predictions=pred_df,
        )
    
    def _build_data_signature(
        self,
        *,
        df: pd.DataFrame,
        train_df: pd.DataFrame,
        valid_df: pd.DataFrame,
    ) -> dict[str, Any]:
        base_cols = [self.time_col, self.target_col]
        min_ds = df[self.time_col].min()
        max_ds = df[self.time_col].max()

        row_fingerprint = self._hash_frame(df[base_cols])

        return {
            "n_rows": len(df),
            "n_train": len(train_df),
            "n_valid": len(valid_df),
            "columns": list(df.columns),
            "dtypes": {k: str(v) for k,v in df.dtypes.items()},
            "time_min": str(min_ds),
            "time_max": str(max_ds),
            "row_fingerprint": row_fingerprint,
        }

    def _build_feature_signature(
        self,
        *,
        df: pd.DataFrame,
        feature_cols: list[str],
    ) -> dict[str, Any]:
        feature_df = df[feature_cols].copy()

        return {
            "n_features": len(feature_cols),
            "features": feature_cols,
            "feature_dtypes": {c: str(df[c].dtype) for c in feature_cols},
            "null_counts": df[feature_cols].isna().sum().to_dict(),
            "feature_fingerprint": self._hash_frame(feature_df),
        }
    
    @staticmethod
    def _hash_frame(df: pd.DataFrame) -> str:
        hashed = pd.util.hash_pandas_object(df, index=True).to_numpy()
        return sha256(hashed.tobytes()).hexdigest()