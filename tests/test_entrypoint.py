import sys
from importlib import util
from pathlib import Path


def load_math_cli_module():
    root = Path(__file__).resolve().parents[1]
    path = root / "math_cli.py"
    spec = util.spec_from_file_location("_math_cli_module", path)
    mod = util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def run_cli(argv):
    cli = load_math_cli_module()
    sys_argv_backup = sys.argv
    try:
        sys.argv = argv
        return cli.main()
    finally:
        sys.argv = sys_argv_backup


def test_main_lists_plugins(capsys):
    exit_code = run_cli(["math_cli.py", "--list-plugins"])
    assert exit_code == 0
    out = capsys.readouterr().out
    # Check for new categorized format
    assert "MATH CLI - AVAILABLE OPERATIONS" in out
    assert "add" in out


def test_main_executes_add_and_prints_result(capsys):
    exit_code = run_cli(["math_cli.py", "add", "2", "3"])
    assert exit_code == 0
    out = capsys.readouterr().out
    assert "Result: 5.0" in out or "Result: 5" in out


def test_main_accepts_additional_plugin_directory(tmp_path, capsys):
    plugin_dir = tmp_path / "custom_plugins"
    plugin_dir.mkdir()

    plugin_module = plugin_dir / "double_value_plugin.py"
    plugin_module.write_text(
        """
from core.base_operations import MathOperation


class DoubleValueOperation(MathOperation):
    name = "double_value"
    help = "Double the provided value"
    args = ["value"]

    @classmethod
    def execute(cls, value):
        return value * 2
"""
    )

    exit_code = run_cli([
        "math_cli.py",
        "--plugin-dir",
        str(plugin_dir),
        "double_value",
        "4",
    ])

    assert exit_code == 0
    out = capsys.readouterr().out
    assert "Result: 8" in out or "Result: 8.0" in out


def test_main_displays_help_for_global_help_flag(capsys):
    exit_code = run_cli(["math_cli.py", "--help"])
    assert exit_code == 0
    out = capsys.readouterr().out
    assert "usage:" in out.lower()
    assert "add" in out
