from __future__ import annotations

from dataclasses import dataclass

from ml_platform.platform.runs import RunKeys


@dataclass
class TrainingRunKeys(RunKeys):
    run_keys: RunKeys
    
    @property
    def model(self) -> str:
        return self.run_keys.artifact("model.joblib")
    
    @property
    def predictions(self) -> str:
        return self.run_keys.artifact("predictions.parquet")
