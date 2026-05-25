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


def test_main_interactive_routes_to_full_screen_app(monkeypatch):
    called = {}

    def fake_run(plugin_manager, operations_metadata):
        called["full_screen"] = len(operations_metadata)

    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)
    monkeypatch.setattr("cli.interactive_app.run_interactive_app", fake_run)

    exit_code = run_cli(["math_cli.py", "--interactive"])

    assert exit_code == 0
    assert called["full_screen"] > 0


def test_main_tui_alias_routes_to_full_screen_app(monkeypatch):
    called = {}

    def fake_run(plugin_manager, operations_metadata):
        called["full_screen"] = len(operations_metadata)

    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)
    monkeypatch.setattr("cli.interactive_app.run_interactive_app", fake_run)

    exit_code = run_cli(["math_cli.py", "--tui"])

    assert exit_code == 0
    assert called["full_screen"] > 0


def test_main_classic_interactive_routes_to_prompt_loop(monkeypatch):
    called = {}

    def fake_run(plugin_manager, operations_metadata, enable_colors, enable_animations, accessibility_settings):
        called["classic"] = len(operations_metadata)

    monkeypatch.setattr("cli.interactive_mode.run_interactive_mode", fake_run)

    exit_code = run_cli(["math_cli.py", "--classic-interactive"])

    assert exit_code == 0
    assert called["classic"] > 0


def test_main_full_screen_without_tty_suggests_classic_mode(monkeypatch, capsys):
    monkeypatch.setattr(sys.stdin, "isatty", lambda: False)
    monkeypatch.setattr(sys.stdout, "isatty", lambda: False)

    exit_code = run_cli(["math_cli.py", "--interactive"])

    assert exit_code == 1
    err = capsys.readouterr().err
    assert "requires an interactive terminal" in err
    assert "--classic-interactive" in err


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


def test_main_executes_expression_input(capsys):
    exit_code = run_cli(["math_cli.py", "7 + 9 * 2"])
    assert exit_code == 0
    out = capsys.readouterr().out
    assert "Result: 25" in out


def test_main_executes_chained_input(capsys):
    exit_code = run_cli(["math_cli.py", "add", "7", "2", "|", "multiply", "4"])
    assert exit_code == 0
    out = capsys.readouterr().out
    assert "Result: 36" in out


def test_main_executes_string_expression_operation(capsys):
    exit_code = run_cli(["math_cli.py", "derivative", "x**2", "x"])
    assert exit_code == 0
    out = capsys.readouterr().out
    assert "Result: 2*x" in out


def test_main_executes_variable_operation_with_string_name(capsys):
    exit_code = run_cli(["math_cli.py", "set", "cli_test_value", "10"])
    assert exit_code == 0
    out = capsys.readouterr().out
    assert "Result: $cli_test_value = 10" in out


def test_main_executes_optional_argument_operation(tmp_path, capsys):
    csv_path = tmp_path / "data.csv"
    csv_path.write_text("value\n1\n2\n")

    exit_code = run_cli(["math_cli.py", "load_data", str(csv_path), "csv", "cli_data"])
    assert exit_code == 0
    out = capsys.readouterr().out
    assert "Loaded 2 rows" in out


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


def test_main_displays_help_when_tui_flag_is_followed_by_help(capsys):
    exit_code = run_cli(["math_cli.py", "--tui", "--help"])
    assert exit_code == 0
    out = capsys.readouterr().out
    assert "usage:" in out.lower()
    assert "--full-screen-tui" in out


def test_main_unknown_operation_is_concise_and_suggests_match(capsys):
    exit_code = run_cli(["math_cli.py", "sub", "1", "2"])

    assert exit_code == 2
    captured = capsys.readouterr()
    output = captured.out + captured.err
    assert "Error: Unknown operation 'sub'" in output
    assert "Did you mean: subtract" in output
    assert "math_cli.py subtract <a> <b>" in output
    assert "Use --list-plugins to see available operations." in output
    assert "invalid choice" not in output
    assert "choose from" not in output
    assert "usage:" not in output.lower()
