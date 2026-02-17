# schema/roles.hcl
schema "app" {}

role "app_user" {
  login    = true
  password = "password123"
}

grant_usage {
  to = role.app_user
  on = schema.app
}
