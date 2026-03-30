from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class DefaultFeatureResolver:
    exclude_cols: tuple[str, ...] = ()

    def resolve(self, *, df: pd.DataFrame, target_col: str) -> list[str]:
        excluded = {target_col, *self.exclude_cols}

        return [c for c in df.columns if c not in excluded]


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