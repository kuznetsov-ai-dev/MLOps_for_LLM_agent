# путь: /services/api/main.py
import os
from typing import Dict, Any
import mlflow
from fastapi import FastAPI, HTTPException

# Конфиги из ENV
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
    global _model
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    _model = mlflow.pyfunc.load_model(MODEL_URI)


@app.get("/health")
def health():
    return {"status": "ok", "model_uri": MODEL_URI}


@app.post("/predict")
def predict(payload: Dict[str, Any]):
    if _model is None:
        raise HTTPException(503, "Model not loaded")
    if "records" not in payload or not isinstance(payload["records"], list):
        raise HTTPException(400, "payload must contain 'records': list[dict]")
    import pandas as pd

    df = pd.DataFrame(payload["records"])
    try:
        preds = _model.predict(df)
    except Exception as e:
        raise HTTPException(400, f"prediction failed: {e}")
    return {"predictions": list(map(float, preds))}
