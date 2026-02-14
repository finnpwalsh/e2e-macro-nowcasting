# --------------------------------------------------------
# Compose Layering
# --------------------------------------------------------
DC := docker compose -f docker-compose.yml -f docker-compose.dev.yml

PROJECT_DIR := /opt/project
AIRFLOW_SERVICE := airflow-scheduler
DAG_ID := price_nowcasting

# --------------------------------------------------------
# Helpers
# --------------------------------------------------------
define RUN_STAGE
	$(DC) run --rm --entrypoint bash $(1) -lc "$(2)"
endef

define EXEC_AIRFLOW
	$(DC) exec $(AIRFLOW_SERVICE) bash -lc "cd $(PROJECT_DIR) && $(1)"
endef

# --------------------------------------------------------
# Build
# --------------------------------------------------------
.PHONY: build build-base build-runtimes

build-base:
	$(DC) build nowcasting-base

build-runtimes:
	$(DC) build runtime-prepare runtime-train runtime-track runtime-select

build: build-base build-runtimes

# --------------------------------------------------------
# Infra
# --------------------------------------------------------
.PHONY: up down init logs ps shell

up: 
	$(DC) up -d

down:
	$(DC) down

init:
	$(DC) run --rm airflow-init

logs:
	$(DC) logs -f

ps:
	$(DC) ps

shell:
	$(DC) exec $(AIRFLOW_SERVICE) bash

# --------------------------------------------------------
# Data Plane
# --------------------------------------------------------
.PHONY: prepare prepare-anchors prepare-shocks prepare-assemble train

prepare: prepare-achors prepare-shocks prepare-assemble

prepare-anchors:
	$(call RUN_STAGE,runtime-prepare,python jobs/prepare/anchors/fred.py)

prepare-shocks:
	$(call RUN_STAGE,runtime-prepare,python jobs/prepare/shocks/yf.py)

prepare-assemble:
	$(call RUN_STAGE,runtime-prepare,python jobs/prepare/assemble/merge.py)

train: train-baseline

train-baseline:
	$(call RUN_STAGE,runtime-train,python jobs/train/baseline.py)

# --------------------------------------------------------
# Control Plane
# --------------------------------------------------------
.PHONY: track select

track:
	$(call RUN_STAGE,runtime-track,python jobs/track/publish.py)

select:
	$(call RUN_STAGE,runtime-select,python jobs/select/promote.py)

# --------------------------------------------------------
# Testing
# --------------------------------------------------------
.PHONY: test test-airflow

test:
	pytest -q

test-airflow:
	$(call RUN_STAGE,runtime-train,pytest -q)

# --------------------------------------------------------
# Orchestrated Run
# --------------------------------------------------------
.PHONY: trigger run

trigger:
	$(call EXEC_AIRFLOW,airflow dags trigger $(DAG_ID))

run: trigger
	@echo "Triggered DAG: $(DAG_ID)"