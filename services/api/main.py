# путь: /services/api/main.py
from typing import Dict, Any
import os

import mlflow
import pandas as pd
from fastapi import FastAPI, HTTPException

# Конфиги из ENV (k8s их задаёт в деплое)
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
MODEL_URI = os.getenv("MODEL_URI", "models:/rossmann-baseline/1")
os.environ.setdefault(
    "MLFLOW_S3_ENDPOINT_URL",
    os.getenv("MLFLOW_S3_ENDPOINT_URL", "http://mlflow-minio:9000"),
)

app = FastAPI(title="rossmann-inference", version="0.1.0")
_model = None


@app.on_event("startup")
def load_model():
    """Ленивая загрузка модели при старте приложения."""
    global _model
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    _model = mlflow.pyfunc.load_model(MODEL_URI)


@app.get("/health")
def health():
    return {"status": "ok", "model_uri": MODEL_URI}


@app.post("/predict")
def predict(payload: Dict[str, Any]):
    if _model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    if "records" not in payload or not isinstance(payload["records"], list):
        raise HTTPException(
            status_code=400, detail="payload must contain 'records': list[dict]"
        )

    df = pd.DataFrame(payload["records"])
    try:
        preds = _model.predict(df)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"prediction failed: {e}")

    # mlflow.pyfunc может вернуть numpy-тип — приводим к float для JSON
    return {"predictions": [float(x) for x in preds]}
