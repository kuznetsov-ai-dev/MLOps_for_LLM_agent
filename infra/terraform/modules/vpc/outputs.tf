# /infra/terraform/modules/vpc/outputs.tf
output "network_id" { value = yandex_vpc_network.this.id }
output "subnet_id"  { value = yandex_vpc_subnet.this.id }
output "sg_id"      { value = yandex_vpc_security_group.default.id }
