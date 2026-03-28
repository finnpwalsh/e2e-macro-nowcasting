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
    ) -> Residuals:
        return Residuals(self.storage.read_parquet(key=key))