.PHONY: help
help:
	@echo "USAGE"
	@echo "  make <commands>"
	@echo ""
	@echo "AVAILABLE COMMANDS"
	@echo "  run		Start the bot"
	@echo "  lint		Reformat code"


.PHONY:	blue
blue:
	poetry run blue src/

.PHONY:	mypy
mypy:
	poetry run mypy --strict --pretty --explicit-package-bases --install-types src/

.PHONY: isort
isort:
	poetry run isort src/

.PHONY: ruff
ruff:
	poetry run ruff check src/ --fix --respect-gitignore

.PHONY: lint
lint: blue isort ruff mypy

.PHONY: run
run:
	migrate
	poetry run python -m src.bot


REQUIREMENTS_FILE := requirements.txt

# Alembic utils
.PHONY: generate
generate:
	source .env
	poetry run alembic revision --m="$(NAME)" --autogenerate

.PHONY: migrate
migrate:
	source .env
	poetry run alembic upgrade head
