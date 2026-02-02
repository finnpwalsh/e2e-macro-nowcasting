← [Back to Docs](../README.md)

# Architecture

This document describes the architectural structure of the nowcasting system.

---

## Execution Structure

Library logic, executable lifecycle entrypoints, and orchestration/coordination concerns are separated.

**Layers**
- `src/`: the core logic of the system
- `jobs/`: lifecycle entrypoints that orchestrate logic from `src/`
- `orchestration/`: worflow definitions that schedule and coordinate multiple jobs over time

---

## Lifecycle Structure

The system is organized by lifecycle stage rather than by tooling.

Responsibilities are separated across data preparation, training, tracking, selection, and serving.

---

## Artifact Interface

Lifecycle stages interact through persisted artifacts, which serve as the interface between stages.