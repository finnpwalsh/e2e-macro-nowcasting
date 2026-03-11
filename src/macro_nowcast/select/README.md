← [Back to Macro Nowcast](../README.md)

# Select

Model selection and champion promotion logic.

---

## Components

| Component | Description |
| --------- | ----------- |
| **resolver** | resolves challenger and champion models + handles absent-champion case |
| **decider** | decision logic for champion promotion – compares challenger vs. champion performance |
| **selector** | produces selection result based on decider's outcome |
| **schema** | shared schemas for resolver and selector outputs |