# Repository Guidelines

## Project Structure & Module Organization
- `math_cli.py` is the CLI entry point for running operations directly from the terminal.
- `cli/` hosts argument parsing (`command_parser.py`) and interactive session logic (`interactive_mode.py`).
- `core/` contains the plugin base class and manager layer that orchestrate discovery and execution.
- `plugins/` ships built-in math operations and a template for extending the toolset.
- `utils/` offers shared helpers and ephemeral session history utilities.
- `tests/` mirrors the package layout; add new test modules alongside the feature area they cover.

## Build, Test, and Development Commands
- `python3 math_cli.py add 2 3` — run a specific operation; swap `add` for any available command.
- `python3 math_cli.py --list-plugins` — enumerate built-in and discovered plugin operations.
- `python3 math_cli.py -i` — launch interactive mode for multi-step workflows.
- `python3 math_cli.py --plugin-dir /path/to/plugins ...` — load external plugins; add custom directory to `PYTHONPATH` when developing locally.
- `pytest -q` — execute the automated test suite with concise output.

## Coding Style & Naming Conventions
- Target Python 3 with 4-space indentation and PEP 8-friendly formatting; prefer descriptive names.
- Use type hints in public APIs (`List[str]`, `Dict[str, Any]`) when they clarify behavior.
- Plugins subclass `core.base_operations.MathOperation`; class names use `PascalCase`, command names stay `snake_case` (e.g., `HypotenuseOperation` → `hypotenuse`).

## Testing Guidelines
- Write pytest tests under `tests/`, mirroring source paths (`tests/test_plugin_manager.py`).
- Name tests `test_<module>_<behavior>()` and assert both success paths and validation errors.
- Run `pytest -q` before raising PRs; include regression coverage for new plugins or CLI flags.

## Commit & Pull Request Guidelines
- Craft imperative, ≤72 character commit subjects (e.g., `add: include --list-plugins flag in help output`).
- Detail rationale or edge cases in the body when the change is non-trivial.
- PRs should summarize scope, link relevant issues, share CLI before/after snippets, and mention new tests or docs updates.

## Security & Configuration Tips
- Only load plugins from directories you trust; third-party code runs in-process.
- Validate user-supplied arguments inside `execute()` and raise clear `ValueError`s on invalid input.
- Interactive history lives in-memory only; avoid storing secrets in command history.
