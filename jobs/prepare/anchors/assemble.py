"""
Prepare: assemble and validate canonical anchors.

Lifecycle stage:
    Prepare

Writes:
    - DATASETS.canonical.anchors
"""
from __future__ import annotations

from dotenv import load_dotenv

from ml_platform.storage import Storage, get_storage
from macro_nowcast.storage import DATASETS

from macro_nowcast.prepare.anchors.registry import ANCHOR_SOURCES
from macro_nowcast.prepare.anchors import AnchorAssembler


def run(storage: Storage) -> None:
    dfs = [
        storage.read_parquet(spec.canonical_key)
        for spec in ANCHOR_SOURCES.values()
    ]

    assembler = AnchorAssembler()
    assembled = assembler.assemble(dfs)

    storage.write_parquet(df=assembled, key=DATASETS.canonical.anchors)

    INDENT = "    "
    SUB = INDENT * 2
    print(f"\n[PREPARE][ANCHORS][ASSEMBLE] Complete")
    print(f"{INDENT}Canonical")
    print(f"{SUB}Key:       {DATASETS.canonical.anchors}")
    print(f"{SUB}Shape:     {assembled.shape}")


def main() -> None:
    load_dotenv()
    storage = get_storage()
    run(storage)

if __name__ == "__main__":
    main()