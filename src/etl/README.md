← [Back to Source](../README.md)

# ETL

Extraction, transformation, and feature construction logic for nowcasting.

---

## Contract

- Contains ETL-stage logic only for nowcasting
- Must not assume training, tracking, or serving concerns
- Produces model-ready datasets for downstream stages

---

## Responsibilities

- Ingest raw data from external sources
- Validate and normalize inputs into canonical forms
- Construct features used by training and inference

## Layout

```
etl/
  anchors/
  assemble/
  shocks/
```

- **[Anchors](./anchors/README.md)** – slow-moving macro sources
- **[Assemble](./assemble/README.md)** – combining anchor and shock datasets
- **[Shocks](./shocks/README.md)** – fast-moving financial market sources