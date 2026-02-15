"""
Prepare: ingest and canonicalize raw Tiingo shock series.

Lifecycle stage:
    Prepare

Writes:
    - DATASETS.raw.tiingo_snapshot
    - DATASETS.canonical.shocks_tiingo
"""
from __future__ import annotations

import os

from dotenv import load_dotenv

from ml_platform.storage import Storage, get_storage
from macro_nowcast.storage import DATASETS

from macro_nowcast.externals.clients.tiingo import TiingoClient
from macro_nowcast.externals.providers.tiingo import TiingoProvider
from macro_nowcast.prepare.shocks.registry import SHOCK_SOURCES
from macro_nowcast.specs.tiingo import TICKERS


START_DATE = "2010-01-01"


def run(storage: Storage) -> None:
    """Ingest raw Tiingo shock series and persist both raw and canonical datasets."""
    api_key = os.getenv("TIINGO_API_KEY") 
    if not api_key:
        raise RuntimeError("Missing TIINGO_API_KEY. Add it to .env")
    
    client = TiingoClient(api_key=api_key)
    provider = TiingoProvider(client)
    canonicalizer = SHOCK_SOURCES["tiingo"].canonicalizer()

    raw = provider.fetch(tickers=TICKERS, start_date=START_DATE)
    storage.write_parquet(df=raw, key=DATASETS.raw.tiingo_snapshot, index=False)

    canon = canonicalizer.canonicalize(raw=raw)
    storage.write_parquet(df=canon, key=DATASETS.canonical.shocks_tiingo)


    INDENT = "    "
    SUB = INDENT * 2
    print(f"\n[PREPARE][SHOCKS][TIINGO] Complete")
    print(f"{INDENT}Raw")
    print(f"{SUB}Key:       {DATASETS.raw.tiingo_snapshot}")
    print(f"{SUB}Shape:     {raw.shape}")
    print(f"{INDENT}Canonical")
    print(f"{SUB}Key:       {DATASETS.canonical.shocks_tiingo}")
    print(f"{SUB}Shape:     {raw.shape}")


def main() -> None:
    load_dotenv()
    storage = get_storage()
    run(storage)


if __name__ == "__main__":
    main()