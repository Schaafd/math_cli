# Repository Guidelines

## Project Structure & Module Organization
- `math_cli.py`: Main entry point (CLI).
- `cli/`: Argument parsing and interactive mode (`command_parser.py`, `interactive_mode.py`).
- `core/`: Plugin base and manager (`base_operations.py`, `plugin_manager.py`).
- `plugins/`: Built-in operations and a template (`core_math.py`, `plugin_template.py`).
- `utils/`: Helpers and session history (`helpers.py`, `history.py`).
- `docs/`: Architecture and flow references.

## Build, Test, and Development Commands
- Run an operation: `python3 math_cli.py add 2 3`.
- List available operations: `python3 math_cli.py --list-plugins`.
- Interactive mode: `python3 math_cli.py -i`.
- Load external plugins: `python3 math_cli.py --plugin-dir /path/to/plugins ...`.

Tip: Add your plugin directory to `PYTHONPATH` or pass `--plugin-dir` so it’s discoverable.

## Coding Style & Naming Conventions
- Python 3, 4‑space indentation, PEP 8 preferences.
- Use type hints in public APIs where clear (`Dict`, `List`, etc.).
- Modules/files: `snake_case.py`; classes: `PascalCase`; functions/vars: `snake_case`.
- Plugins: subclass `core.base_operations.MathOperation` and define `name`, `args`, `help`, and `execute()`.
  - Example class name: `HypotenuseOperation`; command name: `hypotenuse`.

## Testing Guidelines
- Place tests under `tests/` mirroring package paths (e.g., `tests/test_plugin_manager.py`).
- Prefer `pytest`; example: `pytest -q`.
- Cover: argument parsing (`cli/`), plugin discovery/execution (`core/`), and at least one operation.
- Name tests descriptively: `test_<module>_<behavior>()`.

## Commit & Pull Request Guidelines
- Commits: imperative, concise subject (≤72 chars), detailed body when needed.
  - Example: `add: include --list-plugins flag in help output`.
- PRs: clear description, rationale, and scope; link issues; include before/after examples for CLI changes; update docs.
- Keep changes focused; include tests/docs for new features.

## Security & Configuration Tips
- Only load plugins from trusted directories; untrusted code runs with your Python process.
- Validate arguments in operations and raise informative `ValueError`s.
- Interactive history is in‑memory only; avoid pasting secrets.

Refer to `docs/` for class diagrams, package layout, and execution flow.

