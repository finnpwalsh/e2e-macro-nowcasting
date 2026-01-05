"""
Assemble model-ready monthly dataset from processed anchor and shock features.

This script reads the canonical processed feature tables (anchors + shocks),
performs monthly alignment/merging, and writes a single model-ready dataset
for downstream training.

RESPONSIBILITIES:
- Read processed anchor wide table from storage
- Read processed shock monthly feature table from storage
- Call assembly logic in `src.etl.assemble.*` to build the merged dataset
- Write the model-ready merged dataset back to storage
- Print a clear success message on completion

OUTPUTS:
- `paths.processed_merged()` (e.g., data/processed/merged.parquet)

NOTES:
- In V1, anchors are typically monthly macro series and shocks are monthly
  aggregated market features.
- Future versions may add additional assembly targets (e.g., intraday fusion)
  while keeping this entrypoint stable.
"""
from __future__ import annotations

from dotenv import load_dotenv

from src.etl.assemble.merge_monthly import build_merged

from src.common.storage.factory import get_storage
from src.common.storage import paths


def main() -> None:
    # load env
    load_dotenv()
    storage = get_storage()

    # resolve I/O paths
    anchors_in_key = paths.processed_fred_wide()
    anchors_in_key = paths.processed_yfinance_features()
    out_key = paths.processed_merged()

    # read infiles
    anchors = storage.read_parquet(anchors_in_key)
    shocks = storage.read_parquet(anchors_in_key)

    # merge
    df = build_merged(fred=anchors, yf=shocks)

    # write merged DataFrame to storage
    storage.write_parquet(df, out_key)

    # confirm
    print(f"[OK] wrote {len(df)} rows -> {out_key}")

if __name__ == "__main__":
    main()