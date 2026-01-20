← [Back to Nowcast](../README.md)

# ETL

Extraction, transformation, and feature construction logic for nowcasting.

---

## Contract

- Contains ETL-stage logic only for nowcasting
- Responsible for ingestion, validation, and feature construction
- Must not assume training, tracking, or serving concerns

---

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