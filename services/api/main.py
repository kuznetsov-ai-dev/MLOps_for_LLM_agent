# путь: /services/api/main.py
import os
from typing import Dict, Any

import mlflow
import pandas as pd
from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter

# === Конфиги ===
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
# MLflow 2.16+: alias через @production
MODEL_URI = os.getenv("MODEL_URI", "models:/rossmann-baseline@production")
os.environ.setdefault(
    "MLFLOW_S3_ENDPOINT_URL",
    os.getenv("MLFLOW_S3_ENDPOINT_URL", "http://mlflow-minio:9000"),
)

app = FastAPI(title="rossmann-inference", version="0.1.0")
_model = None

# Кастомная метрика
PREDICTIONS_TOTAL = Counter(
    "rossmann_api_predictions_total",
    "Total number of prediction calls",
    ["status"],  # success | error
)

# ВАЖНО: instrument() — до старта приложения (добавляет middleware)
_instrumentator = Instrumentator().instrument(app)


@app.on_event("startup")
def load_model():
    global _model
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    _model = mlflow.pyfunc.load_model(MODEL_URI)
    # /metrics эндпоинт регистрируем уже на старте
    _instrumentator.expose(app, include_in_schema=False, endpoint="/metrics")


@app.get("/health")
def health():
    return {"status": "ok", "model_uri": MODEL_URI}


@app.post("/predict")
def predict(payload: Dict[str, Any]):
    if _model is None:
        raise HTTPException(503, "Model not loaded")
    if "records" not in payload or not isinstance(payload["records"], list):
        PREDICTIONS_TOTAL.labels("error").inc()
        raise HTTPException(400, "payload must contain 'records': list[dict]")

    df = pd.DataFrame(payload["records"])
    try:
        preds = _model.predict(df)
    except Exception as e:
        PREDICTIONS_TOTAL.labels("error").inc()
        raise HTTPException(400, f"prediction failed: {e}")

    PREDICTIONS_TOTAL.labels("success").inc()
    return {"predictions": [float(x) for x in preds]}
