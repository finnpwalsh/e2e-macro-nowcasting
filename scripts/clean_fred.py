from __future__ import annotations

import pandas as pd
from pathlib import Path

from src.pipelines.fred_clean import prep_fred

INPATH = Path("data/raw/fred_all.parquet")
OUTPATH_LONG = Path("data/processed/fred_long.parquet")
OUTPATH_WIDE = Path("data/processed/fred_wide.parquet")

def main():
    # ingest raw
    if not INPATH.exists():
        raise FileNotFoundError(f"Missing raw FRED file: {INPATH}")
    
    # read infile
    df_raw = pd.read_parquet(INPATH)
    if df_raw.empty:
        raise ValueError(f"FRED input file is empty: {INPATH}")
    
    # clean
    df_long, df_wide = prep_fred(df_raw)

    # write long to data/processed
    OUTPATH_LONG.parent.mkdir(parents = True, exist_ok=True)
    df_long.to_parquet(OUTPATH_LONG, index=False)

    # confirm
    print(f"[OK] wrote {len(df_long):,} rows -> {OUTPATH_LONG}")

    # write wide to data/processed
    OUTPATH_WIDE.parent.mkdir(parents = True, exist_ok=True)
    df_wide.to_parquet(OUTPATH_WIDE, index=False)

    # confirm
    print(f"[OK] wrote {len(df_wide):,} rows -> {OUTPATH_WIDE}")

if __name__ == "__main__":
    main()