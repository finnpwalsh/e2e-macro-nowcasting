"""
Clean raw yfinance data.

Ingest long-form raw yfinance parquet, clean and pivot, and write
cleaned long- and wide-form yfinance DataFrames to data/processed.

RESPONSIBILITIES:
- confirm inpath exists
- ingest raw long-form yfinance parquet as DataFrame
- pivot and clean raw long-form yfinance DataFrame
- write cleaned wide-form yfinance DataFrame to data/processed
- confirm task ran successfully

OUTPUTS:
- data/processed/yf_features.parquet
"""
from __future__ import annotations

from src.pipelines.yfinance import prep_yf
from src.storage.factory import get_storage
from src.storage.paths import raw_yfinance_all, processed_yfinance_features

def main() -> None:
    # load env
    storage = get_storage()
    
    # read infile
    in_key = raw_yfinance_all()
    df_raw = storage.read_parquet(key=in_key)
    
    # clean
    df_feat = prep_yf(df_raw)

    # write cleaned wide-form feature DataFrame to storage
    out_key = processed_yfinance_features()
    storage.write_parquet(df=df_feat, key=out_key)

    # confirm
    print(f"[OK] wrote df_feat shape={df_feat.shape} -> {out_key}")


if __name__ == "__main__":
    main()