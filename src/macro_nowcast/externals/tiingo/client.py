from __future__ import annotations

import requests
import pandas as pd

from ml_platform.data.sources import AuthConfig
from ml_platform.platform.secrets import SecretResolver


class TiingoClient:
    """
    Client for Tiingo REST API.
    """
    BASE_URL = "https://api.tiingo.com/tiingo/daily"
    
    def __init__(
        self,
        *,
        auth: AuthConfig,
        secrets: SecretResolver,
    ) -> None:
        self._api_key = self._resolve_api_key(
            auth=auth,
            secrets=secrets,
        )

    def fetch(
            self,
            *,
            ticker: str,
            start_date: str,
            end_date: str | None = None,
            frequency: str = "daily",
    ) -> pd.DataFrame:
        url = f"{self.BASE_URL}/{ticker}/prices"
        
        params: dict[str, str] = {
            "startDate": start_date,
            "resampleFreq": frequency,
            "format": "json",
            "token": self._api_key,
        }

        if end_date:
            params["endDate"] = end_date
        
        r = requests.get(url, params=params)
        r.raise_for_status()

        df = pd.DataFrame(r.json())
        if not df.empty and "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"]).dt.tz_localize(None)
        
        return df
    
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