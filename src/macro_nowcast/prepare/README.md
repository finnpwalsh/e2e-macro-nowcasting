← [Back to Macro Nowcast](../README.md)

# Prepare

Domain-specific data ingestion, transformation, and feature construction logic for macro nowcasting.

---

## Layout

| Component | Description |
| ------------- | --------------- |
 | **anchors** | ETL logic for slow-moving macro sources |
 | **shocks** | ETL logic for fast-moving financial market sources |
| **_interfaces** | interfaces implemented by anchors + shocks |