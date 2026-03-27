from __future__ import annotations

from dataclasses import dataclass, asdict
import pandas as pd

from .metadata import TrainingOutputs
from .builders import (
    DataSignatureBuilder,
    FeatureSignatureBuilder,
    TrainingProvenanceBuilder,
)
from ml_platform.artifacts.predictions import Predictions
from ml_platform.evaluation.schema import RegressionMetrics


@dataclass(frozen=True)
class TrainingOutputsAssembler:
    model_name: str
    time_col: str
    target_col: str
    split_date: str

    def assemble(
        self,
        *,
        df: pd.DataFrame,
        train_df: pd.DataFrame,
        valid_df: pd.DataFrame,
        trainer,
        model,
        predictions: Predictions,
        metrics: RegressionMetrics,
        feature_cols: list[str],
    ) -> TrainingOutputs:
        provenance = TrainingProvenanceBuilder(
            generator_name="TrainingOrchestrator",
            trainer_name=trainer.__class__.__name__,
            model_name=self.model_name,
            time_col=self.time_col,
            target_col=self.target_col,
            split_date=self.split_date,
        ).build()

        data_signature = DataSignatureBuilder(
            time_col=self.time_col,
            target_col=self.target_col,
        ).build(
            df=df,
            train_df=train_df,
            valid_df=valid_df,
        )

        feature_signature = FeatureSignatureBuilder().build(
            df=df,
            feature_cols=feature_cols,
        )

        return TrainingOutputs(
            spec=asdict(trainer.spec),
            provenance=provenance,
            model=model,
            metrics=asdict(metrics),
            predictions=predictions,
            data_signature=data_signature,
            feature_signature=feature_signature,
        )