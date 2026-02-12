"""
Prepare job: cross-domain assembly of anchor and shock datasets.

Lifecycle stage:
    Prepare

Reads:
    - DATASETS.canonical.anchors
    - DATASETS.canonical.shocks

Writes:
    - DATASETS.model_ready.assembled
"""
from __future__ import annotations

from dotenv import load_dotenv

from ml_platform.storage.base import Storage
from ml_platform.storage.factory import get_storage
from macro_nowcast.storage.datasets import DATASETS

from macro_nowcast.prepare.assemble.merge_monthly import build_merged


def run(storage: Storage) -> None:
    anchors_in_key = DATASETS.canonical.anchors
    shocks_in_key = DATASETS.canonical.shocks
    out_key = DATASETS.model_ready.assembled

    anchors = storage.read_parquet(key=anchors_in_key)
    shocks = storage.read_parquet(key=shocks_in_key)

    df = build_merged(fred=anchors, yf=shocks)

    storage.write_parquet(df, out_key)

    print(f"[OK] wrote {len(df)} rows -> {out_key}")


def main() -> None:
    load_dotenv()
    storage = get_storage()
    run(storage)


if __name__ == "__main__":
    main()