from pathlib import Path

import pytest

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11
    tomllib = None


def test_pyproject_installs_short_math_command_alias():
    if tomllib is None:
        pytest.skip("tomllib is not available")

    pyproject_path = Path(__file__).resolve().parents[1] / "pyproject.toml"
    pyproject = tomllib.loads(pyproject_path.read_text())

    scripts = pyproject["project"]["scripts"]
    assert scripts["math"] == "math_cli:main"
    assert scripts["math-cli"] == "math_cli:main"
