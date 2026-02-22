"""
Canonical dataset keys for the macro_nowcast domain.

Layering Rules:

Raw:
    - Full upstream snapshots
    - May reference external providers

Canonical:
    - Validated against domain contract
    - NOT modeling tables

ModelReady:
    - Modeling tables only
    - Anchors and shocks separated
    - No source semantics
"""
from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class RawDatasets:
    root: str = "data/raw"

    @property
    def fred_snapshot(self) -> str:
        return f"{self.root}/fred/snapshot.parquet"
    
    @property
    def tiingo_snapshot(self) -> str:
        return f"{self.root}/tiingo/snapshot.parquet"
    

@dataclass(frozen=True)
class CanonicalDatasets:
    root: str = "data/canonical"

    @property
    def anchors(self) -> str:
        return f"{self.root}/anchors/all.parquet"
    
    @property
    def anchors_fred(self) -> str:
        return f"{self.root}/anchors/fred.parquet"
    
    @property
    def shocks(self) -> str:
        return f"{self.root}/shocks/all.parquet"
    
    @property
    def shocks_tiingo(self) -> str:
        return f"{self.root}/shocks/tiingo.parquet"


@dataclass(frozen=True)
class ModelReadyDatasets:
    root: str = "data/model_ready"

    @property
    def anchors(self) -> str:
        return f"{self.root}/anchors/table.parquet"
    
    @property
    def shocks(self) -> str:
        return f"{self.root}/shocks/table.parquet"


@dataclass(frozen=True)
class Datasets:
    raw: RawDatasets = RawDatasets()
    canonical: CanonicalDatasets = CanonicalDatasets()
    model_ready: ModelReadyDatasets = ModelReadyDatasets()


DATASETS = Datasets()