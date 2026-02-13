from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class TrainArtifacts:
    model_name: str
    run_id: str
    root: str = "artifacts/models"

    @property
    def dir(self) -> str:
        return f"{self.root}/{self.model_name}/{self.run_id}"
    
    @property
    def model(self) -> str:
        return f"{self.dir}/model.joblib"
    
    @property
    def metrics(self) -> str:
        return f"{self.dir}/metrics.json"


@dataclass(frozen=True)
class EvalArtifacts:
    model_name: str
    run_id: str
    root: str = "artifacts/eval"

    @property
    def dir(self) -> str:
        return f"{self.root}/{self.model_name}/{self.run_id}"
    
    @property
    def predictions(self) -> str:
        return f"{self.dir}/predictions.parquet"
    
    @property
    def summary(self) -> str:
        return f"{self.dir}/summary.json"