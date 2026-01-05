"""
Ingest anchor and shock time series and write raw parquet artifacts to storage.

This script is a stateless ETL entrypoint intended to be run:
- locally (`python -m scripts.etl.ingest`)
- in Airflow (DockerOperator)
- inside the ETL container image

RESPONSIBILITIES:
- Load environment/config (API keys, storage backend)
- Ingest anchor series from FRED (macro "anchors")
- Ingest shock series from Yahoo Finance (market "shocks")
- Write raw artifacts to storage using canonical raw keys
- Print a clear success message on completion

OUTPUTS (current):
- anchors: `raw_fred_all()`      (e.g., data/raw/fred/fred_all.parquet)
- shocks:  `raw_yfinance_all()`  (e.g., data/raw/yfinance/yfinance_all.parquet)

NOTES:
- This script currently ingests both anchors and shocks unconditionally.
- Future versions will parameterize which groups/sources to run and will write
  run-scoped/versioned raw artifacts for intraday shocks.
"""
from __future__ import annotations

import os
import pandas as pd

from dotenv import load_dotenv
from fredapi import Fred

from src.etl.anchors.fred.ingest import ingest_fred_series
from src.etl.anchors.fred.schema import FRED_SERIES_IDS
from src.etl.shocks.yfinance.ingest import ingest_yf_series
from src.etl.shocks.yfinance.schema import YF_TICKERS

from src.common.storage.base import Storage
from src.common.storage.paths import raw_fred_all, raw_yfinance_all
from src.common.storage.factory import get_storage


def ingest_anchors(storage: Storage) -> None:
    fred_api_key = os.getenv("FRED_API_KEY") 
    if not fred_api_key:
        raise RuntimeError("Missing FRED_API_KEY. Add it to .env")
    
    fred = Fred(api_key = fred_api_key)

    # resolve input/output paths
    fred_out_key = raw_fred_all()

    # ingest
    fred_dfs = []
    for series_id in FRED_SERIES_IDS:
        df = ingest_fred_series(fred, series_id)
        fred_dfs.append(df)
    
    fred_combined = pd.concat(fred_dfs, ignore_index=True)
    
    # write to storage
    storage.write_parquet(df=fred_combined, key=fred_out_key, index=False)

    # confirm the task ran successfully
    print(f"[OK] wrote {fred_combined.shape} -> {fred_out_key}")
    print(f"[OK] anchor ingestion complete.")


def ingest_shocks(storage: Storage) -> None:
    # resolve input/output paths
    yf_out_key = raw_yfinance_all()

    # ingest
    yf_dfs = []
    for ticker in YF_TICKERS:
        df = ingest_yf_series(ticker=ticker)
        yf_dfs.append(df)
    
    yf_combined = pd.concat(yf_dfs, ignore_index=True)
    
    # write artifacts to storage (versioned V2+)
    storage.write_parquet(df=yf_combined, key=yf_out_key, index=False)

    # confirm the task ran successfully
    print(f"[OK] wrote {yf_combined.shape} -> {yf_out_key}")
    print(f"[OK] shocks ingestion complete.")


def main() -> None:
    # load env + config
    load_dotenv()
    storage = get_storage()

    ingest_anchors(storage)
    ingest_shocks(storage)
    print(f"[OK] ingestion complete")

# run
if __name__ == "__main__":
    main()