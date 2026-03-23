from __future__ import annotations

from dataclasses import dataclass

from ml_platform.storage import Storage

from .schema import Residuals


@dataclass(frozen=True)
class ResidualsResolver:
    storage: Storage

    def resolve(
            self,
            *,
            key: str,
            time_col: str,
    ) -> Residuals:
        df = self.storage.read_parquet(key=key)
        return Residuals(
            df=df,
            time_col=time_col,
        )