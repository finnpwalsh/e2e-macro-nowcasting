from __future__ import annotations

import pandas as pd
from pathlib import Path

from src.pipelines.fred_clean import clean_fred_long

INPATH = Path("data/raw/fred_all.parquet")
OUTPATH = Path("data/processed/fred_long.parquet")

def main():
    # ingest raw
    if not INPATH.exists():
        raise FileNotFoundError(f"Missing raw FRED file: {INPATH}")
    
    # read infile
    df_in = pd.read_parquet(INPATH)
    if df_in.empty:
        raise ValueError(f"FRED input file is empty: {INPATH}")
    
    # clean
    df = clean_fred_long(df_in)

    # write to data/processed
    OUTPATH.parent.mkdir(parents = True, exist_ok=True)
    df.to_parquet(OUTPATH, index=False)

    # confirm
    print(f"[OK] wrote {len(df):,} rows -> {OUTPATH}")

if __name__ == "__main__":
    main()