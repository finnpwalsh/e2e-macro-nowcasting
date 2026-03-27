from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import pandas as pd


class Splitter(Protocol):
    def split_mask(
        self,
        *,
        df: pd.DataFrame,
        split_date: str,
    ) -> tuple[pd.Series, pd.Series]:
        ...


@dataclass(frozen=True)
class TimeSplitter:
    time_col: str

    def split_mask(
        self,
        df: pd.DataFrame,
        *,
        split_date: str,
    ) -> tuple[pd.Series, pd.Series]:
        ts = pd.to_datetime(df[self.time_col])
        cutoff = pd.to_datetime(split_date)
        
        train_mask = ts < cutoff
        valid_mask = ~train_mask

        return train_mask, valid_mask