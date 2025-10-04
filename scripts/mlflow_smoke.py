# scripts/mlflow_smoke.py
import os
import time
import tempfile
import mlflow

# 1) Куда постучаться (MLflow UI/REST)
mlflow.set_tracking_uri("http://127.0.0.1:5000")

# 2) Эксперимент (создастся, если нет)
experiment_name = "smoke-local"
mlflow.set_experiment(experiment_name)

with mlflow.start_run(run_name=f"smoke_{int(time.time())}"):
    # логируем параметры/метрики
    mlflow.log_param("stage", "pre-train")
    mlflow.log_metric("ping", 1.0)

    # создаём и логируем артефакт
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "hello.txt")
        with open(p, "w", encoding="utf-8") as f:
            f.write("hello, mlflow + minio!\n")
        mlflow.log_artifact(p, artifact_path="artifacts")

print("✓ Smoke done. Check MLflow UI and MinIO bucket: mlflow-artifacts")
