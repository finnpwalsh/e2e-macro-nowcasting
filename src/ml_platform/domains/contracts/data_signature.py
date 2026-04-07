from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256

import pandas as pd


@dataclass(frozen=True)
class DataSignature:
    n_rows: int
    columns: list[str]
    dtypes: dict[str, str]
    row_fingerprint: str

    def to_dict(self) -> dict:
        return {
            "n_rows": self.n_rows,
            "columns": self.columns,
            "dtypes": self.dtypes,
            "row_fingerprint": self.row_fingerprint,
        }


class DataSignatureBuilder:
    def build(
        self,
        *,
        df: pd.DataFrame,
    ) -> DataSignature:
        return DataSignature(
            n_rows=len(df),
            columns=list(df.columns),
            dtypes={k: str(v) for k, v in df.dtypes.items()},
            row_fingerprint=self._hash_frame(df),
        )
    
    def _hash_frame(df: pd.DataFrame) -> str:
        hashed = pd.util.hash_pandas_object(df, index=False).to_numpy()
        return sha256(hashed.tobytes()).hexdigest()