from __future__ import annotations

from abc import ABC, abstractmethod
from hashlib import sha256
from typing import Generic, TypeVar

import pandas as pd

from .schema import DataSignature, FeatureSignature


SignatureT = TypeVar("SignatureT")


class SignatureBuilder(ABC, Generic[SignatureT]):
    @abstractmethod
    def build(self, **kwargs) -> SignatureT:
        raise NotImplementedError
    
    @staticmethod
    def _hash_frame(df: pd.DataFrame) -> str:
        hashed = pd.util.hash_pandas_object(df, index=False).to_numpy()
        return sha256(hashed.tobytes()).hexdigest()


class DataSignatureBuilder(SignatureBuilder[DataSignature]):
    def build(
        self,
        *,
        df: pd.DataFrame,
        train_df: pd.DataFrame | None = None,
        valid_df: pd.DataFrame | None = None,
    ) -> DataSignature:
        return DataSignature(
            n_rows=len(df),
            columns=list(df.columns),
            dtypes={k: str(v) for k, v in df.dtypes.items()},
            row_fingerprint=self._hash_frame(df),
            n_train=None if train_df is None else len(train_df),
            n_valid=None if valid_df is None else len(valid_df),
        )


class FeatureSignatureBuilder(SignatureBuilder[FeatureSignature]):
    def build(
            self,
            *,
            df: pd.DataFrame,
            feature_cols: list[str],
    ) -> FeatureSignature:
        feature_df = df[feature_cols].copy()

        return FeatureSignature(
            n_features=len(feature_cols),
            features=list(feature_cols),
            feature_dtypes={c: str(df[c].dtype) for c in feature_cols},
            feature_fingerprint=self._hash_frame(feature_df),
        )