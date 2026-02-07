from __future__ import annotations

import pandas as pd

from dotenv import load_dotenv

from ml_platform.storage.base import Storage
from ml_platform.storage import paths
from ml_platform.storage.factory import get_storage

from price_nowcast.prepare.shocks.yfinance.ingest import ingest_yf_series
from price_nowcast.prepare.shocks.yfinance.clean import clean_yf_long
from price_nowcast.prepare.shocks.yfinance.build_monthly import build_and_resample_yf

from price_nowcast.prepare.shocks.yfinance.schema import YF_TICKERS


def ingest(storage: Storage) -> None:
    out_key = paths.raw_yfinance_all()

    dfs = []
    for ticker in YF_TICKERS:
        df = ingest_yf_series(ticker=ticker)
        dfs.append(df)
    
    combined = pd.concat(dfs, ignore_index=True)
    
    storage.write_parquet(df=combined, key=out_key, index=False)

    print(f"[OK] wrote {combined.shape} -> {out_key}")
    print(f"[OK] shocks ingestion complete.")


def prepare(storage: Storage) -> None:
    in_key = paths.raw_yfinance_all()
    out_key = paths.processed_yfinance_features()

    df_raw = storage.read_parquet(key=in_key)
    
    df_clean = clean_yf_long(df_raw)
    df_feat = build_and_resample_yf(df_clean)

    storage.write_parquet(df=df_feat, key=out_key)

    print(f"[OK] wrote shape={df_feat.shape} -> {out_key}")
    print(f"[OK] shock preparation complete.")


def main() -> None:
    load_dotenv()
    storage = get_storage()

    ingest(storage)
    prepare(storage)


if __name__ == "__main__":
    main()