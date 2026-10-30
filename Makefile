.PHONY: run clean
.SILENT:

VENV = venv
PYTHON = $(VENV)/bin/python3

run: $(VENV)/bin/activate
	$(PYTHON) a_maze_ing.py

$(VENV)/bin/activate:
	python3 -m venv $(VENV)

clean:
	find . -type d -name '__pycache__' -prune -exec rm -rf -- {} +
	rm -rf $(VENV)
	rm -rf result.txt
