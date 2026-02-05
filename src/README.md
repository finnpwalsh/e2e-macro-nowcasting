← [Back to Root](../README.md)

# Source

Reusable library code shared across all execution environments.

---

## Scope

- `src/` contains reusable logic only
- How and when that logic runs is decided outside `src/`

---

## Layout

```
src/
  price_nowcast/
  ml_platform/
```

- [`price_nowcast/`](./price_nowcast/README.md) – nowcasting-specific logic
- [`ml_platform`](./ml_platform/README.md) – reusable production primitives