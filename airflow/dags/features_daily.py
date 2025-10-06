# /airflow/dags/features_daily.py
# путь: /airflow/dags/features_daily.py
from datetime import datetime
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)

# Заменить на свой owner/repo в нижнем регистре:
IMAGE = "ghcr.io/kuznetsov-ai-dev/mlops_for_llm_agent-jobs:latest"

default_args = {
    "owner": "mlops",
    "retries": 0,
}

with DAG(
    dag_id="features_daily",
    start_date=datetime(2025, 10, 1),
    schedule_interval="@daily",
    catchup=False,
    default_args=default_args,
    tags=["rossmann", "features"],
) as dag:

    build_features = KubernetesPodOperator(
        namespace="mlops",
        name="build-features",
        task_id="build_features",
        image=IMAGE,
        cmds=["python"],
        arguments=["/app/jobs/build_features.py"],
        env_vars={
            "S3_ENDPOINT": "http://mlflow-minio:9000",
            # Инжестим «датой DAG» (ds) — формат YYYY-MM-DD
            "INGEST_DATE": "{{ ds }}",
        },
        get_logs=True,
        is_delete_operator_pod=True,
        in_cluster=True,
        # Если образ приватный в GHCR — раскомментируй и добавь секрет imagePull:
        # image_pull_secrets=[k8s.V1LocalObjectReference(name="ghcr-creds")],
    )
