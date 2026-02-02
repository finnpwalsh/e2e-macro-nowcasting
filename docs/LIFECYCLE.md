← [Back to Docs](../README.md)

# Lifecycle

This document describes the end-to-end execution lifecycle of the price nowcasting system.

The lifecycle defines what runs, in what order, and with what responsibility. 

---

## Lifecycle Overview

The price nowcasting pipeline is composed of the following sequence of explicit lifecycle stages:

```
Prepare → Train → Select → Serve
```

Each lifecycle stage:
- has a single responsibility
- executes via a dedicated job entrypoint
- runs in its own isolated execution context
- produces explicit outputs consumed by downstream stages

Stages communicate only through persisted outputs; no stage sees or reuses another stage's internal logic.

**Flow Model**
- Prepare: data → datasets
- Train: datasets → model candidates
- Select: model candidates → chosen models
- Serve: chosen models → predictions

---

## Lifecycle Stages

### Prepare

Transforms raw external data into modeling-ready datasets.

**Responsibilities**
- Ingest data from external sources
- Clean, normalize, and align time series
- Construct features required for downstream modeling

**Execution**
- Implemented as preparation jobs under `jobs/prepare/`
- Core logic lives in `src/prepare/`

**Outputs**
- Versioned datasets suitable for training

---

### Train

Trains statistical or machine learning models on prepared datasets.

**Responsibilities**
- Specify models and transform features
- Fit models to the transformed features
- Compute run-scoped evaluation outputs

**Execution**
- Implemented as training jobs under `jobs/train/`
- Core logic lives in `src/train/`

**Outputs**
- Canonical model artifacts
- Run-scoped evaluation outputs

---

### Select

Evaluates trained models and determines which will be used for prediction.

**Responsibilities**
- Log run metadata and references to trained model artifacts
- Compare model performance across models and runs
- Choose models to be used for inference
- Record which models are chosen and preserve selection history

**Execution**
- Implemented as selection jobs under `jobs/select/`
- Core logic lives in `src/select/`
- May integrate with external tracking or metadata systems (e.g., MLflow)

**Outputs**
- Recorded selection state identifying the currently chosen models

---

### Serve (future)

Uses the currently chosen models to generate predictions.

**Responsibilities**
- Load chosen model artifacts
- Produce predictions in response to new inputs
- Enforce interface, latency, and availability guarantees