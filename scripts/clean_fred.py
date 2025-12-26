"""
Clean raw FRED combined time series and write long- and 
wide-form data to parquet under data/processed/. Wide-form
is ready for merging.

RESPONSIBILITIES:
- ingest raw FRED series
- call prep_fred
- write long- and wide-form DataFrame to data/processed/ as parquet
- confirm task ran successfully

OUTPUTS:
- data/processed/fred_long.parquet
- data/processed/fred_wide.parquet
"""
from __future__ import annotations

import pandas as pd
from pathlib import Path

from src.pipelines.fred import prep_fred

INPATH = Path("data/raw/fred_all.parquet")
OUTDIR = Path("data/processed")

def main() -> None:
    # comfirm inpath exists
    if not INPATH.exists():
        raise FileNotFoundError(f"Missing raw FRED file: {INPATH}")
    
    # read infile
    df_raw = pd.read_parquet(INPATH)
    
    # clean
    df_long, df_wide = prep_fred(df_raw)

    # write to data/processed
    OUTDIR.mkdir(parents = True, exist_ok=True)
    df_long.to_parquet(OUTDIR / "fred_long.parquet", index=False)
    df_wide.to_parquet(OUTDIR / "fred_wide.parquet", index=False)

    # confirm
    print(f"[OK] wrote df_long shape={df_long.shape} -> {OUTDIR / 'fred_long.parquet'}")
    print(f"[OK] wrote df_wide shape={df_wide.shape} -> {OUTDIR / 'fred_wide.parquet'}")


if __name__ == "__main__":
    main()