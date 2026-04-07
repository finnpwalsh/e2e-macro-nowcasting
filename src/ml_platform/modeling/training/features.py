from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FeatureResolver:
    target_col: str
    exclude_cols: tuple[str, ...] = ()

    def resolve(self, *, columns: list[str]) -> list[str]:
        return self._resolve(columns=columns)
    
    def _resolve(self, *, columns: list[str]) -> list[str]:
        excluded = {self.target_col, *self.exclude_cols}

        return [c for c in columns if c not in excluded]