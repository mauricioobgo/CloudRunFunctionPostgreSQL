# Atlas Infra Project

This folder contains Atlas migration config and Terraform resources, separated from the FastAPI app.

## Cloud SQL target

- Instance connection name: `testing-atlas-setup:us-east4:atlas-instance-test`

## Local setup

```bash
cd atlas_infra
cp .env.example .env
export $(grep -v '^#' .env | xargs)
```

Install Atlas and provider:

```bash
atlas login
atlas provider install sqlalchemy
```

## Git workflow with Atlas

1. Create a feature branch.
2. Update models in `atlas_fastapi_sample/app/models.py` and/or role defaults in `atlas_infra/schema/roles.hcl`.
3. Create a migration:

```bash
cd atlas_infra
atlas migrate diff <migration_name> --env local
# or:
make migrate-create name=<migration_name>
```

4. Validate locally:

```bash
atlas migrate lint --env local --latest 1
# or:
make migrate-lint
```

5. Commit both app-model changes and generated files in `atlas_infra/migrations/`.
6. Open a PR.

PRs run `.github/workflows/atlas-ci.yml` to verify checksums and lint latest migration.

After merge to `master`, `.github/workflows/atlas-apply-cloudsql.yml` applies migrations to Cloud SQL through Cloud SQL Auth Proxy.

## Required GitHub repository secrets

- `GCP_SA_KEY`: service account JSON with Cloud SQL Client permissions.
- `DB_USER`: PostgreSQL user.
- `DB_PASSWORD`: PostgreSQL password.
- `DB_NAME`: PostgreSQL database name.

## Terraform named schemas

```bash
cd terraform
terraform init
terraform apply -var='db_url=postgres://postgres:postgres@localhost:5432/app_db'
```
