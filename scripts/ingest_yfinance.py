"""
Ingest all yfinance tickers, combine, and write combined df to 
data/raw as parquet.

RESPONSIBILITIES:
- ingest all yf tickers
- append to combined DataFrame
- write combined df to data/raw/yf_long.parquet
- confirm task ran successfully

OUTPUTS:
- data/raw/yf_long.parquet
"""
from __future__ import annotations

import pandas as pd
from pathlib import Path

from src.ingestion.yfinance import ingest_yf_series
from src.config.yfinance import YF_TICKERS

OUTDIR = Path("data/raw")

def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)

    dfs = []

    for ticker in YF_TICKERS:
        df = ingest_yf_series(ticker=ticker)
        dfs.append(df)
        print(f"[OK] fetched {ticker}:  {len(df):,} rows.")
    
    # write combined series into data/raw
    outpath = OUTDIR / "yf_long.parquet"
    combined = pd.concat(dfs, ignore_index=True)
    combined.to_parquet(outpath, index=False)

    # confirm the task ran successfully
    print(f"[OK] wrote {len(combined):,} rows -> {outpath}")

# run
if __name__ == "__main__":
    main()

