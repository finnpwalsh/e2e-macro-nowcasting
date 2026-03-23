from __future__ import annotations

from dataclasses import dataclass

from ml_platform.storage import Storage

from .schema import Predictions


@dataclass(frozen=True)
class PredictionsResolver:
    storage: Storage

    def resolve(
            self,
            *,
            key: str,
            time_col: str,
            target_col: str,
    ) -> Predictions:
        df = self.storage.read_parquet(key=key)

        return Predictions(
            df=df,
            time_col=time_col,
            target_col=target_col,
        )