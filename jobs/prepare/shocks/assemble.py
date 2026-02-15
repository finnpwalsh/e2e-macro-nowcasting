"""
Prepare: assemble and validate canonical shocks.

Lifecycle stage:
    Prepare

Writes:
    - DATASETS.canonical.shocks
"""
from __future__ import annotations

from dotenv import load_dotenv

from ml_platform.storage import Storage, get_storage
from macro_nowcast.storage import DATASETS

from macro_nowcast.prepare.shocks.registry import SHOCK_SOURCES
from macro_nowcast.prepare.shocks import ShockAssembler


def run(storage: Storage) -> None:
    dfs = [
        storage.read_parquet(spec.canonical_key)
        for spec in SHOCK_SOURCES.values()
    ]

    assembler = ShockAssembler()
    assembled = assembler.assemble(dfs)

    storage.write_parquet(df=assembled, key=DATASETS.canonical.shocks)

    INDENT = "    "
    SUB = INDENT * 2
    print(f"\n[PREPARE][SHOCKS][ASSEMBLE] Complete")
    print(f"{INDENT}Canonical")
    print(f"{SUB}Key:       {DATASETS.canonical.shocks}")
    print(f"{SUB}Shape:     {assembled.shape}")


def main() -> None:
    load_dotenv()
    storage = get_storage()
    run(storage)

if __name__ == "__main__":
    main()