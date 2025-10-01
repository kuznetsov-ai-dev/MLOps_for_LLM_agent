<!-- /docs/02_arch_overview.md -->
# Архитектурный обзор (High-Level)

## Потоки
1) Данные → S3 (raw) → Spark ETL → S3 (features)
2) Обучение в Spark → MLflow (runs, registry)
3) CI/CD: Docker → YC Container Registry → k8s
4) API (FastAPI) → модель из MLflow Registry
5) Airflow DAGs: фичи, переобучение, батч-прогноз
6) Мониторинг: Prometheus+Grafana (тех + ML-метрики)
7) LLM-агент: объяснения и рекомендации
