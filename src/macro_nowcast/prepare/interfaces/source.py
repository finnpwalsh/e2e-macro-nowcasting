from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Literal

import pandas as pd


class Source(ABC):
    """
    External data provider adapter.

    Contract:
        fetch → canonicalize → validate
    """

    name: str
    domain: Literal["anchors", "shocks"]

    @abstractmethod
    def fetch(self, **kwargs) -> pd.DataFrame:
        """Fetch raw data from the external system."""
        ...
    
    @abstractmethod
    def canonicalize(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        """Convert raw external data into canonical domain format."""
        ...
    
    @abstractmethod
    def validate(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        """Validate against domain contract."""
        ...
    

    def load(self, **kwargs) -> pd.DataFrame:
        """
        Orchestrates the standard flow:
            fetch → canonicalize → validate
        """
        df = self.fetch(**kwargs)
        df = self.canonicalize(df, **kwargs)
        df = self.validate(df, **kwargs)
        return df