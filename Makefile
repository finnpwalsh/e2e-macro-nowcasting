# config
APP_NAME := e2e-macro-nowcasting
IMAGE    := $(APP_NAME):dev

# Airflow service to run CLI commands
AIRFLOW_SERVICE := airflow-scheduler
DAG_ID := fred_pipeline

.PHONY: build up init down logs ps shell \
		ingest clean train test \
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
	docker compose exec $(AIRFLOW_SERVICE) bash -lc "python /opt/project/scripts/ingest_fred.py"

clean:
	docker compose exec $(AIRFLOW_SERVICE) bash -lc "python /opt/project/scripts/clean_fred.py"

train:
	docker compose exec $(AIRFLOW_SERVICE) bash -lc "python /opt/project/scripts/train_ridge.py"

test:
	docker compose exec $(AIRFLOW_SERVICE) bash -lc "pytest -q"

# orchestrated run 
trigger:
	docker compose exec $(AIRFLOW_SERVICE) bash -lc "airflow dags trigger $(DAG_ID)"

run: trigger
	@echo "Triggered DAG: $(DAG_ID)"