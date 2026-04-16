from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DataArtifacts:
    """
    Domain-scoped, run-versioned derived data products
    produced during Train that improve reproducibility
    and debugging. 

    Layout:
        artifacts/data/storage/<stage>/<run_id>/...
    """
    stage: str
    run_id: str
    root: str = "artifacts/data"

    @property
    def dir(self) -> str:
        return f"{self.root}/{self.stage}/{self.run_id}"
    
    @property
    def residuals(self) -> str:
        return f"{self.dir}/residuals.parquet"
    
    @property
    def corrector_training(self) -> str:
        return f"{self.dir}/training.parquet"