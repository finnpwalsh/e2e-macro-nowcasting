← [Back to Source](../README.md)

# ML PLatform

Reusable, domain-agnostic primitives for building and operating ML systems.

---

## Responsibilities

This package contains mechanics only:
- how data and artifacts are stored
- how runs, metrics, and models are tracked
- how models are loaded and validated for serving

It does not contain:
- domain concepts (datasets, features, targets)
- model training or evaluation logic
- workflow orchestration or job entrypoints

---

## Layout

```
ml_platform/
  storage/
  tracking/
  serving/ (future)
```

> See [`storage/`](./storage/README.md) for details on shared storage abstractions.