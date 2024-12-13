.PHONY: all
.SILENT:

all: Pipfile.lock
	./env.sh pipenv run python main.py

Pipfile.lock: Pipfile
	./env.sh pipenv install

