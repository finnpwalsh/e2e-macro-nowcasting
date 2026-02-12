"""
Prepare job: cross-domain assembly of anchor and shock datasets.

Lifecycle stage:
    Prepare

Responsibilities:
    - Read processed anchor and shock feature datasets
    - Align datasets on a common time index and schema
    - Assemble a single, model-ready supervised table (features + target)

Inputs:
    - Canonical anchors dataset (clean long format)
    - Canonical shocks dataset (clean long format)

Outputs:
    - Model-ready assembled dataset consumed by downstream training jobs

Out of scope:
    - Feature engineering specific to individual sources
    - Model training, evaluation, or experiment tracking
    - Feature selection based on model performance
    - Generation or consumption of model artifacts

Notes:
    This job performs cross-source integration only. All source-specific 
    ingestion and feature construction must occur upstream in domain 
    preparation jobs.
"""
from __future__ import annotations

from dotenv import load_dotenv

from ml_platform.storage.base import Storage
from ml_platform.storage.factory import get_storage
from macro_nowcast.storage.datasets import DATASETS

from macro_nowcast.prepare.assemble.merge_monthly import build_merged


def assemble(storage: Storage) -> None:
    """Assemble processed anchor and shock features into a unified training dataset."""
    anchors_in_key = DATASETS.canonical.anchors
    shocks_in_key = DATASETS.canonical.shocks
    out_key = DATASETS.model_ready.assembled

    anchors = storage.read_parquet(key=anchors_in_key)
    shocks = storage.read_parquet(key=shocks_in_key)

    df = build_merged(fred=anchors, yf=shocks)

    storage.write_parquet(df, out_key)

    print(f"[OK] wrote {len(df)} rows -> {out_key}")


def main() -> None:
    """Execute cross-domain dataset assembly using configured storage."""
    load_dotenv()
    storage = get_storage()
    assemble(storage)


if __name__ == "__main__":
    main()