from __future__ import annotations

from dataclasses import dataclass

from ml_platform.storage import Storage

from .schema import Predictions, Residuals


@dataclass(frozen=True)
class PredictionsResolver:
    storage: Storage

    def resolve(
            self,
            *,
            key: str,
    ) -> Predictions:
        return Predictions(df=self.storage.read_parquet(key=key))


@dataclass(frozen=True)
class ResidualsResolver:
    storage: Storage

    def resolve(
            self,
            *,
            key: str,
    ) -> Residuals:
        return Residuals(self.storage.read_parquet(key=key))