"""
Prepare job: anchor datset ingestion and construction.

Lifecycle stage:
    Prepare

Responsibilities:
    - Ingest low-frequency macroeconomic anchor series from external sources
    - Clean and normalize raw series into a canonical long format

Inputs:
    - External FRED API (via FRED_API_KEY)
    - Raw FRED series identifiers defined in schema

Outputs:
    - Raw combined source-specific dataset (long format)
    - Canonical anchor dataset(clean long format)

Out of scope:
    - Model training, evaluation, or experiment tracking
    - Feature selection based on model performance
    - Generation or consumption of model artifacts
    - Producing model-ready feature tables

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
from macro_nowcast.storage.datasets import DATASETS

from macro_nowcast.prepare.anchors.fred.ingest import ingest_fred_series
from macro_nowcast.prepare.anchors.fred.clean import clean_fred_long

from macro_nowcast.prepare.anchors.fred.schema import FRED_SERIES_IDS


def ingest(storage: Storage) -> None:
    """Ingest raw FRED anchor series and persist a combined long-format dataset."""
    fred_api_key = os.getenv("FRED_API_KEY") 
    if not fred_api_key:
        raise RuntimeError("Missing FRED_API_KEY. Add it to .env")
    
    fred = Fred(api_key = fred_api_key)

    out_key = DATASETS.raw.fred_snapshot

    dfs = []
    for series_id in FRED_SERIES_IDS:
        df = ingest_fred_series(fred, series_id)
        dfs.append(df)
    
    combined = pd.concat(dfs, ignore_index=True)
    
    storage.write_parquet(df=combined, key=out_key, index=False)

    print(f"[OK] wrote {combined.shape} -> {out_key}")
    print(f"[OK] anchor ingestion complete.")


def prepare(storage: Storage) -> None:
    """Clean and transform raw FRED anchor data into a wide, model-ready feature table."""
    in_key = DATASETS.raw.fred_snapshot
    out_key = DATASETS.canonical.anchors

    df_raw = storage.read_parquet(key=in_key)
    df_clean = clean_fred_long(df_raw)

    storage.write_parquet(df=df_clean, key=out_key, index=False)

    print(f"[OK] wrote shape={df_clean.shape} -> {out_key}")
    print(f"[OK] wide anchor build task completed successfully.")


def main() -> None:
    """Execute anchor ingestion and preparation using configured storage."""
    load_dotenv()
    storage = get_storage()
    ingest(storage)
    prepare(storage)


if __name__ == "__main__":
    main()