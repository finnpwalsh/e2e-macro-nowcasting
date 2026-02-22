← [Back to Contracts](../README.md)

# Train

This document defines the responsibilities and outputs of the Train stage in the price nowcsting execution lifecycle.

**Responsibilities**
- Specify models and transform features
- Fit models to the transformed features
- Compute run-scoped evaluation outputs

**Execution**
- Implemented as training jobs under `jobs/train/`
- Core logic lives in `src/price_nowcasting/train/`

**Outputs**
- Canonical model artifacts
- Run-scoped evaluation outputs