"""
Clean raw FRED data.

Ingest raw long-form FRED data parquet, clean and pivot, and
write wide-form DataFrame to data/processed.

RESPONSIBILITIES:
- ingest raw FRED series
- call prep_fred
- write wide-form DataFrame to data/processed/ as parquet
- confirm task ran successfully

OUTPUTS:
- data/processed/fred_wide.parquet
"""
from __future__ import annotations

from src.pipelines.fred import prep_fred
from src.storage.factory import get_storage
from src.storage.paths import raw_fred_all, processed_fred_wide

def main() -> None:
    # load env
    storage = get_storage()
    
    # read infile
    in_key = raw_fred_all()
    df_raw = storage.read_parquet(key=in_key)
    
    # clean
    df_wide = prep_fred(df_raw)

    # write cleaned wide-form DataFrame to storage
    out_key = processed_fred_wide()
    storage.write_parquet(df=df_wide, key=out_key, index=False)

    # confirm task was successful
    print(f"[OK] wrote df_wide shape={df_wide.shape} -> {out_key}")


if __name__ == "__main__":
    main()