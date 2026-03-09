# --------------------------------------------------------
# Compose
# --------------------------------------------------------
DC := docker compose -f docker-compose.yml

PROJECT_DIR := /opt/project

# --------------------------------------------------------
# Helpers
# --------------------------------------------------------
define RUN_STAGE
	$(DC) run --rm --entrypoint bash $(1) -lc "$(2)"
endef

# --------------------------------------------------------
# Build
# --------------------------------------------------------
.PHONY: build build-base build-runtimes

build-base:
	$(DC) build nowcasting-dev-base

build-runtimes:
	$(DC) build nowcasting-dev-prepare nowcasting-dev-train nowcasting-dev-select nowcasting-dev-workspace

build: build-base build-runtimes

# --------------------------------------------------------
# Data Plane
# --------------------------------------------------------
.PHONY: prepare 
.PHONY: prepare-anchors prepare-anchors-fred prepare-anchors-assemble prepare-anchors-features
.PHONY: prepare-shocks-tiingo prepare-shocks-assemble prepare-shocks-features
.PHONY: train train-baseline


# ===== Prepare =====
prepare: prepare-anchors prepare-shocks

# Anchors
prepare-anchors: prepare-anchors-fred prepare-anchors-assemble prepare-anchors-features
	
prepare-anchors-fred:
	$(call RUN_STAGE,nowcasting-dev-prepare,python -m jobs.prepare.anchors.sources.fred)
	
prepare-anchors-assemble:
	$(call RUN_STAGE,nowcasting-dev-prepare,python -m jobs.prepare.anchors.assemble)

prepare-anchors-features:
	$(call RUN_STAGE,nowcasting-dev-prepare,python -m jobs.prepare.anchors.build_features)


# Shocks
prepare-shocks: prepare-shocks-tiingo prepare-shocks-assemble prepare-shocks-features

prepare-shocks-tiingo:
	$(call RUN_STAGE,nowcasting-dev-prepare,python -m jobs.prepare.shocks.sources.tiingo)

prepare-shocks-assemble:
	$(call RUN_STAGE,nowcasting-dev-prepare,python -m jobs.prepare.shocks.assemble)

prepare-shocks-features:
	$(call RUN_STAGE,nowcasting-dev-prepare,python -m jobs.prepare.shocks.build_features)


# ===== Train =====

train: train-baseline

train-baseline:
	$(call RUN_STAGE,nowcasting-dev-train,python -m jobs.train.run)

# --------------------------------------------------------
# Control Plane
# --------------------------------------------------------
.PHONY: select

select:
	$(call RUN_STAGE,nowcasting-dev-select,python -m jobs.select.run)

# --------------------------------------------------------
# Testing
# --------------------------------------------------------
.PHONY: test

test:
	$(call RUN_STAGE,nowcasting-dev-workspace)