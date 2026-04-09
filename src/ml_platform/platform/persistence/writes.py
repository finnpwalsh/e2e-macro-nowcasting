from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict, is_dataclass
from typing import Any, Mapping

import pandas as pd

from ml_platform.platform.storage import Storage
from .data_io import DataIO


class WriteOp(ABC):
    key: str

    @abstractmethod
    def persist(self, *, storage: Storage) -> None: ...


@dataclass(frozen=True)
class JsonWrite(WriteOp):
    key: str
    payload: Mapping[str, Any] | object

    def persist(self, *, storage: Storage) -> None:
        DataIO(storage).write_json(
            key=self.key,
            payload=self.payload,
        )
    
    @staticmethod
    def _resolve_payload(payload: Mapping[str, Any] | object) -> dict[str, Any]:
        if is_dataclass(payload):
            return asdict(payload)
        
        if isinstance(payload, Mapping):
            return dict(payload)
        
        raise TypeError(
            "JsonWrite payload must be a dataclass or Mapping[str, Any], "
            f"got {type(payload).__name__}"
        )


@dataclass(frozen=True)
class ParquetWrite(WriteOp):
    key: str
    df: pd.DataFrame
    parquet_kwargs: Mapping[str, Any] | None = None

    def persist(self, *, storage: Storage) -> None:
        DataIO(storage).write_parquet(
            key=self.key,
            df=self.df,
            **(self.parquet_kwargs or {}),
        )