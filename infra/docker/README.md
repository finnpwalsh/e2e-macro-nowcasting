← [Back to Infra](../README.md)

# Docker

Container images for each stage of the ML lifecycle and supporting infrastructure.

- **`base`** – shared runtime layer
- **Runtimes** – job-specific layers on top of base
- **Services** – always-on infrastructure images

---

## Contract

- The base image installs `requirements/base.txt`
- Runtime images extend the base image and install only their corresponding `requirements/runtimes/*.txt`
- Service images do **not** extend the base image and install only dependencies required to run the service

---

## Layout

```
infra/docker/
  runtimes/
  services/
```

- [Runtime images](runtimes/README.md)
- [Service images](services/README.md)