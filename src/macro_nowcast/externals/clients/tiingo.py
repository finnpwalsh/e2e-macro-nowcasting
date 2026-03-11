from __future__ import annotations

import requests
import pandas as pd


class TiingoClient:
    """
    Client for Tiingo REST API.

    Responsibilities:
        - Fetch raw price series
        - Return normalized DataFrame
    
    Out of scope:
        - Canonicalization
        - Validation
    """

    BASE_URL = "https://api.tiingo.com/tiingo/daily"

    def __init__(self, api_key: str):
        self._api_key = api_key

    # hide API key
    def __repr__(self) -> str:
        return "TiingoClient(api_key=****)"
    
    def fetch_series(
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