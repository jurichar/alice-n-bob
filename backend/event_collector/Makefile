VENV=venv
PYTHON=python3

$(VENV):
	$(PYTHON) -m venv $(VENV)

install: $(VENV)
	$(VENV)/bin/pip install -r requirements.txt

clear:
	rm -rf $(VENV)

run: install
	$(VENV)/bin/uvicorn main:app --reload

test: install
	$(VENV)/bin/pytest tests.py
