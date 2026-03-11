← [Back to Docs](../README.md)

# Execution Lifecycle

This document describes the stage order and flow of the macro nowcasting platform. 

---

## Stage Overview

The platform follows a four stage execution lifecycle:

```
Prepare → Train → Select → Serve
```

Each stage produces artifacts consumed by the next stage. Stages are isolated and communicate only through persisted outputs.

---

## Flow Model
- prepare: data → datasets
- train: datasets → model candidate
- select: model candidate → champion model
- serve: champion model → predictions

---

## Stage Definitions

| Stage | Definition |
| ----- | ---------- |
| **Prepare** | transforms raw external data into versioned, modeling-ready datasets |
| **Train** | trains candidate statistical or machine learning models on prepared datasets |
| **Select** | compares trained candidates and chooses model for inference |
| **Serve** | loads chosen models and generates predictions at runtime |