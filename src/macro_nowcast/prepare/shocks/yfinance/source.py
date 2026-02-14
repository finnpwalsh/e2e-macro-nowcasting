from __future__ import annotations

import pandas as pd
import yfinance as yf

from macro_nowcast.prepare.interfaces import Source
from macro_nowcast.prepare.shocks.contract import CONTRACT


class YFSource(Source):
    """
    Shocks-domain adapter for yfinance.
    """

    name = "yfinance"
    domain = "shocks"
    contract = CONTRACT

    def fetch(
            self,
            *,
            tickers: dict[str, str],
            start_date: str,
    ) -> pd.DataFrame:
        dfs: list[pd.DataFrame] = []

        for ticker_name, ticker_id in tickers.items():
            t = yf.Ticker(ticker_id).history(start=start_date, auto_adjust=False)

            t = t.copy()

            if t is None or t.empty:
                print(f"[PREPARE][SHOCKS][YF] {ticker_id} has no data. Skipping.")
                continue
            
            col = "Adj Close" if "Adj Close" in t.columns else "Close"

            df = t[[col]].rename(columns={col: "value"}).reset_index()
            df.columns = ["timestamp", "value"]

            df["ticker"] = ticker_name
            df["ticker_id"] = ticker_id
            dfs.append(df)
        
        if not dfs:
            raise ValueError("[PREPARE][SHOCKS][YF] All tickers failed.")
        
        return pd.concat(dfs, ignore_index=True)

    def canonicalize(
            self,
            df: pd.DataFrame,
    ) -> pd.DataFrame:
        out = df.copy()

        out = out.rename(columns = {"timestamp":"ts"})
        out["source"] = self.name

        out = out[["ts", "value", "ticker", "ticker_id", "source"]]
        out = out.dropna(subset=["ts", "value", "ticker", "ticker_id", "source"]).reset_index(drop=True)

        return out
    
    def validate(
            self,
            df: pd.DataFrame,
    ) -> pd.DataFrame:
        return self.contract.validate(df)