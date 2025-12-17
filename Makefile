# --------------------- Config ---------------------
PYTHONPATH := .
VENV := .venv
PY := $(VENV)/bin/python
PIP:= $(PY) -m pip

.PHONY: setup ingest test

# --------------------- Setup ----------------------
setup:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

#------------------ Run ingestion ------------------
ingest-all:
	ingest-fred

ingest-fred: 
	PYTHONPATH=$(PYTHONPATH) $(PY) scripts/ingest_fred.py

# --------------------- Tests ----------------------
test:
	PYTHONPATH=$(PYTHONPATH) $(PY) -m pytest -q