← [Back to Docs](../README.md)

# Lifecycle

This document describes the end-to-end lifecycle of the nowcasting system.

---

## Lifecycle Overview

The nowcasting pipeline is composed of the following stages:

```
ETL → Training → Tracking → Serving
```

Each lifecycle stage:
- has a single responsibility
- executes in its own environment
- has its own set of dependencies
- produces observable and versionable outputs

---

## Lifecycle Stages

### ETL

Transforms raw external data into datasets suitable for modeling.

**Scope**
- Ingestion from external sources
- Cleaning, normalization, and feature construction

**Artifacts**
- Produces modeling-ready datasets

---

### Training

Trains statistical or machine learning models on prepared data.

**Scope**
- Model specification and training
- Feature transformations per modeling needs

**Artifacts**
- Produces model artifacts and predictions

**Boundary**
- Does not perform experiment tracking

---

### Tracking

Records, compares, and reasons about model behavior.

**Scope**
- Metric computation
- Artifact versioning
- Experiment comparison and selection

**Boundary**
- Does not influence training logic

---

### Serving

Makes trained models available for inference.

**Scope**
- Loading approved model artifacts
- Producing predictions in response to new inputs
- Enforcing interface and performance guarantees