from __future__ import annotations

from datetime import datetime

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.models.baseoperator import chain

APP_NET = "e2e-macro-nowcasting-net"

COMMON_ENV = {
    "PYTHONPATH": "/opt/project/src",
    "STORAGE_BACKEND": "s3",
    "AWS_REGION": "us-east-1",
    "AWS_DEFAULT_REGION": "us-east-1",
    "MLFLOW_TRACKING_URI": "http://mlflow:5000",
    "MLFLOW_EXPERIMENT_NAME": "nowcasting",
    "NOWCAST_REGISTRY_MODEL": "nowcasting-models",
    "NOWCAST_MODEL_ALIAS": "champion",
}

with DAG(
    dag_id="price_nowcast",
    start_date=datetime(2010, 1, 1),
    catchup=False,
    tags=["nowcast", "baseline", "docker"],
) as dag:
    prepare_anchors_fred = DockerOperator(
        task_id="prepare_anchors_fred",
        image="nowcasting-prepare:latest",
        command="bash -lc 'python -m jobs.prepare.anchors.sources.fred'",
        auto_remove=True,
        mount_tmp_dir=False,
        network_mode=APP_NET,
        environment=COMMON_ENV,
    )

    prepare_anchors_assemble = DockerOperator(
        task_id="prepare_anchors_assemble",
        image="nowcasting-prepare:latest",
        command="bash -lc 'python -m jobs.prepare.anchors.assemble'",
        auto_remove=True,
        mount_tmp_dir=False,
        network_mode=APP_NET,
        environment=COMMON_ENV,
    )

    prepare_anchors_features = DockerOperator(
        task_id="prepare_anchors_features",
        image="nowcasting-prepare:latest",
        command="bash -lc 'python -m jobs.prepare.anchors.build_features'",
        auto_remove=True,
        mount_tmp_dir=False,
        network_mode=APP_NET,
        environment=COMMON_ENV,
    )

    train_baseline = DockerOperator(
        task_id="train_baseline",
        image="nowcasting-train:latest",
        command="bash -lc 'python -m jobs.train.baseline'",
        auto_remove=True,
        mount_tmp_dir=False,
        network_mode=APP_NET,
        environment=COMMON_ENV,
    )

    track_publish = DockerOperator(
        task_id="track_publish",
        image="nowcasting-track:latest",
        command="bash -lc 'python -m jobs.track.publish'",
        auto_remove=True,
        mount_tmp_dir=False,
        network_mode=APP_NET,
        environment=COMMON_ENV,
    )


    select_promote = DockerOperator(
            task_id="select_promote",
            image="nowcasting-select:latest",
            command="bash -lc 'python -m jobs.select.promote'",
            auto_remove=True,
            mount_tmp_dir=False,
            network_mode=APP_NET,
            environment=COMMON_ENV,
        )
    chain = (
        prepare_anchors_fred,
        prepare_anchors_assemble,
        prepare_anchors_features,
        train_baseline,
        track_publish,
        select_promote,
    )