← [Back to Source](../README.md)

# Macro Nowcast

Domain-specific logic for the macro nowcasting system.

This package contains modeling semantics and economic logic. It defines what is being modeled, not how infrastructure operates.

---

## Responsibilities

This package contains semantics only:

- Define domain concepts (anchors vs. shocks, features vs. targets)
- Define datase meaning (raw → canonical → training)
- Implement feature construction and model training logic
- Define evaluation metrics and model quality criteria
- Compose final nowcast outputs

It does not contain:

- Storage backends or artifact layout mechanics
- Run ID or pointer management
- Experiment tracking infrastructure
- Model registry logic
- Workflow orchestration or job entrypoints
- Container or deployment configuration

---

## Layout

```
macro_nowcast/
    storage/
    evaluate/
    prepare/
    train/
    serve/ (future)
```