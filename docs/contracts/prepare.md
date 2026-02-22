← [Back to Lifecycle](../README.md)

# Prepare

This document defines the Prepare stage in the price nowcasting execution lifecycle.

**Responsibilities**
- Ingest data from external sources
- Clean, normalize, and align time series
- Validate raw and transformed data for schema, completeness, and temporal consistency
- Construct features required for downstream modeling

**Execution**
- Implemented as preparation jobs under `jobs/prepare/`
- Core logic lives in `src/price_nowcasting/prepare/`

**Outputs**
- Versioned datasets suitable for training