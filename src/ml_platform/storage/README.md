← [Back to ML Platform](../README.md)

# Storage

Storage backends and artifact key definitions.

---

| Component | Description |
| --------- | ----------- |
| **base** | storage interface definitions |
| **backends** | storage backends implementing **base** |
| **factory** | backend store resolver (local or S3) |
| **keys** | artifact key definitions |
| **serde** | ser/de utilities for persisted artifacts |