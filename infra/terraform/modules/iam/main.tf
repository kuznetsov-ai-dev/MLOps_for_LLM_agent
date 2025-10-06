resource "yandex_iam_service_account" "sa" {
  name = var.sa_name
}

resource "yandex_resourcemanager_folder_iam_member" "sa_obj_storage" {
  folder_id = var.folder_id
  role      = "storage.admin"
  member    = "serviceAccount:${yandex_iam_service_account.sa.id}"
}

resource "yandex_resourcemanager_folder_iam_member" "sa_cr_admin" {
  folder_id = var.folder_id
  role      = "container-registry.admin"
  member    = "serviceAccount:${yandex_iam_service_account.sa.id}"
}

resource "yandex_iam_service_account_static_access_key" "s3" {
  service_account_id = yandex_iam_service_account.sa.id
  description        = "access for object storage (S3)"
}

output "sa_id" {
  value = yandex_iam_service_account.sa.id
}

output "s3_access_key" {
  value = yandex_iam_service_account_static_access_key.s3.access_key
}

output "s3_secret_key" {
  value     = yandex_iam_service_account_static_access_key.s3.secret_key
  sensitive = true
}
