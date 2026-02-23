from __future__ import annotations

from datetime import datetime
import importlib

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models.baseoperator import chain


def call_job(module: str) -> None:
    mod = importlib.import_module(f"jobs.{module}")
    mod.run()


def job(task_id: str, module: str) -> PythonOperator:
    return PythonOperator(
        task_id=task_id,
        python_callable=call_job,
        op_args=[module],
    )


with DAG(
    dag_id="price_nowcasting_baseline",
    start_date=datetime(2010, 1, 1),
    schedule="@monthly",   # or None for manual only
    catchup=False,
    max_active_runs=1,
    tags=["nowcast", "baseline"],
) as dag:

    prepare_anchors_fred = job(
        task_id="prepare_anchors_fred",
        module="prepare.anchors.sources.fred",
    )

    prepare_anchors_assemble = job(
        task_id="prepare_anchors_assemble",
        module="prepare.anchors.assemble",
    )

    prepare_anchors_features = job(
        task_id="prepare_anchors_features",
        module="prepare.anchors.build_features",
    )

    train_baseline = job(
        task_id="train_baseline",
        module="train.baseline",
    )

    track_publish = job(
        task_id="track_publish",
        module="track.publish",
    )

    select_promote = job(
        task_id="select_promote",
        module="select.promote",
    )

    chain(
        prepare_anchors_fred,
        prepare_anchors_assemble,
        prepare_anchors_features,
        train_baseline,
        track_publish,
        select_promote,
    )