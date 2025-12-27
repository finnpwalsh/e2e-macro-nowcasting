# config
APP_NAME    := e2e-macro-nowcasting
IMAGE       := $(APP_NAME):dev
PROJECT_DIR := /opt/project

# local python dev
PYTHON := .venv/bin/python

# Airflow service to run CLI commands
AIRFLOW_SERVICE := airflow-scheduler
DAG_ID := price_nowcasting

.PHONY: build up init down logs ps shell \
		ingest clean merge train test \
		trigger run

# build
build:
	docker build -t $(IMAGE) .

# infra
up:
	docker compose up -d

init:
	docker compose run --rm airflow-init

down:
	docker compose down

logs:
	docker compose logs -f

ps:
	docker compose ps

shell:
	docker compose exec $(AIRFLOW_SERVICE) bash

# dev utilities (manual)
ingest:
	docker compose exec $(AIRFLOW_SERVICE) bash -lc "cd $(PROJECT_DIR) && python scripts/ingest_fred.py"
	docker compose exec $(AIRFLOW_SERVICE) bash -lc "cd $(PROJECT_DIR) && python scripts/ingest_yfinance.py"

clean:
	docker compose exec $(AIRFLOW_SERVICE) bash -lc "cd $(PROJECT_DIR) && python scripts/clean_fred.py"
	docker compose exec $(AIRFLOW_SERVICE) bash -lc "cd $(PROJECT_DIR) && python scripts/clean_yfinance.py"

merge:
	docker compose exec $(AIRFLOW_SERVICE) bash -lc "cd $(PROJECT_DIR) && python scripts/merge.py"

train:
	docker compose exec $(AIRFLOW_SERVICE) bash -lc "cd $(PROJECT_DIR) && python scripts/train_ridge.py"

test:
	docker compose exec $(AIRFLOW_SERVICE) bash -lc "cd $(PROJECT_DIR) && pytest -q"

# orchestrated run 
trigger:
	docker compose exec $(AIRFLOW_SERVICE) bash -lc "cd $(PROJECT_DIR) && airflow dags trigger $(DAG_ID)"

run: trigger
	@echo "Triggered DAG: $(DAG_ID)"