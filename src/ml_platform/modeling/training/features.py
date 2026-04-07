from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import pandas as pd


class FeatureResolver(Protocol): 
    def resolve(self, *, df: pd.DataFrame, target_col: str) -> list[str]: ...


@dataclass(frozen=True)
class DefaultFeatureResolver:
    exclude_cols: tuple[str, ...] = ()

    def resolve(self, *, df: pd.DataFrame, target_col: str) -> list[str]:
        excluded = {target_col, *self.exclude_cols}

        return [c for c in df.columns if c not in excluded]