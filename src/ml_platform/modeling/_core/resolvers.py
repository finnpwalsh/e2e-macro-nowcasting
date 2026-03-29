from __future__ import annotations

from typing import Protocol

import pandas as pd


class FeatureResolver(Protocol):
    def resolve(self, *, df: pd.DataFrame) -> list[str]: ...