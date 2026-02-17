variable "db_url" {
  type    = string
  default = getenv("DB_URL")
}

variable "dev_url" {
  type    = string
  default = getenv("DEV_URL")
}

data "external_schema" "sqlmodel" {
  program = [
    "python3",
    "../atlas_fastapi_sample/atlas_loader.py"
  ]
}

env "local" {
  url = var.db_url
  dev = var.dev_url
  src = data.external_schema.sqlmodel.url
  
  # Tell Atlas to only diff the 'app' schema
  schemas = ["app"]

  migration {
    dir = "file://migrations"
  }

  format {
        migrate {
            diff = "{{ sql . \"  \" }}"
        }
    }
}