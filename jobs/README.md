← [Back to Root](../README.md)

# Jobs

Pipeline entrypoints that orchestrate logic from `src` and perform all I/O. 

- `jobs/` = execution & orchestration
- `src/` = library code

> Jobs are executed via CLI locally and containerized execution under orchestration.

---

## Contract

Jobs are executable entrypoints that:
- handle runtime setup and configuration
- perform all external I/O
- delegate core logic to `src/`
- produce versioned outputs

Jobs are not responsible for:
- implementing business / modeling logic (lives in `src/`)
- sharing logic across jobs
- maintaining state across runs (stages only communicate via persisted artifacts)

Jobs define how the logic runs, not what the logic is. Each job is independently executable and produces outputs consumed only via persisted artifacts.