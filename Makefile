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
# Docker
# --------------------------------------------------------
AWS_REGION ?= us-east-1
PROFILE ?= nowcasting-dev

ACCOUNT_ID := $(shell aws sts get-caller-identity \
	--profile $(PROFILE) \
	--query Account \
	--output text)

ECR := $(ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com

IMAGE ?= prepare
IMAGE_TAG ?= v1.5.0

# ===== Login =====
.PHONY: docker-login

docker-login:
	aws ecr get-login-password \
		--region $(AWS_REGION) \
		--profile $(PROFILE) \
	| docker login \
		--username AWS \
		--password-stdin $(ECR)

# ===== Build =====
.PHONY: build-image build-runtimes

build-image:
	$(DC) build nowcasting-dev-${IMAGE}

build-runtimes:
	$(MAKE) build-image IMAGE=prepare
	$(MAKE) build-image IMAGE=train
	$(MAKE) build-image IMAGE=select

# ===== Push =====
.PHONY: push-image push-runtimes

push-image:
	docker tag nowcasting-dev-$(IMAGE) $(ECR)/nowcasting-dev-$(IMAGE):$(IMAGE_TAG)
	docker push $(ECR)/nowcasting-dev-$(IMAGE):$(IMAGE_TAG)

push-runtimes:
	$(MAKE) push-image IMAGE=select
	$(MAKE) push-image IMAGE=train
	$(MAKE) push-image IMAGE=select

# ===== Build & Push =====
.PHONY: build-push-image

build-push-image:
	$(MAKE) build-image
	$(MAKE) push-image


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