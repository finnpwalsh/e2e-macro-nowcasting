← [Back to Jobs](../README.md)


# ETL

ETL pipeline entrypoints responsible for producing raw, processed, and model-ready datasets used by downstream training jobs.

---

## Contract

- Produce raw source datasets and processed feature datasets
- Assemble model-ready training tables consumed by downstream jobs
- Organize ETL by domain (`anchors`, `shocks`) and cross-source assembly (`assemble`)

---

## Layout

```
jobs/etl/
  anchors/
  shocks/
  assemble/
```

- **Anchors** – source-specific ingestion and feature construction for low-frequency macroeconomic data
- **Shocks** – source-specific ingestion and feature construction for high-frequency financial market data
- **Assemble** – cross-source dataset assembly and alignment into model-ready training tables