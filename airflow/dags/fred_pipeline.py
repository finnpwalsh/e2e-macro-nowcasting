from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

from scripts.ingest_fred import main as ingest_fred
from scripts.clean_fred import main as clean_fred
from scripts.train_ridge import main as train_baseline

with DAG(
    dag_id="fred_pipeline",
    start_date=datetime(2025,12,1),
    schedule=None, # manual trigger for v1
    catchup=False,
    tags=["v1", "fred"]
) as dag:
    ingest = PythonOperator(
        task_id="ingest_fred",
        python_callable=ingest_fred,
    )

    clean = PythonOperator(
        task_id="clean_fred",
        python_callable=clean_fred,
    )

    train = PythonOperator(
        task_id="train_baseline",
        python_callable=train_baseline,
    )

    ingest >> clean >> train