from __future__ import annotations

import pandas as pd
from fredapi import Fred

from ml_platform.data.sources import AuthConfig
from ml_platform.platform.secrets import SecretResolver


class FREDClient:
    def __init__(
        self,
        *,
        auth: AuthConfig,
        secrets: SecretResolver
    ) -> None:
        api_key = self._resolve_api_key(
            auth=auth,
            secrets=secrets,
        )
        self._fred = Fred(api_key=api_key)
    
    @staticmethod
    def _resolve_api_key(
        *,
        auth: AuthConfig,
        secrets: SecretResolver,
    ) -> str:
        auth.validate()

        if auth.type != "api_key":
            raise ValueError("TiingoClient requires api_key authentication.")
        
        if auth.key_name is None:
            raise ValueError("AuthConig.key_name is required for api_key auth.")
        
        api_key = secrets.get(auth.key_name)
        
        if not api_key:
            raise ValueError(f"Missing API key for secret: '{auth.key_name}'.")
        
        return api_key
    
    def fetch(
        self,
        *,
        series_id: str,
        start_date: str,
        end_date: str | None = None,
    ) -> pd.DataFrame:
        s = self._fred.get_series(
            series_id=series_id,
            observation_start=start_date,
            observation_end=end_date,
        )

        return (
            s.rename("value")
             .reset_index()
             .rename(columns = {"index":"date"})
        )