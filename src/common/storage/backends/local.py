"""Local filesystem implementation of Storage."""

from __future__ import annotations

import pandas as pd
from pathlib import Path


class LocalStorage:
    """
    Local filesystem storage backend.

    Interprets storage keys as paths relative to the project root.
    """
    
    def read_parquet(self, key: str) -> pd.DataFrame:
        """
        Read a parquet object from local storage.
        
        Parameters:
        - key : str
            -> Storage key, e.g. 'data/raw/fred/fred_all.parquet'
        
        Returns:
        - pd.DataFrame

        Raises:
        - FileNotFoundError: if no input file is found.
        """
        path = Path(key)

        if not path.exists():
            raise FileNotFoundError(f"Missing parquet file: {path}")

        return pd.read_parquet(path)

    def write_parquet(self, df: pd.DataFrame, key: str, **kwargs) -> None:
        """
        Write a DataFrame to local storage as parquet.
        
        Parameters:
        - df : pd.DataFrame
            -> DataFrame to be written as parquet
        - key : str
            -> Storage key, e.g. 'data/processed/fred_wide.parquet`
        
        Outputs:
        - None
        """
        path = Path(key)
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(path, **kwargs)
    
    def read_bytes(self, key: str) -> bytes:
        """
        Read raw bytes from local storage.
        
        Parameters:
        - key : str
            -> Storage key, e.g. `artifacts/models/{model_name}/{run_id}/metrics.json`
        
        Outputs:
        - bytes

        Raises:
        - FileNotFoundError
        """
        path = Path(key)

        if not path.exists():
            raise FileNotFoundError(f"Missing file: {path}")
        
        return path.read_bytes()
    
    def write_bytes(self, data: bytes, key: str) -> None:
        """
        Write raw bytes to local storage.
        
        Parameters:
        - data : bytes
            -> raw bytes
        - key : str
            -> Storage key, e.g. artifacts/models/{model_name}/{run_id}/metrics.json
        
        Returns:
        - None
        """
        path = Path(key)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        

    def exists(self, key: str) -> bool:
        """Check whether a key exists in storage."""
        return Path(key).exists()