# путь: /docker/api/Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Нужны зависимости для mlflow-инференса и работы с S3 (MinIO)
RUN pip install --no-cache-dir \
    fastapi==0.115.0 \
    uvicorn[standard]==0.30.6 \
    mlflow==2.16.0 \
    pandas==2.2.2 \
    scikit-learn==1.5.2 \
    boto3==1.34.162

COPY services/api /app

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
