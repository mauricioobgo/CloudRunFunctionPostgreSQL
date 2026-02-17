.PHONY: migrate-create migrate-lint migrate-apply

migrate-create:
	@if [ -z "$(name)" ]; then echo "Usage: make migrate-create name=<migration_name>"; exit 1; fi
	atlas migrate diff $(name) --env local

migrate-lint:
	atlas migrate lint --env local --latest 1

migrate-apply:
	atlas migrate apply --env local
