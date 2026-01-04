"""
Ingest FRED time series and write data to parquet files under data/raw/fred/.

RESPONSIBILITIES:
- load FRED api
- call ingest_fred_series
- write raw data to data/raw/fred/
- confirm task ran successfully

OUTPUTS:
- data/raw/fred/fred_all.parquet
"""
from __future__ import annotations

import os
import pandas as pd

from dotenv import load_dotenv
from fredapi import Fred

from src.ingestion.fred import ingest_fred_series
from src.config.fred import FRED_SERIES
from src.storage.paths import raw_fred_all
from src.storage.factory import get_storage

def main() -> None:
    # load env
    load_dotenv()
    storage = get_storage()

    # load FRED
    api_key = os.getenv("FRED_API_KEY") 
    if not api_key:
        raise RuntimeError("Missing FRED_API_KEY. Add it to .env")
    
    fred = Fred(api_key = api_key)
    
    # append each FRED series to list
    dfs = []
    for series_id in FRED_SERIES:
        df = ingest_fred_series(fred, series_id)
        dfs.append(df)
        print(f"[OK] fetched {series_id}: {len(df):,} rows.")
    
    # concatinate FRED series list -> combined DataFrame
    combined = pd.concat(dfs, ignore_index=True)
    
    # write concatinated DataFrame to storage
    out_key = raw_fred_all()
    storage.write_parquet(df=combined, key=out_key, index=False)

    # confirm the task ran successfully
    print(f"[OK] wrote {len(combined):,} rows -> {out_key}")

# run
if __name__ == "__main__":
    main()