"""
Prepare job: shock dataset ingestion and feature construction.

Lifecycle stage:
    Prepare

Responsibilities:
    - Ingest high-frequency financial market series via external sources
    - Clean and normalize raw series into a canonical long format

Inputs:
    - External market data
    - Ticker universe defined in schema

Outputs:
    - Raw combined yfinance dataset (long format)
    - Processed shock feature dataset (resampled / aggregated)

Out of scope:
    - Model training, evaluation, or experiment tracking
    - Feature selection based on model performance
    - Generation or consumption of model artifacts

Notes:
    This job is deterministic given external source data and configuration.
    All artifacts are written to persistent storage and consumed by downstream 
    training jobs via storage contracts.
"""
from __future__ import annotations

import pandas as pd

from dotenv import load_dotenv

from ml_platform.storage.base import Storage
from ml_platform.storage.factory import get_storage
from macro_nowcast.storage.datasets import DATASETS

from macro_nowcast.prepare.shocks.yfinance.ingest import ingest_yf_series
from macro_nowcast.prepare.shocks.yfinance.clean import clean_yf_long

from macro_nowcast.prepare.shocks.yfinance.schema import YF_TICKERS


def ingest(storage: Storage) -> None:
    """Ingest raw yfinance shock series and persist a combined long-fomat dataset."""
    out_key = DATASETS.raw.yfinance_snapshot

    dfs = []
    for ticker in YF_TICKERS:
        df = ingest_yf_series(ticker=ticker)
        dfs.append(df)
    
    combined = pd.concat(dfs, ignore_index=True)
    
    storage.write_parquet(df=combined, key=out_key, index=False)

    print(f"[OK] wrote {combined.shape} -> {out_key}")
    print(f"[OK] shocks ingestion complete.")


def prepare(storage: Storage) -> None:
    """Clean and normalize shocks into a the canonical long-format shocks dataset."""
    in_key = DATASETS.raw.yfinance_snapshot
    out_key = DATASETS.canonical.shocks

    df_raw = storage.read_parquet(key=in_key)
    
    df_clean = clean_yf_long(df_raw)

    storage.write_parquet(df=df_clean, key=out_key)

    print(f"[OK] wrote shape={df_clean.shape} -> {out_key}")
    print(f"[OK] canonical shocks dataset build completed successfully.")


def main() -> None:
    """Execute shock ingestion and preparation using configured storage."""
    load_dotenv()
    storage = get_storage()
    ingest(storage)
    prepare(storage)


if __name__ == "__main__":
    main()