# Docker

Container images for each stage of the ML lifecycle and supporting infrastructure.

---

## Design

- **`base`** – shared runtime layer
- **Runtimes** – job-specific layers on top of `base`
- **Services** – always-on infrastructure

Objectives:

- Fast builds via layered images
- Separation of concerns
- Reproducible runtimes across local, Airflow, and ECS

---

## Layout

```
infra/docker/
  runtimes/
  services/
```

**Components:**
- [Runtime images](runtimes/README.md)
- [Service images](services/README.md)

---

## Build Rules

- `base` installs `requirements/base.txt`
- Runtime images install only their own `requirements/runtimes/*.txt`
- Service images install only what they need to run