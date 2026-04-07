from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar, Mapping

from .identity import RunIdentity

TSpec = TypeVar("TSpec")
TOutputs = TypeVar("TOutputs")
TSummary = TypeVar("TSummary")


@dataclass(frozen=True)
class RunRefs:
    refs: Mapping[str, str]


@dataclass(frozen=True)
class RunSummary(Generic[TSpec, TSummary]):
    run_identity: RunIdentity
    refs: RunRefs
    summary: TSummary


@dataclass(frozen=True)
class RunManifest(Generic[TSpec, TOutputs]):
    run_identity: RunIdentity
    refs: RunRefs
    spec: TSpec
    outputs: TOutputs