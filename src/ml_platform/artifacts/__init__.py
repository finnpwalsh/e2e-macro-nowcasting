"""
Artifact contract layer.

Defines:
    - Immutable run-scoped artifact keys (TrainArtifacts, EvalArtifacts)
    - Mutable lifecycle pointers (ModelPointers)
"""
from .keys import TrainArtifacts, EvalArtifacts
from .pointers import ModelPointers
from .ids import run_id

__all__ = [
    "TrainArtifacts",
    "EvalArtifacts",
    "ModelPointers",
    "run_id",
]