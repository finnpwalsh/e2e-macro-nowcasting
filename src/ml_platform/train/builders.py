from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import pandas as pd

from ml_platform.train.metadata import (
    DataSignature,
    FeatureSignature,
    TrainingProvenance,
)


def _hash_frame(df: pd.DataFrame) -> str:
    hashed = pd.util.hash_pandas_object(df, index=True).to_numpy()
    return sha256(hashed.tobytes()).hexdigest()


@dataclass(frozen=True)
class DataSignatureBuilder:
    time_col: str
    target_col: str

    def build(
        self,
        *,
        df: pd.DataFrame,
        train_df: pd.DataFrame,
        valid_df: pd.DataFrame,
    ) -> DataSignature:
        base_cols = [self.time_col, self.target_col]

        return DataSignature(
            n_rows=len(df),
            n_train=len(train_df),
            n_valid=len(valid_df),
            columns=list(df.columns),
            dtypes={k: str(v) for k, v in df.dtypes.items()},
            time_min=str(df[self.time_col].min()),
            time_max=str(df[self.time_col].max()),
            row_fingerprint=_hash_frame(df[base_cols]),
        )


@dataclass(frozen=True)
class FeatureSignatureBuilder:
    def build(
        self,
        *,
        df: pd.DataFrame,
        feature_cols: list[str],
    ) -> FeatureSignature:
        feature_df = df[feature_cols].copy()

        return FeatureSignature(
            n_features=len(feature_cols),
            features=feature_cols,
            feature_dtypes={c: str(df[c].dtype) for c in feature_cols},
            null_counts=df[feature_cols].isna().sum().to_dict(),
            feature_fingerprint=_hash_frame(feature_df),
        )


@dataclass(frozen=True)
class TrainingProvenanceBuilder:
    generator_name: str
    trainer_name: str
    model_name: str
    time_col: str
    target_col: str
    split_date: str

    def build(self) -> TrainingProvenance:
        return TrainingProvenance(
            generator=self.generator_name,
            trainer=self.trainer_name,
            model_name=self.model_name,
            time_col=self.time_col,
            target_col=self.target_col,
            split_date=self.split_date,
        )