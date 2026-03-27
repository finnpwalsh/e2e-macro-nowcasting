from __future__ import annotations

from typing import Any, Protocol

import pandas as pd

class ModelSpec(Protocol):
    def build(self) -> Any: ...


class FeatureResolver(Protocol):
    def resolve(self, *, df: pd.DataFrame) -> list[str]: ...