← [Back to Jobs](../README.md)

# Track

Tracking entrypoints log and register already-produced artifacts into metadata systems. Tracking is control-plane: it should not retrain models nor define artifact schemas.

---

## Contract

- Read `run.json` and referenced artifacts from storage
- Delegate backend-specific tracking to `src`
- Treat tracking as best-effort: training artifacts remain valid even if tracking fails

---

## Layout

```
jobs/track/
```