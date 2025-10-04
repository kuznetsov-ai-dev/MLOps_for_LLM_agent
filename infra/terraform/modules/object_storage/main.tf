# /infra/terraform/modules/object_storage/main.tf
resource "yandex_storage_bucket" "raw" {
  bucket     = "${var.bucket_prefix}-raw"
  access_key = var.s3_access_key
  secret_key = var.s3_secret_key
}

resource "yandex_storage_bucket" "features" {
  bucket     = "${var.bucket_prefix}-features"
  access_key = var.s3_access_key
  secret_key = var.s3_secret_key
}

resource "yandex_storage_bucket" "mlflow" {
  bucket     = "mlflow-artifacts-${var.bucket_prefix}"
  access_key = var.s3_access_key
  secret_key = var.s3_secret_key
}

output "bucket_raw"      { value = yandex_storage_bucket.raw.bucket }
output "bucket_features" { value = yandex_storage_bucket.features.bucket }
output "bucket_mlflow"   { value = yandex_storage_bucket.mlflow.bucket }
