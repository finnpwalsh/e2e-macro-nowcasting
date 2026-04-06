from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import pandas as pd


class Splitter(Protocol):
    def split(
        self,
        *,
        df: pd.DataFrame,
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        ...


@dataclass(frozen=True)
class RandomSplitter:
    train_frac: float = 0.8
    shuffle: bool = True
    random_state: int | None = None

    def split(
        self,
        *,
        df: pd.DataFrame,
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        if self.shuffle:
            df = df.sample(frac=1.0, random_state=self.random_state)
        
        n_train = int(len(df) * self.train_frac)

        train_df = df.iloc[:n_train]
        valid_df = df.iloc[n_train]

        return train_df, valid_df


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