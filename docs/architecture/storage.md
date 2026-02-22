← [Back to Docs](../README.md)

# Storage Architecture

This document defines the storage layout and data semantics of the macro nowcasting platform.

## 1. Data Lake Layout

All datasets are organized under a tiered lakehouse structure:

```
data/
  raw/
  canonical/
  model_ready/
```

Each tier represents a different level of processing and validation.

---

## 2. Tier Definitions

### 2.1 Raw

External provider snapshots.

Properties:
- may have missing values
- no cross-source merging
- not safe for modeling

Layout:
```
data/raw/
  <source>/snapshot.parquet
```

---

### 2.2 Canonical

Cleaned, normalized, and domain-validated datasets.

Properties:
- domain-specific (e.g., anchors)
- validated against domain contracts
- not safe for modeling
- produces a domain-specific combined-source dataset (`all.parquet`)

Layout:
```
data/canonical/
  anchors/
    <source>.parquet
    all.parquet
  shocks/
    <source>.parquet
    all.parquet
```

### 2.3 Model Ready
Modeling tables consumed by training.

Properties:
    - Fully validated
    - Safe for modeling

Layout:
```
data/model_ready/
  anchors/
    table.parquet
  shocks/
    table.parquet
```

---

## 3. Artifact Architecture

Run-scoped artifacts produced by training. 

Properties:
    - immutable
    - never overwritten
    - unique Run IDs

Layout:
```
artifacts/
  models/
    <model_name>/<run_id>/
      model.joblib
      metrics.json
  eval/
    <model_name>/<run_id>/
      predictions.parquet
      summary.json
```

---

## 4. Addressability

Datasets and artifacts are referenced via logical keys defined in code.

Physical storage may be:
- local filesystem
- S3
- other compatible object store

Storage backend is abstracted by the platform layer.