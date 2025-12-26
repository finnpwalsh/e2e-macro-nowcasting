from __future__ import annotations
import pandas as pd
from pathlib import Path

from src.pipelines.merge import build_merged

FRED_INPATH = Path("data/processed/fred_wide.parquet")
YF_INPATH = Path("data/processed/yf_wide.parquet")
OUTPATH = Path("data/processed/merged.parquet")

def main() -> None:
    # read infiles
    fred = pd.read_parquet(FRED_INPATH)
    yf = pd.read_parquet(YF_INPATH)

    # merge
    df = build_merged(fred=fred, yf=yf)

    # write out
    df.to_parquet(OUTPATH)

    # confirm
    print(f"[OK] wrote {len(df)} rows -> {OUTPATH}")
