# /infra/terraform/main.tf
module "vpc" {
  source       = "./modules/vpc"
  network_name = var.network_name
  zone         = var.zone
  subnet_cidr  = var.subnet_cidr
}

module "iam" {
  source    = "./modules/iam"
  sa_name   = var.sa_name
  folder_id = var.folder_id
}

module "object_storage" {
  source        = "./modules/object_storage"
  bucket_prefix = var.bucket_prefix
  s3_access_key = module.iam.s3_access_key
  s3_secret_key = module.iam.s3_secret_key
}

module "cr" {
  source        = "./modules/container_registry"
  registry_name = var.registry_name
}
