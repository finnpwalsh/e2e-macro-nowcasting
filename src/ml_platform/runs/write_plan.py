from dataclasses import dataclass
from typing import Any, List

import pandas as pd


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

@dataclass(frozen=True)
class WritePlan:
    writes: List[JsonWrite | JoblibWrite | ParquetWrite]