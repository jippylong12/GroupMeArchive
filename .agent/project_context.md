# Project Context: Python Script & CLI (Hypermodern)

## 1. Project Architecture
**Philosophy:** "Hypermodern Python." Modular, type-safe, testable.
**Critical Rule:** NO MONOLITHS. Logic must be split into small, single-purpose files within `src/`.

### Directory Structure (Src Layout)
The `src/` layout is mandatory. Tests run against the installed package.

```text
project_root/
├── pyproject.toml       # SINGLE source of truth (Deps, Config, Build)
├── uv.lock              # Lockfile (if using uv)
├── .python-version      # Python version pin
├── README.md
├── src/
│   └── project_name/    # Actual package
│       ├── __init__.py
│       ├── __main__.py  # Entry point (allows `python -m project_name`)
│       ├── cli.py       # Typer/Click definition (Interface Layer)
│       ├── core.py      # Business logic orchestration
│       ├── config.py    # Pydantic settings
│       └── utils/       # Small, pure functions
│           ├── __init__.py
│           └── fs.py
└── tests/
    ├── __init__.py
    ├── conftest.py      # Pytest fixtures
    └── test_core.py
```

## 2. Tech Stack & Standards
* **Package Manager:** `uv` (preferred) or `poetry`. (NO `pip` + `requirements.txt`).
* **Linter/Formatter:** `ruff` (Line length 88, double quotes, strict import sorting).
* **Type Checking:** `mypy` or `pyright` (Strict mode).
* **CLI Framework:** `typer` (Standard) or `click`.
* **Configuration:** `pydantic-settings`.

## 3. Immutable Constraints (The "Laws")
* **Modularity Rule:** Files must be small (<200 lines). If a file grows larger, split it.
* **Separation Rule:** `cli.py` handles arguments/printing ONLY. It **never** contains business logic. It imports from `core.py`.
* **Config Rule:** Do not use `os.getenv` directly in logic files. Use `config.py` with `pydantic-settings`.
* **Exception Rule:** Never catch bare `Exception`. Use custom exceptions defined in `exceptions.py`.
* **Testing Rule:** 90%+ branch coverage. **Never** make real network calls in tests (use `pytest-mock`).

## 4. Patterns & Recipes (The "How-To")

### The "Runnable Module" Pattern
* **Rule:** The script is executed via `__main__.py` to allow `python -m project_name`.
* **Snippet (`src/project_name/__main__.py`):**
    ```python
    from .cli import app

    if __name__ == "__main__":
        app()
    ```

### Dependency Injection Pattern
* **Bad:** Instantiating DB connections globally.
* **Good:** Functions accept dependencies as arguments.
    ```python
    # core.py
    def process_data(data: list, db_conn: Connection) -> None:
        ...
    ```

## 5. Agent Workflow
1.  **Init:** If `pyproject.toml` is missing, generate it with `uv init`.
2.  **Code:** When asked to write a script, immediately structure it into `src/project_name/`. **Do not** dump code into a root `script.py`.
3.  **Refactor:** If you see a function with >3 branches or >20 lines, suggest extracting a helper function.
4.  **Docstrings:** Apply Google Style docstrings to all public modules/functions.