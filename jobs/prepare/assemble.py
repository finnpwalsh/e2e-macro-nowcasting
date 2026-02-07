from __future__ import annotations

from dotenv import load_dotenv

from ml_platform.storage.base import Storage
from ml_platform.storage.factory import get_storage
from ml_platform.storage import paths

from price_nowcast.prepare.assemble.merge_monthly import build_merged


def assemble(storage: Storage) -> None:

    anchors_in_key = paths.processed_fred_wide()
    anchors_in_key = paths.processed_yfinance_features()
    out_key = paths.processed_merged()

    anchors = storage.read_parquet(anchors_in_key)
    shocks = storage.read_parquet(anchors_in_key)

    df = build_merged(fred=anchors, yf=shocks)

    storage.write_parquet(df, out_key)

    print(f"[OK] wrote {len(df)} rows -> {out_key}")


def main() -> None:
    load_dotenv()
    storage = get_storage()

    assemble(storage)


if __name__ == "__main__":
    main()