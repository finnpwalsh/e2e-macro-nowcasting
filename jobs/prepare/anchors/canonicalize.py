"""
Prepare: canonicalize anchors (clean long format).

Lifecycle stage:
    Prepare

Reads:
    - DATASETS.raw.fred_snapshot
Writes:
    - DATASETS.canonical.anchors
"""
from __future__ import annotations

from dotenv import load_dotenv

from ml_platform.storage.base import Storage
from ml_platform.storage.factory import get_storage
from macro_nowcast.storage.datasets import DATASETS

from macro_nowcast.prepare.anchors.fred.clean import clean_fred_long


def run(storage: Storage) -> None:
    in_key = DATASETS.raw.fred_snapshot
    out_key = DATASETS.canonical.anchors

    df_raw = storage.read_parquet(key=in_key)
    df_clean = clean_fred_long(df_raw)

    storage.write_parquet(df=df_clean, key=out_key, index=False)
    print(f"[OK] wrote shape={df_clean.shape} -> {out_key}")


def main() -> None:
    load_dotenv()
    storage = get_storage()
    run(storage)


if __name__ == "__main__":
    main()