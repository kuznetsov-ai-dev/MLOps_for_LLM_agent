#!/bin/sh
set -e

mc alias set local http://minio:9000 "${MINIO_ROOT_USER}" "${MINIO_ROOT_PASSWORD}"

# создаём бакет для артефактов MLflow (повторный вызов не упадёт)
mc mb -p local/mlflow-artifacts || true

# (опционально) сделать артефакты читаемыми анонимно (для локалки ок)
mc anonymous set download local/mlflow-artifacts || true
