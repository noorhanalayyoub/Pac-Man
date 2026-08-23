PYTHON := python3
MAZE_WHEEL := ./mazegenerator-2.1.0-py3-none-any.whl

.PHONY: install run debug clean lint lint-strict

install:
	$(PYTHON) -m pip install pygame flake8 mypy $(MAZE_WHEEL)

run:
	$(PYTHON) menu.py

debug:
	$(PYTHON) -m pdb menu.py

clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache
	rm -rf testing/__pycache__ mazegenerator-2.1.0-py3-none-any/mazegenerator/__pycache__
	rm -f *.pyc testing/*.pyc

lint:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy . --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy . --strict
