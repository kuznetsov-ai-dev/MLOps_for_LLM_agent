# /Makefile
PYTHON ?= python3.11
VENV ?= .venv
PIP := $(VENV)/bin/pip
PY := $(VENV)/bin/python
PRECOMMIT := $(VENV)/bin/pre-commit

.PHONY: help
help: ## показать команды
	@grep -E '^[a-zA-Z_\-]+:.*?##' Makefile | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2}'

.PHONY: venv
venv: ## создать venv
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip

.PHONY: deps
deps: venv ## установить зависимости
	$(PIP) install -r requirements-dev.txt

.PHONY: precommit-install
precommit-install: ## установить хуки pre-commit
	$(PRECOMMIT) install

.PHONY: format
format: ## форматировать black/ruff
	$(VENV)/bin/black .
	$(VENV)/bin/ruff check --fix .

.PHONY: check
check: ## проверить линтер
	$(VENV)/bin/ruff check .


# /Makefile (добавить блок)
.PHONY: tf-init
tf-init: ## terraform init (local backend)
	cd infra/terraform && terraform init

.PHONY: tf-validate
tf-validate: ## terraform validate
	cd infra/terraform && terraform validate

.PHONY: tf-plan
tf-plan: ## terraform plan (prod)
	cd infra/terraform && terraform plan -var-file=envs/prod/terraform.tfvars


.PHONY: docker-api
docker-api: ## локально собрать API образ
	docker build -t local/rossmann-api:dev -f docker/api/Dockerfile .

.PHONY: docker-jobs
docker-jobs: ## локально собрать jobs образ
	docker build -t local/rossmann-jobs:dev -f docker/jobs/Dockerfile .
