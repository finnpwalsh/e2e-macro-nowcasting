from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class RunKeys:
    model_name: str
    run_id: str
    root: str = "artifacts/runs"

    @property
    def dir(self) -> str:
        return f"{self.root}/{self.model_name}/{self.run_id}"
    
    @property
    def manifest(self) -> str:
        return f"{self.dir}/manifest.json"
    
    @property
    def summary(self) -> str:
        return f"{self.dir}/summary.json"


@dataclass(frozen=True)
class ModelKeys:
    model_name: str
    run_id: str
    root: str = "artifacts/models"

    @property
    def dir(self) -> str:
        return f"{self.root}/{self.model_name}/{self.run_id}"
    
    @property
    def model(self) -> str:
        return f"{self.dir}/model.joblib"
    

@dataclass(frozen=True)
class DatasetKeys:
    model_name: str
    run_id: str
    root: str = "artifacts/datasets"

    @property
    def dir(self) -> str:
        return f"{self.root}/{self.model_name}/{self.run_id}"
    
    @property
    def predictions(self) -> str:
        return f"{self.dir}/predictions.parquet"


@dataclass(frozen=True)
class PointerKeys:
    model_name: str
    root: str = "artifacts/pointers"

    @property
    def latest(self) -> str:
        return f"{self.root}/{self.model_name}/latest.json"
    
    @property
    def champion(self) -> str:
        return f"{self.root}/{self.model_name}/champion.json"


# ---------------------
# Wrapper
# ---------------------

@dataclass(frozen=True)
class Keys:
    model_name: str
    run_id: str

    @property
    def run(self) -> RunKeys:
        return RunKeys(self.model_name, self.run_id)
    
    @property
    def models(self) -> ModelKeys:
        return ModelKeys(self.model_name, self.run_id)
    
    @property
    def datasets(self) -> DatasetKeys:
        return DatasetKeys(self.model_name, self.run_id)
    
    @property
    def pointers(self) -> PointerKeys:
        return PointerKeys(self.model_name)