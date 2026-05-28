---
name: python-programming
description: Use when writing Python code — implement features, fix bugs, or refactor. Covers project structure, modular design, pytest, TDD, integration tests, and e2e tests.
---

# Python Programming Skill

When writing or modifying Python code, follow these conventions and practices.

## Project Structure

```
project/
├── src/
│   └── package_name/
│       ├── __init__.py
│       ├── main.py
│       ├── models/
│       ├── services/
│       └── utils/
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_models.py
│   │   └── test_services.py
│   ├── integration/
│   │   ├── __init__.py
│   │   └── test_api.py
│   └── e2e/
│       ├── __init__.py
│       └── test_workflow.py
├── pyproject.toml
├── pytest.ini
└── conftest.py
```

- Use `src/` layout to separate application code from tests
- One class of fixtures per `conftest.py` at the appropriate scope level
- Keep `__init__.py` minimal (or empty) — no runtime side effects

## Modular Design

- Favor pure functions and composition over deep inheritance
- One distinct responsibility per module — if a module has "and" in its description, split it
- Use dependency injection for testability (pass dependencies, don't import them globally)
- Type-annotate all public functions and methods
- Use `dataclasses` for simple data containers, `pydantic` for validated config/data
- Avoid global state — use context managers, factories, or dependency injection containers
- Keep functions small (under 30 lines typically) — extract helper functions

## Test-Driven Development (TDD)

Always follow the Red-Green-Refactor cycle:

```
1. RED   — Write a failing test first (define expected behavior)
2. GREEN — Write the minimum code to make it pass
3. REFACTOR — Clean up both test and implementation
```

- Write the **test first** before any implementation code
- The test should fail initially (confirm it's testing something real)
- After it passes, refactor before writing the next test
- Each test should verify **one behavior**

## pytest Conventions

### Configuration (`pytest.ini` or `pyproject.toml`)
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short --strict-markers
```

### Test patterns
```python
# Arrange — set up test data and mocks
# Act — call the function under test
# Assert — verify the result
```

- Use `tmp_path` fixture for file I/O tests (not `tempfile` directly)
- Use `monkeypatch` for environment variable overrides
- Use `pytest.fixture` for shared setup; scope appropriately (`session`, `module`, `function`)
- Use `pytest.mark.parametrize` for testing multiple inputs
- Use `pytest.approx` for float comparisons
- Name tests descriptively: `test_<function>_<scenario>_<expected_result>`

### Fixtures guidelines
- Fixtures in `conftest.py` at the appropriate level (root for global, per-directory for scoped)
- `conftest.py` files should contain **only** fixtures, hooks, and configuration — no test functions

### Mocking
- Use `unittest.mock` (or `pytest-mock`'s `mocker` fixture if available)
- Mock at the **source** of the import, not the destination
- Prefer `mocker.spy` over mocks when you need to observe but still call through
- Avoid over-mocking — integration tests should use real implementations where practical

## Test Categories

### Unit Tests (`tests/unit/`)
- Test a single function, class, or module in isolation
- All external dependencies are mocked
- Fast (milliseconds per test)
- No network, database, or filesystem I/O (except `tmp_path`)

### Integration Tests (`tests/integration/`)
- Test how modules work together
- May use real databases (use test containers or in-memory alternatives)
- May hit real APIs (use sandbox/test environments)
- Slower than unit tests (seconds per test)

### End-to-End Tests (`tests/e2e/`)
- Test the full system from the user's perspective
- Spin up the real application, hit real endpoints
- Use tools like `pytest-playwright` for UI, `httpx` for API, or custom test harnesses
- Slowest — run separately from unit/integration suites

### Running tests
```bash
# Run all tests
pytest

# Run specific category
pytest tests/unit/
pytest tests/integration/
pytest tests/e2e/

# Run with coverage
pytest --cov=src/ --cov-report=term-missing

# Run a specific test
pytest tests/unit/test_models.py::test_user_creation
```

## Code Quality

- Format: `ruff format .`
- Lint: `ruff check .` (or `ruff check --fix .`)
- Type-check: `mypy src/`
- All three must pass cleanly before considering work done
- Run tests after every meaningful change, not just at the end

## Type Annotations

```python
from collections.abc import Sequence
from typing import Any, Optional

def process_items(items: Sequence[str], max_count: int = 10) -> list[dict[str, Any]]:
    ...
```

- Use `list[X]`, `dict[K, V]`, `set[X]`, `tuple[X, ...]` (Python 3.9+)
- Use `Optional[X]` or `X | None` (Python 3.10+)
- Use `collections.abc` for generic container types (`Sequence`, `Mapping`, etc.)
- Use `Self` return type for class methods returning `self` (Python 3.11+)
- Use `TypeVar` and `Generic` for reusable generic functions/classes
- Annotate `__init__` return type as `None`
