from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict, is_dataclass
from typing import Any, Mapping
from collections.abc import Sequence

import pandas as pd

from ml_platform.storage import Storage
from ml_platform.storage.serde import write_joblib, write_json


class WriteOp(ABC):
    key: str

    @abstractmethod
    def persist(self, *, storage: Storage) -> None: ...


@dataclass(frozen=True)
class JsonWrite(WriteOp):
    key: str
    payload: Any

    def persist(self, *, storage: Storage) -> None:
        write_json(
            storage=storage,
            key=self.key,
            payload=self._resolve_json_payload(self.payload),
        )
    
    @staticmethod
    def _resolve_json_payload(payload: Any) -> Any:
        if is_dataclass(payload): return asdict(payload)
        elif isinstance(payload, Mapping): return dict(payload)
        else: raise TypeError(
                f"JsonWrite payload must be a dataclass or mapping, got {type(payload).__name__}"
            )


@dataclass(frozen=True)
class JoblibWrite(WriteOp):
    key: str
    obj: Any

    def persist(self, *, storage: Storage) -> None:
        write_joblib(storage=storage, key=self.key, obj=self.obj)


@dataclass(frozen=True)
class ParquetWrite(WriteOp):
    key: str
    df: pd.DataFrame

    def persist(self, *, storage: Storage) -> None:
        storage.write_parquet(key=self.key, df=self.df)


@dataclass(frozen=True)
class PersistencePlan:
    writes: Sequence[WriteOp]

    def persist(self, *, storage: Storage) -> None:
        for write in self.writes:
            write.persist(storage=storage)