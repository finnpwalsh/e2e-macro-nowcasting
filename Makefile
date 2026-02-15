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


# ===== Prepare =====
prepare: prepare-achors prepare-shocks prepare-assemble

# Anchors
prepare-anchors: prepare-anchors-fred prepare-anchors-assemble prepare-anchors-features
	
prepare-anchors-fred:
	$(call RUN_STAGE,runtime-prepare,python -m jobs.prepare.anchors.sources.fred)
	
prepare-anchors-assemble:
	$(call RUN_STAGE,runtime-prepare,python -m jobs.prepare.anchors.assemble)

prepare-anchors-features:
	$(call RUN_STAGE,runtime-prepare,python -m jobs.prepare.anchors.build_features)


# Shocks
prepare-shocks: prepare-shocks-tiingo prepare-shocks-assemble prepare-shocks-features

prepare-shocks-tiingo:
	$(call RUN_STAGE,runtime-prepare,python -m jobs.prepare.shocks.sources.tiingo)

prepare-shocks-assemble:
	$(call RUN_STAGE,runtime-prepare,python -m jobs.prepare.shocks.assemble)

prepare-shocks-features:
	$(call RUN_STAGE,runtime-prepare,python -m jobs.prepare.shocks.build_features)


# ===== Train =====
train: train-baseline

train-baseline:
	$(call RUN_STAGE,runtime-train,python -m jobs.train.baseline)

# --------------------------------------------------------
# Control Plane
# --------------------------------------------------------
.PHONY: track select

track:
	$(call RUN_STAGE,runtime-track,python -m jobs.track.publish)

select:
	$(call RUN_STAGE,runtime-select,python -m jobs.select.promote)

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