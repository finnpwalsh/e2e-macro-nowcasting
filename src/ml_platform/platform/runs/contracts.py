from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

from .identity import RunIdentity


TRefs = TypeVar("TRefs")
TSpec = TypeVar("TSpec")
TOutputs = TypeVar("TOutputs")
TSummary = TypeVar("TSummary")


@dataclass(frozen=True)
class RunSummary(Generic[TRefs, TSummary]):
    run_identity: RunIdentity
    refs: TRefs
    summary: TSummary


@dataclass(frozen=True)
class RunManifest(Generic[TRefs, TSpec, TOutputs]):
    run_identity: RunIdentity
    refs: TRefs
    spec: TSpec
    outputs: TOutputs