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
.PHONY: build ingest clean train run test shell

build:
	docker build -t $(IMAGE) .

ingest:
	$(DOCKER_RUN) python scripts/ingest_fred.py

clean:
	$(DOCKER_RUN) python scripts/clean_fred.py

train:
	$(DOCKER_RUN) python scripts/train_baseline.py

run: ingest clean train
	@echo "Run complete."

test:
	$(DOCKER_RUN) pytest -q

shell:
	$(DOCKER_RUN) bash