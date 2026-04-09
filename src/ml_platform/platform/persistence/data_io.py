from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Any
from io import BytesIO
import json

import pandas as pd

from ..storage import Storage


@dataclass(frozen=True)
class DataIO:
    storage: Storage

    def read_json(self, *, key: str) -> dict:
        data = self.storage.read_bytes(key=key)
        return json.loads(data.decode("utf-8"))

    def write_json(self, *, key: str, payload: Mapping[str, Any]) -> None:
        data = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")
        self.storage.write_bytes(key=key, data=data)
    
    def write_parquet(self, *, key: str, df: pd.DataFrame, **kwargs) -> None:
        buffer = BytesIO()
        df.to_parquet(buffer, index=False, **kwargs)
        self.storage.write_bytes(key=key, data=buffer.getvalue())

    def read_parquet(self, *, key: str, **kwargs) -> pd.DataFrame:
        data = self.storage.read_bytes(key=key)
        return pd.read_parquet(BytesIO(data), **kwargs)