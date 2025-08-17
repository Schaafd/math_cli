import subprocess
import sys
from pathlib import Path

def run_cli(commands: str) -> str:
    """Run math_cli.py in interactive mode with the provided commands."""
    repo_root = Path(__file__).resolve().parent.parent
    result = subprocess.run(
        [sys.executable, "math_cli.py", "-i"],
        input=commands.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        cwd=repo_root,
        check=False,
    )
    return result.stdout.decode()

def test_factorial_requires_integer():
    output = run_cli("factorial 5.5\nexit\n")
    assert "Invalid argument '5.5' for n. Expected an integer." in output
