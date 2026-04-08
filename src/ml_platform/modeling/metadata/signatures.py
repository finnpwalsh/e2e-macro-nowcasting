from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256

import pandas as pd


@dataclass(frozen=True)
class FeatureSignature:
    n_features: int
    features: list[str]
    feature_dtypes: dict[str, str]
    feature_fingerprint: str

    def to_dict(self) -> dict:
        return {
            "n_features": self.n_features,
            "features": self.features,
            "feature_dtypes": self.feature_dtypes,
            "feature_fingerprint": self.feature_fingerprint,
        }


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
            features=list(feature_cols),
            feature_dtypes={c: str(df[c].dtype) for c in feature_cols},
            feature_fingerprint=self._hash_frame(feature_df),
        )
    
    def _hash_frame(df: pd.DataFrame) -> str:
        hashed = pd.util.hash_pandas_object(df, index=False).to_numpy()
        return sha256(hashed.tobytes()).hexdigest()