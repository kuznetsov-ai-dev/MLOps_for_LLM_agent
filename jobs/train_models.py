# jobs/train_models.py
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import mlflow
import mlflow.sklearn

# MLflow сервер (локальный)
mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("rossmann-baseline")

# Подключение к MinIO из хоста
MINIO_USER = os.getenv("MINIO_ROOT_USER", "mlops_user")
MINIO_PASS = os.getenv("MINIO_ROOT_PASSWORD", "mlops_password_ChangeMe123")

# storage_options для s3fs (MinIO по http, path-style)
STO = {
    "key": MINIO_USER,
    "secret": MINIO_PASS,
    "client_kwargs": {"endpoint_url": "http://127.0.0.1:9000"},
}

# Читаем фичи, собранные Spark’ом
FEATURES_PATH = "s3://rossmann-features/demo_features/"

print("[*] Reading features from:", FEATURES_PATH)
df = pd.read_parquet(FEATURES_PATH, storage_options=STO)

print("[*] Columns:", list(df.columns))
target = "Sales"
if target not in df.columns:
    raise ValueError(f"Column '{target}' not found. Available: {list(df.columns)}")

# Простейшие фичи (можешь расширять позже)
cand = [c for c in ["Store", "DayOfWeek", "Promo", "Year", "Month"] if c in df.columns]
X = df[cand].fillna(0)
y = df[target].astype("float32")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

with mlflow.start_run(run_name="baseline_linear_regression"):
    model = LinearRegression()
    model.fit(X_train, y_train)

    pred = model.predict(X_test)
    rmse = mean_squared_error(y_test, pred, squared=False)
    mae = mean_absolute_error(y_test, pred)
    r2 = r2_score(y_test, pred)

    mlflow.log_params({"model": "LinearRegression", "features": ",".join(cand)})
    mlflow.log_metrics({"rmse": rmse, "mae": mae, "r2": r2})

    # Сохраняем модель в MLflow (как артефакт)
    mlflow.sklearn.log_model(model, artifact_path="model")

    print(f"[✓] Logged to MLflow: rmse={rmse:.3f}, mae={mae:.3f}, r2={r2:.3f}")
    print("[✓] Run URL:", mlflow.get_tracking_uri())
