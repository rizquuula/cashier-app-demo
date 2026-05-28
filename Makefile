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

.DEFAULT_GOAL := help
.PHONY: help opencode opencode-debug sandbox-clean
