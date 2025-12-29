"""
Merge FRED and yfinance data and write model-ready merged 
file to data/processed.

RESPONSIBILITIES:
- ingest wide-form FRED, yfinance parquets
- build merged DataFrame
- write model-ready merged DataFrame to data/processed/merged.parquet
- confirm task ran successfully

OUTPUTS:
- data/processed/merged.parquet
"""
from __future__ import annotations

from src.pipelines.merge import build_merged
from src.storage.factory import get_storage
from src.storage.paths import processed_fred_wide, processed_yfinance_features, processed_merged

def main() -> None:
    # load env
    storage = get_storage()

    # read infiles
    fred_in = processed_fred_wide()
    yf_in = processed_yfinance_features()

    fred = storage.read_parquet(fred_in)
    yf = storage.read_parquet(yf_in)

    # merge
    df = build_merged(fred=fred, yf=yf)

    # write merged DataFrame to storage
    out_key = processed_merged()
    df.to_parquet(out_key)

    # confirm
    print(f"[OK] wrote {len(df)} rows -> {out_key}")

if __name__ == "__main__":
    main()