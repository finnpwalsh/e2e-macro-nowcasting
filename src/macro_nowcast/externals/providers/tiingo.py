from __future__ import annotations

import pandas as pd
from macro_nowcast.externals.clients.tiingo import TiingoClient


class TiingoProvider:
    name = "tiingo"
    domain = "shocks"

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
            df = self._client.fetch_series(
                ticker=ticker_id,
                start_date=start_date,
                frequency=frequency,
            )

            if df is None or df.empty:
                continue

            df = df.copy()
            df["ticker"] = ticker_name
            df["ticker_id"] = ticker_id
            dfs.append(df)
        
        if not dfs:
            return pd.DataFrame()
        
        out = pd.concat(dfs, ignore_index=True)
        return out.drop_duplicates(subset=["ticker_id", "date"], keep="last")