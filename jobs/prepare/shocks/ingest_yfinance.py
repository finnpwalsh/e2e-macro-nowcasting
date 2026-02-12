"""
Prepare: ingest raw yfinance shock series.

Lifecycle stage: 
    Prepare

Writes:
    - DATASETS.raw.yfinance_snapshot
"""
from __future__ import annotations

import pandas as pd

from dotenv import load_dotenv

from ml_platform.storage.base import Storage
from ml_platform.storage.factory import get_storage
from macro_nowcast.storage.datasets import DATASETS

from macro_nowcast.prepare.shocks.yfinance.ingest import ingest_yf_series

from macro_nowcast.prepare.shocks.yfinance.schema import YF_TICKERS


def run(storage: Storage) -> None:
    """Ingest raw yfinance shock series and persist a combined long-fomat dataset."""
    out_key = DATASETS.raw.yfinance_snapshot

    dfs = []
    for ticker in YF_TICKERS:
        df = ingest_yf_series(ticker=ticker)
        dfs.append(df)
    
    combined = pd.concat(dfs, ignore_index=True)
    
    storage.write_parquet(df=combined, key=out_key, index=False)

    print(f"[OK] wrote {combined.shape} -> {out_key}")
    print(f"[OK] yfinance ingestion complete.")


def main() -> None:
    """Execute shock ingestion and preparation using configured storage."""
    load_dotenv()
    storage = get_storage()
    run(storage)


if __name__ == "__main__":
    main()