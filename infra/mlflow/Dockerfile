FROM ghcr.io/mlflow/mlflow:latest

# Add Postgres driver + AWS SDK so:
# - backend-store-uri can be postgres
# - artifacts can be S3
RUN pip install --no-cache-dir psycopg2-binary boto3
