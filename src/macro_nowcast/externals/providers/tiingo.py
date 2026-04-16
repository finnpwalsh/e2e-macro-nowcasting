from __future__ import annotations

import pandas as pd
from macro_nowcast.externals.clients.tiingo import TiingoClient


class TiingoProvider:
    name = "tiingo"

    def __init__(self, client: TiingoClient):
        self._client = client
    
    def fetch(
            self,
            *,
            tickers: dict[str, str],
            start_date: str,
            frequency: str,
    ) -> pd.DataFrame:
        """Fetch all tickers from Tiingo and return one raw dataframe."""
        dfs: list[pd.DataFrame] = []

        for ticker_name, ticker_id in tickers.items():
            raw = self._client.fetch_series(
                ticker=ticker_id,
                start_date=start_date,
                frequency=frequency,
            )

            if raw is None or raw.empty:
                continue

            df = raw.copy()

            if "adjClose" in df.columns:
                df["value"] = pd.to_numeric(df["adjClose"], errors="coerce")
            elif "close" in df.columns:
                df["value"] = pd.to_numeric(df["adjClose"], errors="coerce")
            else: 
                continue
            
            df["ticker"] = ticker_name
            df["ticker_id"] = ticker_id
            dfs.append(df)
        
        if not dfs:
            return pd.DataFrame()
        
        out = pd.concat(dfs, ignore_index=True)
        return out.drop_duplicates(subset=["ticker_id", "date"], keep="last")