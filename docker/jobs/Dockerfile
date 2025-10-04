# /docker/jobs/Dockerfile
# путь: /docker/jobs/Dockerfile
FROM python:3.11-slim

# Ставим системные утилиты для pyspark (java не нужен для клиентского submit)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates bash tini && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Библиотеки — синхронизированы с проектом
RUN pip install --no-cache-dir \
    pyspark==3.5.1 \
    mlflow==2.16.0 \
    boto3==1.34.162

WORKDIR /app
# Кладём текущие джобы (так мы сможем запускать их внутри контейнера при необходимости)
COPY jobs /app/jobs

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["python", "-c", "print('jobs image ready')"]
