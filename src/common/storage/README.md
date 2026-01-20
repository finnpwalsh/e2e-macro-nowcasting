← [Back to Common](../README.md)

# Storage

Shared storage abstractions for nowcasting artifacts and datasets.

---

## Contract

- `base.py` defines the storage interface
- `backends/` contains concrete storage implementations
- `factory.py` selects the active backend at runtime
- `io.py` and `paths.py` provide shared helpers used by all stages

---

## Layout

```
storage/
  base.py
  factory.py
  io.py
  paths.py
  backends/
    local.py
    s3.py
```