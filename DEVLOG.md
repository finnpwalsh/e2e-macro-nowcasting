# Activity Log
## Template
## Month XX, 202X
**NEXT**
- 
- 
- 

**DONE**
- 
- 
- 

## V1
## December 22, 2025
**NEXT**
- begin v1 -> v2
- ingest yfinance

**DONE**
- add tests on baseline model
- v0.4.0 release
- add docker-compose for Airflow + PostgreSQL
- fred_pipeline_v1 DAG live + successful
- v1.0.0 release

# December 21, 2025
**NEXT**
- add tests on baseline model
- v0.4.0 tag/release

**DONE**
- wide-form, model-ready FRED dataset
- v0.3.0 tag/release
- make repo public
- add baseline model on FRED

## December 20, 2025
**NEXT**
- wide-form, model-ready FRED dataset

**DONE**
- raw -> clean stage for FRED series
- clean FRED data contract test
- refactor README

### December 18, 2025
**NEXT**
- raw → clean stage for FRED series

**DONE**
- ingest multiple FRED series
- store FRED series list in config
- incl. test for all global FRED series
- move raw FRED test to tests/data
- remove non-V1 directories + files
- v0.2.0 tag

### December 17, 2025
**NEXT**
- ingest multiple FRED series
- raw → clean stage for FRED series

**DONE**
- enforce FRED schema
- raw FRED data contract test (passed)
    - Takes multiple series
- added docstrings to ingest_fred, fred, raw FRED data test for clarity
- v0.1.0 tag

### December 16, 2025
**NEXT**
- enforce FRED schema
- data tests
- scale fred ingest to take multiple series

**DONE**
- finalize Dockerfile + Makefile
- move all workflow to Docker
- add smoke test to ensure pytest is functional
- ingestion writes parquet