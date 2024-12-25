.PHONY: default main scratchpad checker graphviz clean
.SILENT:

default: scratchpad

main:
	mypy --strict main.py
	pypy3 main.py

scratchpad:
	mypy --strict scratchpad.py
	pypy3 scratchpad.py

checker:
	mypy --strict checker.py
	pypy3 checker.py

graphviz:
	mypy --strict graphviz.py
	pypy3 graphviz.py
	dot -Tx11 graph.dot

clean:
	rm -rf graph.dot .mypy_cache

