← [Back to Macro Nowcast](../README.md)

# Prepare

Domain-specific data ingestion, transformation, and feature construction logic for macro nowcasting.

---

## Responsibilities

- Ingest and normalize raw external data sources
- Apply domain-specific transformations and feature construction

---

## Layout

```
prepare/
  anchors/
  assemble/
  shocks/
```

- `anchors/` – slow-moving macro sources
- `assemble/` – combining anchor and shock datasets
- `shocks/` – fast-moving financial market sources