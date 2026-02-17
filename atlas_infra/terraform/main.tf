terraform {
  required_providers {
    atlas = {
      source  = "ariga/atlas"
      version = "~> 0.8"
    }
  }
}

provider "atlas" {}

variable "db_url" {
  description = "Target PostgreSQL URL (without schema in search_path)"
  type        = string
  sensitive   = true
}

variable "tenant_schemas" {
  description = "Schemas to ensure exist in shared PostgreSQL database"
  type        = set(string)
  default     = ["app", "reporting"]
}

locals {
  managed_tables_exclude = [
    "table.users",
    "table.posts",
  ]
}

data "atlas_schema" "tenant" {
  for_each = var.tenant_schemas

  hcl = <<-EOT
    schema "${each.key}" {}
  EOT
}

resource "atlas_schema" "tenant" {
  for_each = var.tenant_schemas

  url     = var.db_url
  src     = data.atlas_schema.tenant[each.key].url
  exclude = local.managed_tables_exclude
  dev_url = "docker://postgres/16/dev?search_path=${each.key}"
  tx_mode = "none"
}
