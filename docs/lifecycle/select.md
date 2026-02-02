← [Back to Lifecycle](../README.md)

# Select (future)

This document defines the Select stage in the price nowcasting execution lifecycle.

> Find boundaries [here](../contracts/select.md)

**Responsibilities**
- Consume logged run metadata and references to trained model artifacts
- Compare model performance across models and runs
- Choose models to be used for inference
- Record which models are chosen and preserve selection history

**Execution**
- Implemented as selection jobs under `jobs/select/`
- Core logic lives in `src/price_nowcasting/select/`
- May integrate with external tracking or metadata systems (e.g., MLflow)

**Outputs**
- Recorded selection state identifying the currently chosen models