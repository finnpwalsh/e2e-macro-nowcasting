'''
Run ingest/fred.py and write output to data/raw/fred_{FRED_SERIES}.parquet

RESPONSIBILITIES:
- load FRED api
- call ingest_fred_api
- write raw data to data/raw
- confirm task ran successfully
'''

from __future__ import annotations

import os
import pandas as pd
from pathlib import Path

from dotenv import load_dotenv
from fredapi import Fred

from src.ingestion.fred import ingest_fred_series

START_DATE = "2010-01-01"
OUTDIR = Path("data/raw")

def main() -> None:
    # load secrets
    load_dotenv()
    api_key = os.getenv("FRED_API_KEY")

    # handle missing 
    if not api_key:
        raise RuntimeError("Missing FRED_API_KEY. Add it to .env")
    
    # make out directory (and all parent directories) if
    # doesn't exist. Do not throw error if it does exist
    OUTDIR.mkdir(parents=True, exist_ok=True)

    # create Fred variable
    fred = Fred(api_key = api_key)

    # initialize dataframe for concatinated series
    dfs = []

    # read all fred series from src/config
    config_path = Path("src/config/fred.txt")
    with open(config_path) as f:
        # control for blank lines and comments
        fred_series = [
            line.strip() for line in f
            if line.strip() and not line.startswith("#")
        ]
    
    # control for null input
    if not fred_series:
        raise RuntimeError("No FRED series found in src/config/fred.txt.")
    
    # write each FRED series into data/raw
    for series_id in fred_series:
        # ingest series
        df = ingest_fred_series(fred, series_id, start=START_DATE)

        # make out-path, save data as parquet
        out_path = OUTDIR / f"fred_{series_id}.parquet"
        df.to_parquet(out_path, index=False)

        # append to dfs
        dfs.append(df)

        # confirm the task ran successfully
        print(f"[OK] wrote {len(df):,} rows -> {out_path}")
    
    # write combined series into data/raw
    out_path = OUTDIR / "fred_all.parquet"
    combined = pd.concat(dfs, ignore_index=True)
    combined.to_parquet(out_path, index=False)

    # confirm the task ran successfully
    print(f"[OK] wrote {len(combined):,} rows -> {out_path}")

# run
if __name__ == "__main__":
    main()