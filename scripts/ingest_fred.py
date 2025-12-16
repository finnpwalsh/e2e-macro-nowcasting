from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from fredapi import Fred

from src.ingestion.fred import ingest_fred_series

def main():
    # load secrets
    load_dotenv()
    api_key = os.getenv("FRED_API_KEY")

    # handle missing 
    if not api_key:
        raise RuntimeError("Missing FRED_API_KEY. Add it to .env")
    
    # check for .env variables FRED_SERIES, FRED START. If they
    # do not exist, use "CPIAUCSL and 2010-01-01, respectively"
    series_id = os.getenv("FRED_SERIES", "CPIAUCSL")
    start     = os.getenv("FRED_START", "2010-01-01")

    # create Fred variable, ingest the series into a df
    fred = Fred(api_key = api_key)
    df   = ingest_fred_series(fred, series_id, start=start)

    # make out directory (and all parent directories) if
    # doesn't exist. Do not throw error if it does exist
    outdir = Path("data/raw")
    outdir.mkdir(parents=True, exist_ok=True)
    
    # make out path, save data as csv
    out_path = outdir / f"fred_{series_id}.csv"
    df.to_csv(out_path, index=False)

    # confirm the task ran successfully
    print(f"[OK] wrote {len(df):,} rows -> {out_path}")

# run
if __name__ == "__main__":
    main()