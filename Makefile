#Makefile

install:
	uv sync

dev:
	uv run flask --debug --app page_analyzer:app run

uv_build:
	uv build

build:
	./build.sh

render-start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

package-install:
	uv tool install dist/*.whl

lint:
	uv run ruff check

check: 
	test lint

test-coverage:
	uv run pytest --cov=page_analyzer --cov-report xml

PORT ?= 8000
start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

setup:
	install