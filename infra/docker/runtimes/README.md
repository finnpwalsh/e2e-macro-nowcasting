← [Back to Docker](../README.md)

# Runtime Images

Containerized execution environments for pipeline jobs.

Runtime images are built on top of a shared base imsge and provide stage-specific dependencies for executing jobs.

---

## Contract

- Runtime images extend the shared base image
- Each runtime installs only its own incremental dependencies
- Runtimes are used for batch execution (local, Airflow, ECS)

Runtime images do not define services or long-running processes.

---

## Layout

```
infra/docker/runtimes/
  base/
  etl/
  train/
  track/
  serve/
```

Each folder defines a single runtime image.