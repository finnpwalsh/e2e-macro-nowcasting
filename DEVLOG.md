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
### December 18, 2025
**NEXT**
- raw → clean stage for FRED series

**DONE**
- ingest multiple FRED series
- store FRED series list in config
- incl. test for all global FRED series
- move raw FRED test to tests/data
- remove non-V1 directories + files

### December 17, 2025
**NEXT**
- ingest multiple FRED series
- raw → clean stage for FRED series

**DONE**
- enforce FRED schema
- raw FRED data contract test (passed)
    - Takes multiple series
- added docstrings to ingest_fred, fred, raw FRED data test for clarity



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