from __future__ import annotations

from dataclasses import dataclass, asdict, is_dataclass
from typing import Any, Mapping

import pandas as pd

from ml_platform.storage import Storage
from ml_platform.storage.serde import write_joblib, write_json


@dataclass(frozen=True)
class JsonWrite:
    key: str
    payload: Any


@dataclass(frozen=True)
class JoblibWrite:
    key: str
    obj: Any

@dataclass(frozen=True)
class ParquetWrite:
    key: str
    df: pd.DataFrame


Write = JsonWrite | JoblibWrite | ParquetWrite


@dataclass(frozen=True)
class PersistencePlan:
    writes: list[Write]

    def persist(self, *, storage: Storage) -> None:
        for write in self.writes:
            if isinstance(write, ParquetWrite):
                storage.write_parquet(key=write.key, df=write.df)
            elif isinstance(write, JoblibWrite):
                write_joblib(storage=storage, key=write.key, obj=write.obj)
            elif isinstance(write, JsonWrite):
                write_json(
                    storage=storage,
                    key=write.key,
                    payload=self._resolve_json_payload(write.payload),
                )
        
    @staticmethod
    def _resolve_json_payload(payload: Any) -> Any:
        if is_dataclass(payload):
            return asdict(payload)
        elif isinstance(payload, Mapping):
            return dict(payload)
        else:
            raise TypeError(
                f"JsonArtifact payload must be a dataclass or mapping, got {type(payload).__name__}"
            )