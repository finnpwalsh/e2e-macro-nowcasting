← [Back to Lifecycle](../README.md)

# Track

This document defines the Track stage in the price nowcasting execution lifecycle.

> Find boundaries [here](../contracts/track.md)

**Responsibilities**
- Record run metadata for training and evaluation jobs
- Log metrics, parameters, and artifacts produced by models
- Maintain lineage between datasets, runs, and model artifacts
- Provide an auditable system of record for experiments and results

**Execution**
- Implemented as tracking jobs under `jobs/track/`
- Core logic lives in `src/price_nowcasting/track/`
- Integrates with external tracking or metadata systems (e.g., MLflow)

**Outputs**
- Persisted run records, metrics, and artifact references suitable for downstream selection
