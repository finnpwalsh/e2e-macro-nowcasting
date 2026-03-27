from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import pandas as pd


class Splitter(Protocol):
    def split(
        self,
        *,
        df: pd.DataFrame,
        split_date: str,
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        ...


@dataclass(frozen=True)
class TimeSplitter:
    time_col: str

    def split(
        self,
        df: pd.DataFrame,
        *,
        split_date: str,
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        
        train_df = df[df[self.time_col] < split_date].copy()
        valid_df = df[df[self.time_col] >= split_date].copy()
        
        if train_df.empty or valid_df.empty:
            raise ValueError(
                f"Empty split: train={len(train_df)}, valid={len(valid_df)}"
            )

        return train_df, valid_df