variable "bucket_prefix" { type = string }

variable "s3_access_key" { type = string }

variable "s3_secret_key" {
  type      = string
  sensitive = true
}
