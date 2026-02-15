"""
Prepare: build model-ready anchor features.

Lifecycle stage:
    Prepare

Writes:
    - DATASETS.model_ready.anchors_table
"""
from __future__ import annotations

from dotenv import load_dotenv

from ml_platform.storage import Storage, get_storage
from macro_nowcast.storage import DATASETS

from macro_nowcast.prepare.anchors import AnchorFeatureBuilder


def run(storage: Storage) -> None:
    canon = storage.read_parquet(DATASETS.canonical.anchors)
    
    builder = AnchorFeatureBuilder()
    table = builder.build(canon)

    storage.write_parquet(df=table, key=DATASETS.model_ready.anchors_table)

    INDENT = "    "
    SUB = INDENT * 2
    print(f"\n[PREPARE][ANCHORS][FEATURES] Complete")
    print(f"{INDENT}Model-Ready")
    print(f"{SUB}Key:       {DATASETS.model_ready.anchors_table}")
    print(f"{SUB}Shape:     {table.shape}")


def main() -> None:
    load_dotenv()
    storage = get_storage()
    run(storage)

if __name__ == "__main__":
    main()