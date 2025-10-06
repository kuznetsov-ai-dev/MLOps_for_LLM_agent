variable "cloud_id" {
  type = string
}

variable "folder_id" {
  type = string
}

variable "zone" {
  type    = string
  default = "ru-central1-a"
}

variable "network_name" {
  type    = string
  default = "mlops-net"
}

variable "subnet_cidr" {
  type    = string
  default = "10.10.0.0/24"
}

variable "bucket_prefix" {
  type    = string
  default = "rossmann"
}

variable "registry_name" {
  type    = string
  default = "mlops-registry"
}

variable "sa_name" {
  type    = string
  default = "sa-mlops"
}
