FROM ghcr.io/mlflow/mlflow:2.14.3

# Add Postgres driver + AWS SDK so:
# - backend-store-uri can be postgres
# - artifacts can be S3
USER root
RUN pip install --no-cache-dir psycopg2-binary boto3

USER 10001

EXPOSE 5000