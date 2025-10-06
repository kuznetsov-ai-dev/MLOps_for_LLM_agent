# /infra/terraform/modules/container_registry/main.tf
resource "yandex_container_registry" "this" {
  name = var.registry_name
}

output "registry_id"   { value = yandex_container_registry.this.id }
output "registry_name" { value = yandex_container_registry.this.name }
