← [Back to Docs](../README.md)

# Lifecycle

This document describes the end-to-end execution lifecycle of the price nowcasting system.

The lifecycle defines what runs, in what order, and with what responsibility. 

---

## Overview

The price nowcasting pipeline is composed of the following sequence of explicit lifecycle stages:

```
Prepare → Train → Track → Select → Serve
```

Each lifecycle stage:
- has a single responsibility
- executes via a dedicated job entrypoint
- runs in its own isolated execution context
- produces explicit outputs consumed by downstream stages

Stages communicate only through persisted outputs; no stage sees or reuses another stage's internal logic.

---

## Stages

- **[Prepare](./prepare.md)** transforms raw external data into versioned, modeling-ready datasets
- **[Train](./train.md)** trains candidate statistical or machine learning models on prepared datasets
- **[Track](./track.md)** records run metadata, metrics, artifacts, and lineage
- **[Select](./select.md)** compares trained candidates and records which models are chosen for inference
- **[Serve](./serve.md)** loads chosen models and generates predictions at runtime


**Flow Model**
- Prepare: data → datasets
- Train: datasets → model candidates
- Track: model candidates → tracked candidates
- Select: tracked candidates → chosen models
- Serve: chosen models → predictions