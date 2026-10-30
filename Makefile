.PHONY: run clean install debug lint lint-strict execute re
.SILENT:

# run
NAME = a_maze_ing.py
VENV = venv
PYTHON = $(VENV)/bin/python3
PYTHON_FLAG = -m
ARGS ?= config.txt

# install
PIP = pip
INSTALL = install
FREEZE = freeze
REQUIREMENTS_FILE = requirements.txt
DEPENDENCES = mypy flake8 pudb

# lint
MYPY = mypy
MYPY_FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
FLAKE8 = flake8
STRICT = --strict
FILES = Model/*.py Utils/*.py a_maze_ing.py

# debug
DEBUG = pudb

# format
CLEAR = clear
ECHO = echo

# clean
RM = rm
RMFLAGS = -rf
OUTPUT_FILE := $(shell grep '^OUTPUT_FILE=' $(ARGS) | sed 's/^OUTPUT_FILE=//')

# execute
EXECUTE_FILE = a-maze-ing.sh
BASH = bash


install: $(VENV)/bin/activate
	$(PYTHON) $(PYTHON_FLAG) $(PIP) $(INSTALL) $(DEPENDENCES)
	$(PYTHON) $(PYTHON_FLAG) $(PIP) $(FREEZE) > $(REQUIREMENTS_FILE)
	$(CLEAR)


run: $(VENV)/bin/activate install
	$(PYTHON) $(NAME) $(ARGS)


debug: $(VENV)/bin/activate install
	$(PYTHON) $(PYTHON_FLAG) $(DEBUG) $(NAME) $(ARGS)


lint: $(VENV)/bin/activate install
	$(ECHO) "### MYPY ###"
	$(PYTHON) $(PYTHON_FLAG) $(MYPY) $(FILES) $(MYPY_FLAGS)
	$(ECHO) "### FLAKE8 ###"
	$(PYTHON) $(PYTHON_FLAG) $(FLAKE8) $(FILES)


lint-strict: $(VENV)/bin/activate install
	$(ECHO) "### MYPY ###"
	$(PYTHON) $(PYTHON_FLAG) $(MYPY) $(FILES) $(MYPY_FLAGS) $(STRICT)
	$(ECHO) "### FLAKE8 ###"
	$(PYTHON) $(PYTHON_FLAG) $(FLAKE8) $(FILES)


execute: $(VENV)/bin/activate install
	$(BASH) $(EXECUTE_FILE)

$(VENV)/bin/activate:
	python3 $(PYTHON_FLAG) venv $(VENV)


clean:
	find . -type d -name '__pycache__' -prune -exec $(RM) $(RMFLAGS) -- {} +
	find . -type d -name '.mypy_cache' -prune -exec $(RM) $(RMFLAGS) -- {} +
	$(RM) $(RMFLAGS) $(VENV)
	$(RM) $(RMFLAGS) $(OUTPUT_FILE)


re: clean run