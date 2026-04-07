from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class RunKeys:
    run_family: str
    run_id: str
    runs_root: str = "artifacts/runs"

    @property
    def run_dir(self) -> str:
        return f"{self.root}/{self.run_family}/{self.run_id}"
    
    @property
    def manifest(self) -> str:
        return f"{self.run_dir}/manifest.json"
    
    @property
    def summary(self) -> str:
        return f"{self.run_dir}/summary.json"


@dataclass(frozen=True)
class PointerKeys:
    run_family: str
    pointer_root: str = "artifacts/pointers"

    def __call__(self, slot: str) -> str:
        return f"{self.pointer_root}/{self.run_family}/{slot}.json"