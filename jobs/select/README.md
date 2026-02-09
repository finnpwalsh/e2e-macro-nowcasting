← [Back to Jobs](../README.md)

# Select

Pipeline entrypoints responsible for mutating model deployment pointers based on explicit decisions.

---

## Contract

Selection jobs are executable entrypoints that:
- Read model registry state
- Mutate a single deployment pointer (e.g. registry alias)
- Perform explicit, auditable promotion actions

Selection jobs are not responsible for:
- training or retraining models
- logging metrics or artifacts
- comparing models or computing evaluation results
- defining artifact schemas or storage layout

---

## Layout

```
jobs/select/
  promote.py
```
