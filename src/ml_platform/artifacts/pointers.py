from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class ModelPointers:
    model_name: str
    root: str = "artifacts/models"

    @property
    def latest(self) -> str:
        return f"{self.root}/{self.model_name}/latest.json"
    
    @property
    def champion(self) -> str:
        return f"{self.root}/{self.model_name}/champion.json"