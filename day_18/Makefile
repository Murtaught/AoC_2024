.PHONY: all
.SILENT:

all: Pipfile.lock
	./env.sh pipenv run mypy main.py
	./env.sh pypy3 main.py

cpython: Pipfile.lock
	./env.sh pipenv run python3 main.py

Pipfile.lock: Pipfile
	./env.sh pipenv install
