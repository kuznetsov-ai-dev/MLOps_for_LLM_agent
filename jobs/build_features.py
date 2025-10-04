# jobs/build_features.py
import os
import traceback
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, month, dayofweek, to_date

S3_ENDPOINT = os.getenv("S3_ENDPOINT", "http://minio:9000")
ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID", "mlops_user")
SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "mlops_password_ChangeMe123")

spark = (
    SparkSession.builder.appName("BuildFeatures")
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    .config("spark.hadoop.fs.s3a.endpoint", S3_ENDPOINT)
    .config("spark.hadoop.fs.s3a.access.key", ACCESS_KEY)
    .config("spark.hadoop.fs.s3a.secret.key", SECRET_KEY)
    .config("spark.hadoop.fs.s3a.path.style.access", "true")
    .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")
    .config("spark.hadoop.fs.s3a.fast.upload", "true")
    .getOrCreate()
)


def main():
    # Пути под твою текущую структуру с ingest_date=YYYY-MM-DD
    train_path = "s3a://rossmann-raw/train/ingest_date=*/train.csv"
    store_path = "s3a://rossmann-raw/store/ingest_date=*/store.csv"

    print(">>> Sanity read 1 row from:", train_path)
    head = spark.read.csv(train_path, header=True, inferSchema=True).limit(1)
    print("  head rows:", head.count())

    print(">>> Reading train & store")
    train = spark.read.csv(train_path, header=True, inferSchema=True)
    store = spark.read.csv(store_path, header=True, inferSchema=True)

    # Простейший джойн (если понадобится)
    if "Store" in train.columns and "Store" in store.columns:
        df = train.join(store, on="Store", how="left")
    else:
        df = train

    print(">>> Feature engineering")
    df = df.withColumn("Date", to_date(col("Date")))
    df_feat = (
        df.withColumn("Year", year(col("Date")))
        .withColumn("Month", month(col("Date")))
        .withColumn("DayOfWeek", dayofweek(col("Date")))
    )

    out_path = "s3a://rossmann-features/demo_features"
    print(">>> Writing parquet to:", out_path)
    df_feat.write.mode("overwrite").parquet(out_path)
    print("✓ Done write")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("!! ERROR in job:", e)
        traceback.print_exc()
        raise
    finally:
        spark.stop()
