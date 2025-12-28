"""
Ingest all yfinance tickers, combine, and write combined
DataFrame to data/raw/yfinance/ as parquet.

RESPONSIBILITIES:
- ingest all yf tickers
- append to combined DataFrame
- write combined DataFrame to data/raw/yfinance/
- confirm task ran successfully

OUTPUTS:
- data/raw/yfinance/yf_all.parquet
"""
from __future__ import annotations

import pandas as pd

from src.ingestion.yfinance import ingest_yf_series
from src.config.yfinance import YF_TICKERS
from src.storage.paths import raw_yfinance_all
from src.storage.factory import get_storage

def main() -> None:
    # load env
    storage = get_storage()

    # append each yfinance tickers to list
    dfs = []
    for ticker in YF_TICKERS:
        df = ingest_yf_series(ticker=ticker)
        dfs.append(df)
        print(f"[OK] fetched {ticker}:  {len(df):,} rows.")
    
    # concatinate yfinance ticker list to combined DataFrame
    combined = pd.concat(dfs, ignore_index=True)
    
    # write out
    out_key = raw_yfinance_all()
    storage.write_parquet(df=combined, key=out_key, index=False)

    # confirm the task ran successfully
    print(f"[OK] wrote {len(combined):,} rows -> {out_key}")

# run
if __name__ == "__main__":
    main()

