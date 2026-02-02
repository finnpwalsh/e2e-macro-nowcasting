← [Back to Lifecycle](../README.md)

# Train

This document defines the responsibilities and outputs of the Train stage in the price nowcsting execution lifecycle.

> Find boundaries [here](../contracts/train.md)

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