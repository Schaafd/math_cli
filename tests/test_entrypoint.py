import sys
from importlib import util
from pathlib import Path


def load_math_cli_module():
    """
    Load and return the math_cli.py module located in the repository root.
    
    Resolves this file's grandparent directory, builds the path to "math_cli.py",
    creates an import spec and module object, executes the module to populate it,
    and returns the module object.
    
    Returns:
        types.ModuleType: The loaded math_cli module.
    
    Raises:
        AssertionError: If an import spec or its loader could not be created.
    """
    root = Path(__file__).resolve().parents[1]
    path = root / "math_cli.py"
    spec = util.spec_from_file_location("_math_cli_module", path)
    mod = util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def run_cli(argv):
    """
    Run the math CLI's main() with a temporary argv and return its result.
    
    This loads the project's math_cli module, replaces sys.argv with the provided list of arguments for the duration of the call to the module's main(), and restores the original sys.argv afterwards.
    
    Parameters:
        argv (list[str]): Argument vector to present to the CLI (e.g., ["math_cli.py", "add", "2", "3"]).
    
    Returns:
        The value returned by math_cli.main(), typically an integer exit code.
    """
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
    assert "Available operations" in out
    assert "add" in out


def test_main_executes_add_and_prints_result(capsys):
    exit_code = run_cli(["math_cli.py", "add", "2", "3"])
    assert exit_code == 0
    out = capsys.readouterr().out
    assert "Result: 5.0" in out or "Result: 5" in out
