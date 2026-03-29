from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class FeatureResolver:
    target_col: str
    exclude_cols: tuple[str, ...] = ()

    def resolve(self, *, df: pd.DataFrame) -> list[str]:
        excluded = {self.target_col, *self.exclude_cols}

        return [c for c in df.columns if c not in excluded]