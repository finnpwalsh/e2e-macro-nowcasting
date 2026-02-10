FROM ghcr.io/mlflow/mlflow:v2.14.3

USER root

COPY requirements/ /opt/project/requirements/
RUN pip install --no-cache-dir -r /opt/project/requirements/services/mlflow.txt

USER 10001

EXPOSE 5000