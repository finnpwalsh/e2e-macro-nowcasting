"""
Ingest anchor time series and write raw parquet artifacts to storage.

This script is a stateless ETL entrypoint intended to be run:
- locally (`python -m scripts.etl.ingest`)
- in Airflow (DockerOperator)
- inside the ETL container image

RESPONSIBILITIES:
- Load environment/config (API keys, storage backend)
- Ingest anchor series from FRED (macro "anchors")
- Write raw artifacts to storage using canonical raw keys
- Print a clear success message on completion

OUTPUTS (current):
- anchors: `raw_fred_all()`      (e.g., data/raw/fred/fred_all.parquet)
"""
from __future__ import annotations

import os
import pandas as pd

from dotenv import load_dotenv
from fredapi import Fred

from src.etl.anchors.fred.ingest import ingest_fred_series
from src.etl.anchors.fred.schema import FRED_SERIES_IDS

from src.common.storage.base import Storage
from src.common.storage.paths import raw_fred_all
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


def main() -> None:
    # load env + config
    load_dotenv()
    storage = get_storage()

    ingest_anchors(storage)

# run
if __name__ == "__main__":
    main()