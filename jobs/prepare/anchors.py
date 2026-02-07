"""
Prepare job: anchor datset ingestion and construction.

Lifecycle stage:
    Prepare

Responsibilities:
    - Ingest low-frequency macroeconomic anchor series from FRED
    - Clean and normalize raw series into a canonical long format
    - Assemble a wide, model-ready anchor feature table

Inputs:
    - External FRED API (via FRED_API_KEY)
    - Raw FRED series identifiers defined in schema

Outputs:
    - Raw combined FRED dataset (long format)
    - Processed, wide anchor feature dataset

Out of scope:
    - Model training, evaluation, or experiment tracking
    - Feature selection based on model performance
    - Generation or consumption of model artifacts

Notes:
    This job is deterministic given external source data and configuration. 
    All artifacts are written to persitent storage and consumed by downstream 
    training jobs via storage contracts.
"""
from __future__ import annotations

import os
import pandas as pd

from dotenv import load_dotenv
from fredapi import Fred

from ml_platform.storage.base import Storage
from ml_platform.storage.factory import get_storage
from ml_platform.storage import paths

from price_nowcast.prepare.anchors.fred.ingest import ingest_fred_series
from price_nowcast.prepare.anchors.fred.clean import clean_fred_long
from price_nowcast.prepare.anchors.fred.build_wide import build_fred_wide

from price_nowcast.prepare.anchors.fred.schema import FRED_SERIES_IDS


def ingest(storage: Storage) -> None:
    """Ingest raw FRED anchor series and persist a combined long-format dataset."""
    fred_api_key = os.getenv("FRED_API_KEY") 
    if not fred_api_key:
        raise RuntimeError("Missing FRED_API_KEY. Add it to .env")
    
    fred = Fred(api_key = fred_api_key)

    fred_out_key = paths.raw_fred_all()

    fred_dfs = []
    for series_id in FRED_SERIES_IDS:
        df = ingest_fred_series(fred, series_id)
        fred_dfs.append(df)
    
    fred_combined = pd.concat(fred_dfs, ignore_index=True)
    
    storage.write_parquet(df=fred_combined, key=fred_out_key, index=False)

    print(f"[OK] wrote {fred_combined.shape} -> {fred_out_key}")
    print(f"[OK] anchor ingestion complete.")


def prepare(storage: Storage) -> None:
    """Clean and transform raw FRED anchor data into a wide, model-ready feature table."""
    fred_in_key = paths.raw_fred_all()
    fred_out_key = paths.processed_fred_wide()

    df_raw = storage.read_parquet(key=fred_in_key)
    
    df_clean = clean_fred_long(df_raw)
    df_wide = build_fred_wide(df_clean)

    storage.write_parquet(df=df_wide, key=fred_out_key, index=False)

    print(f"[OK] wrote shape={df_wide.shape} -> {fred_out_key}")
    print(f"[OK] wide anchor build task completed successfully.")


def main() -> None:
    """Execute anchor ingestion and preparation using configured storage."""
    load_dotenv()
    storage = get_storage()
    ingest(storage)
    prepare(storage)


if __name__ == "__main__":
    main()