"""
Prepare: ingest, canonicalize, and validate yfinance shock series.

Lifecycle stage:
    Prepare

Writes:
    - DATASETS.raw.yfinance_snapshot
    - DATASETS.canonical.shocks
"""
from __future__ import annotations

import os

from dotenv import load_dotenv

from ml_platform.storage import Storage, get_storage
from macro_nowcast.storage.datasets import DATASETS
from macro_nowcast.prepare.shocks.yfinance import (
    YFSource,
    TICKERS,
)

START_DATE = "2010-01-01"


def run(storage: Storage) -> None:
    """Ingest raw yfinance anchor series and persist both raw and canonical datasets."""
    source = YFSource()

    raw = source.fetch(ticker=TICKERS, start_date=START_DATE)
    storage.write_parquet(df=raw, key=DATASETS.raw.yfinance_snapshot, index=False)

    canon = source.canonicalize(df=raw)
    valid = source.validate(df=canon)
    storage.write_parquet(df=valid, key=DATASETS.canonical.shocks)


    INDENT = "    "
    SUB = INDENT * 2
    print(f"\n[PREPARE][SHOCKS][YF] Complete")
    print(f"{INDENT}Raw")
    print(f"{SUB}Key:       {DATASETS.raw.yfinance_snapshot}")
    print(f"{SUB}Shape:     {raw.shape}")
    print(f"{INDENT}Canonical")
    print(f"{SUB}Key:       {DATASETS.canonical.shocks}")
    print(f"{SUB}Shape:     {raw.shape}")


def main() -> None:
    load_dotenv()
    storage = get_storage()
    run(storage)


if __name__ == "__main__":
    main()