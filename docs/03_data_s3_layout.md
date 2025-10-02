<!-- /docs/03_data_s3_layout.md -->
# S3 layout

- `rossmann-raw/` — исходные CSV из Kaggle (train/test/store), дата-штамп + источник.
- `rossmann-features/` — паркет/дельта-таблицы с фичами.
- `mlflow-artifacts/` — артефакты экспериментов (модели, логи, картинки).

## Именование файлов (raw)
- `rossmann-raw/train/ingest_date=YYYY-MM-DD/train.csv`
- `rossmann-raw/store/ingest_date=YYYY-MM-DD/store.csv`
