← [Back to Docs](../README.md)

# Execution Lifecycle

This document describes the stage order and flow of the macro nowcasting platform. 

---

## 1. Stage Overview

The platform follows a five stage execution lifecycle:

```
Prepare → Train → Track → Select → Serve
```

Each stage produces artifacts consumed by the next stage. Stages are isolated and communicate only through persisted outputs.

---

## 2. Flow Model
- Prepare: data → datasets
- Train: datasets → model candidates
- Track: model candidates → tracked candidates
- Select: tracked candidates → chosen models
- Serve: chosen models → predictions

---

## 3. Stage Contracts

- [Prepare](docs/contracts/prepare.md) transforms raw external data into versioned, modeling-ready datasets
- [Train](docs/contracts/train.md) trains candidate statistical or machine learning models on prepared datasets
- [Track](docs/contracts/track.md) records run metadata, metrics, artifacts, and lineage
- [Select](docs/contracts/select.md) compares trained candidates and records which models are chosen for inference
- [Serve](docs/contracts/serve.md) loads chosen models and generates predictions at runtime