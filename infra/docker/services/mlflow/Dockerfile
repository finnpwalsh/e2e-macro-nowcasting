FROM ghcr.io/mlflow/mlflow:v2.14.3

USER root

RUN apt-get update \
 && apt-get install -y --no-install-recommends curl \
 && rm -rf /var/lib/apt/lists/*

COPY requirements/ /opt/project/requirements/
RUN pip install --no-cache-dir -r /opt/project/requirements/services/mlflow.txt

USER 10001

EXPOSE 5000