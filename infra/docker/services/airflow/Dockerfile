FROM apache/airflow:2.9.3-python3.11

WORKDIR /opt/airflow

COPY requirements/ /opt/project/requirements/

USER airflow
RUN pip install --no-cache-dir \
    --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.9.3/constraints-3.11.txt" \
    -r /opt/project/requirements/services/airflow.txt

COPY orchestration/airflow/dags/ /opt/airflow/dags/