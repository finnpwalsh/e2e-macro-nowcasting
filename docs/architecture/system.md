← [Back to Docs](../README.md)

# System Architecture

This document defines the structural architecture of the macro nowcasting platform.

---

## Separation of concerns

The system is designed around separation of concerns:
- prepare, train, select, and serve are distinct
- domain logic and platform infrastructure are distinct
- library code, execution, and orchestration are distinct
- anchors and shocks are distinct

---

## Package structure

The repository is divided into two primary packages:

---

`macro_nowcast/` – domain layer

Contains:
- Anchor and shock ingestion logic
- Canonicalization and validation
- Model-ready dataset assembly
- Baseline and shock model training logic
- Domain contracts

---

`ml_platform/` – platform layer

Contains:
- Storage abstraction
- Artifact path definitions
- MLflow tracking utilities
- Selection logic

This package is domain-agnostic and reusable.

---

## Modeling Architecture

Two-model system:

1. Baseline
- Trained on anchor features
- Produces baseline estimate
- Outputs residuals (v1.4.2)

2. Shock Corrector
- Trained on residual signal
- Produces correction term

---

Final nowcast:
```
Nowcast = Baseline + ShockCorrection
```