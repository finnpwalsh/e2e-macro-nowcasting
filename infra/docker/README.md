← [Back to Infra](../README.md)

# Docker

Container images for each stage of the ML lifecycle and supporting infrastructure.

- **Runtimes** – execution images for pipeline jobs
  - `base` – shared runtime foundation
  - stage-specific runtimes layered on top
- **Services** – always-on infrastructure images

---

## Contract

- The base runtime image installs `requirements/base.txt`
- All runtime images extend the base runtime image and install only their corresponding `requirements/runtimes/*.txt`
- Service images do **not** extend the base runtime image and install only dependencies required to run the service

---

## Layout

```
infra/docker/
  runtimes/
  services/
```

- **[Runtime images](runtimes/README.md)**
- **[Service images](services/README.md)**