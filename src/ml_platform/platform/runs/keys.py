from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class RunKeys:
    run_family: str
    run_id: str
    runs_root: str = "artifacts/runs"

    @property
    def run_dir(self) -> str:
        return f"{self.runs_root}/{self.run_family}/{self.run_id}"
    
    @property
    def manifest(self) -> str:
        return f"{self.run_dir}/manifest.json"
    
    @property
    def summary(self) -> str:
        return f"{self.run_dir}/summary.json"
    
    @property
    def artifacts_dir(self) -> str:
        return f"{self.run_dir}/artifacts"
    
    def artifact(self, name: str) -> str:
        return f"{self.artifacts_dir}/{name}"


@dataclass(frozen=True)
class PointerKeys:
    run_family: str
    pointer_root: str = "artifacts/pointers"

    @property
    def family_dir(self) -> str:
        return f"{self.pointer_root}/{self.run_family}"
    
    def pointer(self, slot: str) -> str:
        return f"{self.family_dir}/{slot}.json"