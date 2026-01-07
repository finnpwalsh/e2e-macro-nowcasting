"""
Build processed feature tables from raw shock datasets.

This script reads raw long-form datasets from storage, applies cleaning and
feature construction, and writes processed artifacts back to storage.

RESPONSIBILITIES:
- Read raw Yahoo Finance (shocks) long-form data, clean, build monthly features
- Write processed feature tables to storage
- Print a clear success message on completion

OUTPUTS:
- shocks:  `paths.processed_yfinance_features()` (e.g., data/processed/yfinance_features.parquet)

NOTES:
- This script currently builds monthly shocks features.
- Future versions may support additional frequencies (e.g., intraday shocks).
"""
from __future__ import annotations

from dotenv import load_dotenv

from src.etl.shocks.yfinance.clean import clean_yf_long
from src.etl.shocks.yfinance.build_monthly import build_and_resample_yf

from src.common.storage.base import Storage
from src.common.storage.factory import get_storage
from src.common.storage import paths


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

    build_monthly_shocks(storage)


if __name__ == "__main__":
    main()