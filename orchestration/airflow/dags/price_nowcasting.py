"""
End-to-end FRED + yfinance data pipeline (V1).

Manually triggered pipeline that ingests raw FRED + yfinance
time-series data, cleans and prepares modeling datasets, merges, 
and trains a baseline Ridge regression model for evaluation.
"""
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models.baseoperator import chain

from scripts.ingest_fred import main as ingest_fred
from scripts.ingest_yfinance import main as ingest_yfinance
from scripts.clean_fred import main as clean_fred
from scripts.clean_yfinance import main as clean_yfinance
from scripts.merge import main as merge
from scripts.train_ridge import main as train_ridge

DEFAULT_ARGS = {
    "owner": "ml-platform",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="price_nowcasting",
    description=
        ("Manual V1 pipeline: ingest (FRED+yfinance), clean, merge train baseline."),
    default_args=DEFAULT_ARGS,
    start_date=datetime(2025,12,1),
    schedule_interval=None, # manual trigger for v1
    catchup=False,
    tags=["v1", "fred", "yfinance", "baseline"]
) as dag:
    ingest_fred_task = PythonOperator(
        task_id="ingest_fred",
        python_callable=ingest_fred,
    )

    ingest_yfinance_task = PythonOperator(
        task_id="ingest_yfinance",
        python_callable=ingest_yfinance,
    )

    clean_fred_task = PythonOperator(
        task_id="clean_fred",
        python_callable=clean_fred,
    )

    clean_yfinance_task = PythonOperator(
        task_id="clean_yfinance",
        python_callable=clean_yfinance,
    )

    merge_task = PythonOperator(
        task_id="merge",
        python_callable=merge,
    )

    train_task = PythonOperator(
        task_id="train_ridge",
        python_callable=train_ridge,
    )

    chain(
        [ingest_fred_task, ingest_yfinance_task],
        [clean_fred_task, clean_yfinance_task],
        merge_task,
        train_task,
    )
