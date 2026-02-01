← [Back to Docs](../README.md)

# Contracts

This document defines contracts for the price nowcasting system.


---

## Storage Contract

Data, artifacts, and metadata are stored in a lakehouse as follows:

```
lake/
  raw/
    anchors/
      fred/
        ...
    shocks/
      yfinance/
        ...
  
  canonical/
    anchors/
      ...
    shocks/
      ...

  curated/
    targets/
      monthly/
        ...
    features/
      monthly_anchors/
        ...
      intraday_shocks/
        ...
    training_sets/
      baseline_monthly/
        ...
      shocks_residual_monthly/
        ...
    residuals/
      baseline_monthly/
        ...
    predictions/
      baseline_monthly/
        ...
      corrected_monthly/
        ...
      

artifacts/
  models/
    baseline/
      ...
    shocks_corrector/
      ... 
  eval/
    baseline/
      ...
    corrected/
      ...


registry/
  pointers/
    datasets/
      targets_monthly/
        ...
      features_monthly_anchors/
        ...
      features_intraday_shocks/
        ...
      features_monthly_shocks/
        ...
      residuals_baseline_monthly/
        ...
      training_sets_baseline_monthly/
        ...
      training_sets_shocks_residual_monthly/
        ...
      predictions_baseline_monthly/
        ...
      predictions_corrected_monthly/
        ...
    models/
      baseline/
        ...
      shocks_corrector/
        ...


_meta/
  manifests/
    lake/
      ...
    artifacts/
      ...
  lineage/
      ...
  schemas/
    datasets/
      targets_monthly/
      features_monthly_anchors/
      features_intraday_shocks/
      residuals_baseline_monthly/
      training_sets_baseline_monthly/
      training_sets_shocks_residual_monthly/
      predictions_baseline_monthly/
      predictions_corrected_monthly/
    artifacts/
      models_baseline/
      models_shocks_corrector/
      eval_baseline/
      eval_corrected/

```

---

## Dataset Contracts

### Raw layer
- `raw_anchors_fred`
- `raw_shocks_yfinance/`

### Canonical layer
- `canonical_anchors`
- `canonical_shocks`

### Curated layer
- `targets_monthly`
- `features_monthly_anchors`
- `training_baseline_monthly`
- `residuals_baseline_monthly`
- `features_intraday_shocks`
- `features_monthly_shocks`
- `training_shocks_residual_monthly`
- `predictions_baseline_monthly`
- `predictions_corrected_monthly`

---

## Artifact Contracts

### Model layer
- `models_baseline`
- `models_shocks_corrector`

### Evaluation layer
- `eval_baseline`
- `eval_corrected`