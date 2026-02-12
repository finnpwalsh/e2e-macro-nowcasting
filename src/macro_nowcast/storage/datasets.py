"""
Canonical dataset keys for the macro_nowcast domain.

Rules:
    - Raw layer may reference upstream data sources.
    - Canonical layer must be source-agnostic and reflect modeling semantics only.
    - This module defines dataset locations only. It does not read or write data
"""
from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class RawDatasets:
    """
    Raw ingestion layer.

    These datasets represent full snapshots of upstream sources.
    They are allowed to reference external providers.
    """
    root: str = "data/raw"

    @property
    def fred_snapshot(self) -> str:
        return f"{self.root}/fred/snapshot.parquet"
    
    @property
    def yfinance_snapshot(self) -> str:
        return f"{self.root}/yfinance/snapshot.parquet"
    

@dataclass(frozen=True)
class CanonicalDatasets:
    """
    Canonical modeling datasets.

    These datasets must NOT reference data sources.
    They are divided strictly by modeling semantics:
        - anchors
        - shocks
        - assembled
    """
    root: str = "data/canonical"

    @property
    def anchors(self) -> str:
        return f"{self.root}/anchors/dataset.parquet"
    
    @property
    def shocks(self) -> str:
        return f"{self.root}/shocks/dataset.parquet"
    
    @property
    def targets(self) -> str:
        return f"{self.root}/shocks/dataset.parquet"


@dataclass(frozen=True)
class ModelReadyDatasets:
    """Model-ready supervised table (features + target)."""
    root: str = "data/model_ready"

    @property
    def assembled(self) -> str:
        return f"{self.root}/assembled.parquet"


@dataclass(frozen=True)
class Datasets:
    raw: RawDatasets = RawDatasets()
    canonical: CanonicalDatasets = CanonicalDatasets()
    model_ready: ModelReadyDatasets = ModelReadyDatasets()


DATASETS = Datasets()