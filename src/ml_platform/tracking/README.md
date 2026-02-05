← [Back to Source](../README.md)

# Tracking

Experiment and artifact tracking.

---

## Contract

- Contains tracking-stage logic only (logging, registration, promotion, metadata)
- Consumes training outputs produced by `train/`

---

## Responsibilities

- Log metrics, params, and artifacts for completed training runs
- Register/version models and associate them with run metadata
- Maintain "latest/champion" pointers or other promotion primitives used by `serve/`