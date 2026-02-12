"""
Prepare: ingest raw FRED anchor series.

Lifecycle stage:
    Prepare

Writes:
    - DATASETS.raw.fred_snapshot
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

from macro_nowcast.prepare.anchors.fred.schema import FRED_SERIES_IDS


def run(storage: Storage) -> None:
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


def main() -> None:
    load_dotenv()
    storage = get_storage()
    run(storage)


if __name__ == "__main__":
    main()