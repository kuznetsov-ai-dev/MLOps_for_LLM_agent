# /infra/terraform/versions.tf
terraform {
  required_version = ">= 1.6.0"
  required_providers {
    yandex = {
      source  = "yandex-cloud/yandex"
      version = "~> 0.123"
    }
  }
}

provider "yandex" {
  # параметры берём из ENV (YC_*)
  cloud_id  = var.cloud_id
  folder_id = var.folder_id
  zone      = var.zone
}
