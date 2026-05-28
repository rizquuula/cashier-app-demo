SHELL := /bin/bash
OPENCODE := /root/.opencode/bin/opencode
SANDBOX := $(CURDIR)/.sandbox

SANDBOX_ENV := \
	HOME=$(SANDBOX) \
	XDG_CONFIG_HOME=$(SANDBOX)/.config \
	XDG_DATA_HOME=$(SANDBOX)/.local/share \
	XDG_CACHE_HOME=$(SANDBOX)/.cache \
	XDG_STATE_HOME=$(SANDBOX)/.local/state \
	OPENCODE_CONFIG_DIR=$(SANDBOX)/.config/opencode \
	OPENCODE_DISABLE_CLAUDE_CODE=1 \
	OPENCODE_DISABLE_EXTERNAL_SKILLS=1

help:
	@echo "Available targets:"
	@echo "  opencode        - Run opencode in an isolated \$$HOME sandbox"
	@echo "  opencode-debug  - Show resolved config + skills inside the sandbox"
	@echo "  sandbox-clean   - Delete the .sandbox directory"
	@echo "  help            - Show this help message (default)"

$(SANDBOX):
	mkdir -p $(SANDBOX)/.config/opencode \
	         $(SANDBOX)/.local/share/opencode \
	         $(SANDBOX)/.cache/opencode \
	         $(SANDBOX)/.local/state/opencode \
	         $(SANDBOX)/.claude
	@if [ ! -f $(CURDIR)/AGENTS.md ]; then touch $(CURDIR)/AGENTS.md; fi
	@if [ ! -f $(CURDIR)/CLAUDE.md ]; then touch $(CURDIR)/CLAUDE.md; fi
	@if [ ! -f $(SANDBOX)/.config/opencode/opencode.json ]; then \
		echo '{ "$$schema": "https://opencode.ai/config.json" }' \
			> $(SANDBOX)/.config/opencode/opencode.json; \
	fi

opencode: $(SANDBOX)
	$(SANDBOX_ENV) $(OPENCODE) $(CURDIR)

opencode-debug: $(SANDBOX)
	@echo "=== debug paths ==="
	@$(SANDBOX_ENV) $(OPENCODE) debug paths
	@echo "=== debug config ==="
	@$(SANDBOX_ENV) $(OPENCODE) debug config
	@echo "=== debug skill ==="
	@$(SANDBOX_ENV) $(OPENCODE) debug skill

sandbox-clean:
	rm -rf $(SANDBOX)

VENV := $(CURDIR)/venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

$(VENV):
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

run: $(VENV)
	$(PYTHON) app.py

init-db: $(VENV)
	$(PYTHON) -c "from app import create_app; from models import db; app = create_app(); app.app_context().push(); db.create_all(); print('DB initialized')"

seed: $(VENV)
	$(PYTHON) seed.py

db-clean:
	rm -rf $(CURDIR)/instance

.DEFAULT_GOAL := help
.PHONY: help opencode opencode-debug sandbox-clean run init-db seed db-clean
