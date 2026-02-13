"""
Prepare: ingest, canonicalize, and validate FRED anchor series.

Lifecycle stage:
    Prepare

Writes:
    - DATASETS.raw.fred_snapshot
    - DATASETS.canonical.anchors
"""
from __future__ import annotations

import os

from dotenv import load_dotenv

from ml_platform.storage import Storage, get_storage
from macro_nowcast.storage.datasets import DATASETS
from macro_nowcast.prepare.anchors.fred import (
    FREDClient,
    FREDSource,
    SERIES,
)

START_DATE = "1990-01-01"


def run(storage: Storage) -> None:
    """Ingest raw FRED anchor series and persist both raw and canonical datasets."""
    api_key = os.getenv("FRED_API_KEY") 
    if not api_key:
        raise RuntimeError("Missing FRED_API_KEY. Add it to .env")
    
    client = FREDClient(api_key=api_key)
    source = FREDSource(client)

    raw = source.fetch(series=SERIES, start_date=START_DATE)
    storage.write_parquet(df=raw, key=DATASETS.raw.fred_snapshot, index=False)

    canon = source.canonicalize(df=raw)
    valid = source.validate(df=canon)
    storage.write_parquet(df=valid, key=DATASETS.canonical.anchors)


    INDENT = "    "
    SUB = INDENT * 2
    print(f"\n[PREPARE][ANCHORS][FRED] Complete")
    print(f"{INDENT}Raw")
    print(f"{SUB}Key:       {DATASETS.raw.fred_snapshot}")
    print(f"{SUB}Shape:     {raw.shape}")
    print(f"{INDENT}Canonical")
    print(f"{SUB}Key:       {DATASETS.canonical.anchors}")
    print(f"{SUB}Shape:     {raw.shape}")


def main() -> None:
    load_dotenv()
    storage = get_storage()
    run(storage)


if __name__ == "__main__":
    main()