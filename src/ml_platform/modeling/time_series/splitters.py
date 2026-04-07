from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class TemporalSplitter:
    time_col: str
    split_at: str | pd.Timestamp

    def split(
        self,
        df: pd.DataFrame,
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        
        train_df = df[df[self.time_col] < self.split_at].copy()
        valid_df = df[df[self.time_col] >= self.split_at].copy()
        
        if train_df.empty or valid_df.empty:
            raise ValueError(
                f"Empty split: train={len(train_df)}, valid={len(valid_df)}"
            )

        return train_df, valid_df