# macroeconomic nowcasting platform

Cloud-native inflation nowcasting system built as a production-grade ML platform.

Includes structured pipelines for data preparation, model training & artifact tracking, and champion promotion. Built with modular architecture separating infrastructure, platform primitives, and domain logic.

---

## system architecture

```
      data sources
           ↓
        prepare
           ↓
  model-ready datasets
           ↓
         train
           ↓
artifacts + run manifest
           ↓
         select
           ↓
    champion pointer
           ↓
         serve
     (coming soon)
```
---

 ## getting started

- See [`docs/README.md`](docs/README.md) for detailed project documentation
- New here? See [quickstart](docs/quickstart.md) to run the system locally

---

## release status

- **latest release:** v1.5.0 – contract & execution hardening
- **in progress:** v1.5.1 – two-stage nowcasting

---

## components

| Component | Description |
| --------- | ----------- |
| **[dependencies](dependencies/README.md)** | dependency specifications |
| **[docs](docs/README.md)** | design and reference documents |
| **[infra](infra/docker/README.md)** | container management and cloud infrastructure |
| **[jobs](jobs/README.md)** | executable pipeline entrypoints |
| **[src](src/README.md)** | reusable library code |
| **tests** | automated checks |