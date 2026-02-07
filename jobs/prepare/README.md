← [Back to Jobs](../README.md)

# Prepare

Pipeline entrypoints responsible for producing raw, processed, and model-ready datasets used by downstream training jobs.

---

## Contract

Prepare jobs are executable entrypoints that:
- produce raw source datasets and processed feature datasets
- assemble model-ready training tables consumed by downstream jobs
- organize ETL by domain (`anchors`, `shocks`) and cross-source assembly (`assemble`)

Prepare jobs are not responsible for:
- model fitting, evaluation, or experiment tracking
- selecting features based on model performance
- generating or consuming model artifacts

---

## Layout

```
prepare/
  anchors.py
  shocks.py
  assemble.py
```

- **Anchors** – source-specific ingestion and feature construction for low-frequency macroeconomic data
- **Shocks** – source-specific ingestion and feature construction for high-frequency financial market data
- **Assemble** – cross-source dataset assembly and alignment into model-ready training tables