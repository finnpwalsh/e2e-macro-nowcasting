← [Back to Root](../README.md)

# Jobs

Executable pipeline entrypoints.

---

## Contract

Jobs do:
- handle runtime setup and configuration
- orchestrate logic from `src`
- produce versioned outputs
- communicate via persisted outputs

Jobs do not:
- share logic across jobs
- maintain state across runs

---

## Components

| Component | Description | Reads from | Writes to |
| --------- | ----------- | ---------- | --------- |
| **prepare** | data preparation & feature generation | data | data |
| **train** | model training & artifact tracking | data | artifacts |
| **select** | model selection & champion promotion | artifacts | artifacts |