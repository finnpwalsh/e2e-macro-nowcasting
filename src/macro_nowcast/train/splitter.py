from __future__ import annotations

from dataclasses import dataclass
import pandas as pd


@dataclass(frozen=True)
class TimeSplitter:
    time_col: str

    def split_mask(
        df: pd.DataFrame,
        *,
        time_col: str,
        split_date: str,
    ) -> tuple[pd.Series, pd.Series]:
        d = pd.to_datetime(df[time_col])
        cutoff = pd.to_datetime(split_date)
        
        train_mask = d < cutoff
        valid_mask = ~train_mask

        return train_mask, valid_mask