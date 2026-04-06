from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class RunKeys:
    run_family: str
    run_id: str
    root: str = "artifacts/runs"

    @property
    def dir(self) -> str:
        return f"{self.root}/{self.run_family}/{self.run_id}"
    
    @property
    def manifest(self) -> str:
        return f"{self.dir}/manifest.json"
    
    @property
    def summary(self) -> str:
        return f"{self.dir}/summary.json"


@dataclass(frozen=True)
class ModelKeys:
    run_family: str
    run_id: str
    root: str = "artifacts/models"

    @property
    def dir(self) -> str:
        return f"{self.root}/{self.run_family}/{self.run_id}"
    
    @property
    def model(self) -> str:
        return f"{self.dir}/model.joblib"
    

@dataclass(frozen=True)
class DatasetKeys:
    run_family: str
    run_id: str
    root: str = "artifacts/datasets"

    @property
    def dir(self) -> str:
        return f"{self.root}/{self.run_family}/{self.run_id}"
    
    @property
    def predictions(self) -> str:
        return f"{self.dir}/predictions.parquet"
    
    @property
    def residuals(self) -> str:
        return f"{self.dir}/residuals.parquet"


@dataclass(frozen=True)
class PointerKeys:
    run_family: str
    root: str = "artifacts/pointers"

    @property
    def latest(self) -> str:
        return f"{self.root}/{self.run_family}/latest.json"
    
    @property
    def champion(self) -> str:
        return f"{self.root}/{self.run_family}/champion.json"


# ---------------------
# Wrapper
# ---------------------

@dataclass(frozen=True)
class Keys:
    run_family: str
    run_id: str

    @property
    def run(self) -> RunKeys:
        return RunKeys(self.run_family, self.run_id)
    
    @property
    def models(self) -> ModelKeys:
        return ModelKeys(self.run_family, self.run_id)
    
    @property
    def datasets(self) -> DatasetKeys:
        return DatasetKeys(self.run_family, self.run_id)
    
    @property
    def pointers(self) -> PointerKeys:
        return PointerKeys(self.run_family)