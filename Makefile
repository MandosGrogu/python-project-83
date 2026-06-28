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

PORT ?= 8000
start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app