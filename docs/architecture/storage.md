← [Back to Docs](../README.md)

# Storage Architecture

This document defines the storage layout and data semantics of the macro nowcasting platform.

Datasets and artifacts are persisted to S3 buckets we will call `data` and `artifacts`, respectively.

## `data`

All datasets are organized under a tiered lakehouse structure:

```
    raw
     ↓
 canonical
     ↓
model_ready
```

Each tier represents a different level of processing and validation:

---

**Raw** – external provider snapshots

Properties:
- may have missing values
- no cross-source merging
- not safe for modeling

---

**Canonical** – cleaned, normalized, and domain-validated datasets

Properties:
- domain-specific (e.g., anchors)
- validated against domain contracts
- not safe for modeling
- produces a domain-specific combined-source dataset

---

**Model-ready** – modeling tables consumed by training

Properties:
- Fully validated
- Safe for modeling

---

## `artifacts`

Run-scoped artifacts produced by training. 

Properties:
- immutable
- never overwritten
- unique Run IDs

Each run produces:
- manifest – run metadata
- summary – quick-reference metadata
  - summary ⊂ manifest
- predictions
- model object