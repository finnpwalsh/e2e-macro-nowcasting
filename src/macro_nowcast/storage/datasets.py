"""
Canonical dataset keys for the macro_nowcast domain.

Layering Rules:

Raw:
    - Full upstream snapshots
    - May reference external providers

Canonical:
    - Source-specific cleaned datasets
    - Validated against domain contract
    - NOT merged across sources
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
        return f"{self.root}/anchors/anchors.parquet"
    
    @property
    def anchors_fred(self) -> str:
        return f"{self.root}/anchors/fred.parquet"
    
    @property
    def shocks(self) -> str:
        return f"{self.root}/shocks/shocks.parquet"
    
    @property
    def shocks_tiingo(self) -> str:
        return f"{self.root}/shocks/tiingo.parquet"
    
    @property
    def targets(self) -> str:
        return f"{self.root}/targets/target.parquet"


@dataclass(frozen=True)
class ModelReadyDatasets:
    root: str = "data/model_ready"

    @property
    def anchors_table(self) -> str:
        return f"{self.root}/anchors_table.parquet"
    
    @property
    def shocks_table(self) -> str:
        return f"{self.root}/shocks_table.parquet"


@dataclass(frozen=True)
class Datasets:
    raw: RawDatasets = RawDatasets()
    canonical: CanonicalDatasets = CanonicalDatasets()
    model_ready: ModelReadyDatasets = ModelReadyDatasets()


DATASETS = Datasets()