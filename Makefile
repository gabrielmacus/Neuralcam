.PHONY: help install install-dev check type-check lint format format-check test test-verbose test-coverage test-unit test-watch clean dev-setup

help: ## Muestra este mensaje de ayuda
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Instala las dependencias del proyecto
	pip install -e .

install-dev: ## Instala las dependencias de desarrollo
	pip install -e ".[dev]"

check: type-check lint test ## Ejecuta todas las verificaciones (type-check + lint + test)

type-check: ## Ejecuta Pyright para verificación de tipos
	pyright src/ tests/

lint: ## Ejecuta flake8 para verificación de estilo
	flake8 --max-line-length=100 --extend-ignore=E203,W503 src/ tests/

format: ## Formatea el código usando black e isort
	black src/ tests/
	isort src/ tests/

format-check: ## Verifica si el código está formateado correctamente
	black --check src/ tests/
	isort --check-only src/ tests/

test: ## Ejecuta todos los tests
	python3 -m pytest

test-verbose: ## Ejecuta todos los tests con salida detallada
	python3 -m pytest -v

test-coverage: ## Ejecuta tests con reporte de cobertura
	python3 -m pytest --cov=src --cov-report=html --cov-report=term

test-unit: ## Ejecuta solo tests unitarios
	python3 -m pytest tests/ -k "not integration and not e2e" -s

test-integration: ## Ejecuta solo tests de integración
	python3 -m pytest tests/ -k "integration" -s

test-e2e: ## Ejecuta solo tests de e2e
	python3 -m pytest tests/ -k "e2e" -s

clean: ## Limpia archivos temporales y caches
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

dev-setup: install-dev ## Configuración completa del entorno de desarrollo
	@echo "Entorno de desarrollo configurado correctamente"
	@echo "Ejecuta 'make check' para verificar el código y tests"
	@echo "Ejecuta 'make test' para ejecutar solo los tests" 