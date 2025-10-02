# /scripts/minio-init.sh
#!/usr/bin/env sh
set -e

# Ждём MinIO
until (mc alias set local http://minio:9000 "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD") do
  echo "Waiting for MinIO..."
  sleep 2
done

# Создаём бакеты (идемпотентно)
mc mb -p local/rossmann-raw || true
mc mb -p local/rossmann-features || true
mc mb -p local/mlflow-artifacts || true

# Права public list отключены — приватно по умолчанию
mc anonymous set none local/rossmann-raw || true
mc anonymous set none local/rossmann-features || true
mc anonymous set none local/mlflow-artifacts || true

echo "[✓] MinIO initialized: rossmann-raw, rossmann-features, mlflow-artifacts"
