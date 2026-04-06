from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Sequence

import pandas as pd

from ml_platform.runs import RunArtifacts, RunContext
from ml_platform.signatures import DataSignatureBuilder, FeatureSignatureBuilder
from ml_platform.storage.persistence import JoblibWrite, ParquetWrite, WriteOp
from ml_platform.modeling._core import TrainingResult

from .schema import TrainingRunArtifacts


@dataclass(frozen=True)
class TrainingRunArtifactsBuilder:
    def build(
        self,
        *,
        ctx: RunContext,
        df: pd.DataFrame,
        training_result: TrainingResult,
    ) -> TrainingRunArtifacts:

        artifacts = RunArtifacts(
            primary=ctx.keys.models.model,
            extras={
                "predictions": ctx.keys.datasets.predictions,
            }
        )

        writes: Sequence[WriteOp] = [
            JoblibWrite(
                key=ctx.keys.models.model,
                obj=training_result.trained_model.model,
            ),
            ParquetWrite(
                key=ctx.keys.datasets.predictions,
                df=training_result.predictions.to_frame(),
            ),
        ]

        data_signature = DataSignatureBuilder().build(
            df=df,
            train_df=training_result.train_df,
            valid_df=training_result.valid_df,
        )

        feature_signature = FeatureSignatureBuilder().build(
            df=df,
            feature_cols=training_result.trained_model.feature_cols,
        )
    
        return TrainingRunArtifacts(
            artifacts=artifacts,
            writes=writes,
            data_signature=data_signature,
            feature_signature=feature_signature,
        )