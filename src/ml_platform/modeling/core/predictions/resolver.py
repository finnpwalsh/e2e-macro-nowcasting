from __future__ import annotations

from dataclasses import dataclass

from ml_platform.platform.storage import Storage

from .schema import Predictions


@dataclass(frozen=True)
class PredictionsResolver:
    storage: Storage

    def resolve(
            self,
            *,
            key: str,
    ) -> Predictions:
        return Predictions(df=self.storage.read_parquet(key=key))