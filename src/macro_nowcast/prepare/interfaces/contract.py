from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Tuple

import pandas as pd


class Contract(ABC):
    """
    Domain contract interface.

    A contract defines:
        - required columns
        - primary key uniqueness
        - coercion semantics
        - validation semantics
    """

    @property
    @abstractmethod
    def columns(self) -> Tuple[str, ...]:
        ...
    
    @property
    @abstractmethod
    def primary_key(self) -> Tuple[str, ...]:
        ...
    
    @abstractmethod
    def coerce(self, df: pd.DataFrame) -> pd.DataFrame:
        """Coerce dtypes / normalize canonical semantics."""
        ...
    
    def _validate_columns(self, df: pd.DataFrame) -> None:
        missing = [c for c in self.columns if c not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
        
    def _validate_primary_key(self, df: pd.DataFrame) -> None:
        missing = [c for c in self.primary_key if c not in df.columns]
        if missing:
            raise ValueError(f"Primary key columns missing: {missing}")
        
        if df.duplicated(list(self.primary_key)).any():
            raise ValueError("Primary key violation: duplicates detected")
    
    def validate(self, df: pd.DataFrame) -> pd.DataFrame:
        self._validate_columns(df)

        out = self.coerce(df.copy())
        
        self._validate_columns(out)
        self._validate_primary_key(out)

        return out