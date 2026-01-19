"""
Build processed feature tables from raw anchor datasets.

This script reads raw long-form datasets from storage, applies cleaning and
feature construction, and writes processed artifacts back to storage.

RESPONSIBILITIES:
- Read raw FRED (anchors) long-form data, clean, pivot to wide monthly table
- Write processed feature tables to storage
- Print a clear success message on completion

OUTPUTS:
- anchors: `paths.processed_fred_wide()`        (e.g., data/processed/fred_wide.parquet)
"""
from __future__ import annotations

from dotenv import load_dotenv

from src.etl.anchors.fred.clean import clean_fred_long
from src.etl.anchors.fred.build_wide import build_fred_wide
from src.etl.shocks.yfinance.clean import clean_yf_long
from src.etl.shocks.yfinance.build_monthly import build_and_resample_yf

from src.common.storage.base import Storage
from src.common.storage.factory import get_storage
from src.common.storage import paths


def build_wide_anchors(storage: Storage) -> None:
    # resolve I/O paths
    fred_in_key = paths.raw_fred_all()
    fred_out_key = paths.processed_fred_wide()

    # read infile
    df_raw = storage.read_parquet(key=fred_in_key)
    
    # clean
    df_clean = clean_fred_long(df_raw)
    df_wide = build_fred_wide(df_clean)

    # write cleaned wide-form DataFrame to storage
    storage.write_parquet(df=df_wide, key=fred_out_key, index=False)

    # confirm task was successful
    print(f"[OK] wrote shape={df_wide.shape} -> {fred_out_key}")
    print(f"[OK] wide anchor build task completed successfully.")


def build_monthly_shocks(storage: Storage) -> None:
    # resolve I/O paths
    yf_in_key = paths.raw_yfinance_all()
    yf_out_key = paths.processed_yfinance_features()

    # read infile
    df_raw = storage.read_parquet(key=yf_in_key)
    
    # prep
    df_clean = clean_yf_long(df_raw)
    df_feat = build_and_resample_yf(df_clean)

    # write cleaned wide-form feature DataFrame to storage
    storage.write_parquet(df=df_feat, key=yf_out_key)

    # confirm
    print(f"[OK] wrote shape={df_feat.shape} -> {yf_out_key}")
    print(f"[OK] monthly shock feature build task completed successfully.")

def main() -> None:
    load_dotenv()
    storage = get_storage()

    build_wide_anchors(storage)
    build_monthly_shocks(storage)
    
    print(f"[OK] feature build task completed successfully.")


if __name__ == "__main__":
    main()