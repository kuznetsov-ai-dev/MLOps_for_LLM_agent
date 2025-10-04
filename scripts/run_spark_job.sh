#!/usr/bin/env bash
set -euo pipefail

APP_IN_CONTAINER=${1:-/workspace/jobs/build_features.py}
IVY_DIR="/tmp/ivy"

docker compose -f docker-compose.yml -f docker-compose.spark.yml exec spark-master bash -lc "
  mkdir -p ${IVY_DIR}/cache &&
  /opt/spark/bin/spark-submit \
    --master spark://spark-master:7077 \
    --conf spark.jars.ivy=${IVY_DIR} \
    --packages org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.367 \
    ${APP_IN_CONTAINER}
"
