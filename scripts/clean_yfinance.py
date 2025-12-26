"""
Clean raw yfinance data.

Ingest long-form raw yfinance parquet, clean and pivot, and write
cleaned long- and wide-form yfinance DataFrames to data/processed.

RESPONSIBILITIES:
- affirm inpath exists
- ingest raw long-form yfinance parquet as DataFrame
- pivot and clean raw long-form yfinance DataFrame
- write cleaned long- and wide-form yfinance DataFrames to data/processed
- affirm task ran successfully

OUTPUTS:
- data/processed/yf_long.parquet
- data/processed/yf_wide.parquet
"""
from __future__ import annotations

import pandas as pd
from pathlib import Path

from src.pipelines.yfinance import prep_yf

INPATH = Path("data/raw/yf_long.parquet")
OUTDIR = Path("data/processed")

def main() -> None:
    if not INPATH.exists():
        raise FileNotFoundError(f"Missing raw YF file: {INPATH}")
    
    # read infile
    df_raw = pd.read_parquet(INPATH)
    
    # clean
    df_long, df_wide = prep_yf(df_raw)

    # write to data/processed
    OUTDIR.mkdir(parents = True, exist_ok=True)
    df_long.to_parquet(OUTDIR / "yf_long.parquet", index=False)
    df_wide.to_parquet(OUTDIR / "yf_wide.parquet", index=False)

    # confirm
    print(f"[OK] wrote df_long shape={df_long.shape} -> {OUTDIR / 'yf_long.parquet'}")
    print(f"[OK] wrote df_wide shape={df_wide.shape} -> {OUTDIR / 'yf_wide.parquet'}")


if __name__ == "__main__":
    main()