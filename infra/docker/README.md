← [Back to Infra](../README.md)

# Docker

Container images for each stage of the ML lifecycle and supporting infrastructure.

---

## Components 

| Component | Description |
| --------- | ----------- |
| **base** | shared runtime foundation |
| **runtimes** | execution images for pipeline jobs |
| **services** | always-on infrastructure images |

---

## Contract

- The base runtime image installs `dependencies/base.txt`
- All runtime images extend the base runtime image and install only their corresponding `dependencies/runtimes/*.txt`
- Service images do **not** extend the base runtime image and install only dependencies required to run the service