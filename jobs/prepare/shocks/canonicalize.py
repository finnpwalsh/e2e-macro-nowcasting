"""
Prepare: canonicalize shocks (clean long format).

Lifecycle stage: 
    Prepare

Reads:
    - DATASETS.raw.yfinance_snapshot

Writes:
    - DATASETS.canonical.shocks
"""
from __future__ import annotations

from dotenv import load_dotenv

from ml_platform.storage import Storage, get_storage
from macro_nowcast.storage.datasets import DATASETS

from macro_nowcast.prepare.shocks.yfinance.clean import clean_yf_long


def run(storage: Storage) -> None:
    """Clean and normalize shocks into a the canonical long-format shocks dataset."""
    in_key = DATASETS.raw.yfinance_snapshot
    out_key = DATASETS.canonical.shocks

    df_raw = storage.read_parquet(key=in_key)
    
    df_clean = clean_yf_long(df_raw)

    storage.write_parquet(df=df_clean, key=out_key)

    INDENT = "    "
    print(f"\n[PREPARE][SHOCKS][CANONICALIZE] Complete")
    print(f"{INDENT}output_key:   {out_key}")
    print(f"{INDENT}shape:        {df_clean.shape}")


def main() -> None:
    """Execute shock ingestion and preparation using configured storage."""
    load_dotenv()
    storage = get_storage()
    run(storage)


if __name__ == "__main__":
    main()