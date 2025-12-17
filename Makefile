# config
APP_NAME	:= e2e-macro-nowcasting
IMAGE		:= $(APP_NAME):dev
ENV_FILE	:= .env
WORKDIR		:= /app


# common docker run flags
DOCKER_RUN  := docker run --rm -it \
	--env-file $(ENV_FILE) \
	-v $(PWD):$(WORKDIR) \
	-w $(WORKDIR) \
	$(IMAGE)


# do
.PHONY: build run shell test

build:
	docker build -t $(IMAGE) .

run:
	$(DOCKER_RUN) python scripts/ingest_fred.py

test:
	$(DOCKER_RUN) pytest -q

shell:
	$(DOCKER_RUN) bash