← [Back to Source](../README.md)

# Macro Nowcast

Domain-specific logic for the macro nowcasting system.

---

## Components

Components are divided into lifecycle stages + cross-stage utilities.

| Lifecycle stage | Description |
| --------------- | ----------- |
| **[prepare](./prepare/README.md)** | ETL pipelines for anchors and shocks datasets |
| **[train](./train/README.md)** | model training and candidate generation |
| **[select](./select/README.md)** | champion model selection and promotion logic |


| Utility | Description |
| ------- | ----------- |
| **[externals](./externals/README.md)** | interfaces for external data sources |
| **storage** | Dataset key definitions for the S3 data lake |
| **eval** | model evaluation utilities (regression diagnostics) |