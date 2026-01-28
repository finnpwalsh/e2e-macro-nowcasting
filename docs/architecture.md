← [Back to Docs](../README.md)

# Architecture

This document describes the architectural boundaries of the nowcasting system.

---

## Execution Boundary

**Principle:** Library logic (`src/`), executable lifecycle entrypoints (`jobs/`), and orchestration/coordination concerns (`orchestration/`) are kept separate.

**Layers**
- `src/`: the core logic of the system
- `jobs/`: lifecycle entrypoints that orchestrate logic from `src/`
- `orchestration/`: worflow definitions that schedule and coordinate multiple jobs over time

**Guarantees**
- `src/` never depends on `jobs/` or `orchestration/`
- `jobs/` may depend on `src/` but not on `orchestration/`
- `orchestration/` coordinates `jobs/` without inspecting `src/`

---

## Lifecycle Boundary

**Principle:** System is organized by lifecycle stage rather than by tooling.

Responsibilities are separated across data preparation, training, tracking, and serving.

---

## Isolation Model

**Principle:** Each lifecycle stage operates in an isolated execution context.

Depencies, runtime concerns, and execution details are scoped to the stage that needs them.

---

## Artifact Boundary

**Principle**: Lifecycle stages communicate exclusively through explicit artifacts.

Artifacts represent the only contract between stages.