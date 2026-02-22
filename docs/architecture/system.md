← [Back to Docs](../README.md)

# System Architecture

This document defines the structural architecture of the macro nowcasting platform.

It describes system components, boundaries, and data movement.

> For stage sequencing, see [`architecture/lifecycle.md`](./lifecycle.md)
> For behavioral boundaries, see [`contracts/`]

---

## 1. Design Principles

The system is designed around the following principles:

- **Stage isolation** – Prepare, Train, Track, Select, and Serve are independent
- **Separation of concerns**
    - Domain logic and platform infrastructure are distinct
    - Library code, execution, and orchestration are distinct
    - Anchors and Shocks are kept separate in logic, execution, orchestration, and storage

---

## 2. Package Structure

The repository is divided into two primary packages:

### `macro_nowcast/`

Domain layer. Contains:
- Anchor and shock ingestion logic
- Canonicalization and validation
- Model-ready dataset assembly
- Baseline and shock model training logic
- Domain contracts

---

### `ml_platform/`

Platform layer. Contains:
- Storage abstraction
- Artifact path definitions
- MLflow tracking utilities
- Selection logic

This package is domain-agnostic and reusable.

---

## 3. Modeling Architecture

Two-model system:

1. Baseline
- Trained on anchor features
- Produces baseline estimate
- Outputs residuals (v1.4.2)

2. Shock Corrector
- Trained on residual signal
- Produces correction term

Final nowcast:
```
Nowcast = Baseline + ShockCorrection
```