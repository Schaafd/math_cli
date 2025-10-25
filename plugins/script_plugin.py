"""Script execution plugin for Math CLI."""

from core.base_operations import MathOperation
from cli.script_runner import ScriptRunner
from pathlib import Path


class RunScriptOperation(MathOperation):
    """Run a .mathcli script file."""

    name = "run"
    args = ["script_path", "?verbose"]
    help = "Run script: run script.mathcli"
    category = "scripting"

    @classmethod
    def execute(cls, script_path: str, verbose: str = "false") -> str:
        """Execute a script file.

        Args:
            script_path: Path to .mathcli script file
            verbose: If 'true', show each line as it executes

        Returns:
            Summary of execution
        """
        # Convert verbose to boolean
        if isinstance(verbose, bool):
            verbose_bool = verbose
        else:
            verbose_bool = str(verbose).lower() in ('true', 'yes', '1')

        # Create runner and execute
        runner = ScriptRunner()
        result = runner.run_script(script_path, verbose=verbose_bool)

        if result['success']:
            return f"✓ Script completed: {result['lines_executed']} commands executed"
        else:
            error_msg = result['error']
            return f"✗ Script failed after {result['lines_executed']} commands:\n{error_msg}"


class EvalOperation(MathOperation):
    """Evaluate a script string inline."""

    name = "eval"
    args = ["script_content"]
    help = "Evaluate script: eval 'set x 10; add $x 5'"
    category = "scripting"

    @classmethod
    def execute(cls, script_content: str) -> str:
        """Evaluate a script string.

        Args:
            script_content: Script content to execute

        Returns:
            Last result from script
        """
        # Replace semicolons with newlines for inline scripts
        script_content = script_content.replace(';', '\n')

        # Create runner and execute
        runner = ScriptRunner()
        result = runner.run_script_string(script_content, verbose=False)

        if result['success']:
            # Return the last output
            if result['outputs']:
                return result['outputs'][-1]
            else:
                return "✓ Script completed (no output)"
        else:
            error_msg = result['error']
            return f"✗ Script failed:\n{error_msg}"
