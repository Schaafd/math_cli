"""Script file runner for Math CLI.

Executes .mathcli script files containing sequences of commands.
"""

import os
from pathlib import Path
from typing import List, Optional, Tuple
from core.plugin_manager import PluginManager
from core.variables import get_variable_store


class ScriptRunner:
    """Runs Math CLI script files."""

    def __init__(self, plugin_manager: Optional[PluginManager] = None):
        """Initialize the script runner.

        Args:
            plugin_manager: PluginManager instance to use (creates new if None)
        """
        self.plugin_manager = plugin_manager or PluginManager()
        if plugin_manager is None:
            self.plugin_manager.discover_plugins()

    def parse_line(self, line: str) -> Optional[Tuple[str, List[str]]]:
        """Parse a script line into operation and arguments.

        Args:
            line: Line to parse

        Returns:
            Tuple of (operation_name, args) or None if line should be skipped
        """
        # Remove leading/trailing whitespace
        line = line.strip()

        # Skip empty lines
        if not line:
            return None

        # Skip comments
        if line.startswith('#'):
            return None

        # Split into tokens (simple whitespace splitting for now)
        tokens = line.split()
        if not tokens:
            return None

        operation = tokens[0]
        args = tokens[1:] if len(tokens) > 1 else []

        return operation, args

    def execute_line(self, line: str, line_number: int) -> Optional[str]:
        """Execute a single script line.

        Args:
            line: Line to execute
            line_number: Line number (for error reporting)

        Returns:
            Result string or None if line was skipped

        Raises:
            Exception: If execution fails
        """
        parsed = self.parse_line(line)
        if parsed is None:
            return None

        operation, args = parsed

        try:
            result = self.plugin_manager.execute_operation(operation, *args)
            return str(result) if result is not None else None
        except Exception as e:
            raise RuntimeError(f"Error on line {line_number}: {line}\n  {type(e).__name__}: {e}")

    def run_script(self, script_path: str, verbose: bool = False) -> dict:
        """Run a script file.

        Args:
            script_path: Path to the .mathcli script file
            verbose: If True, print each line and result

        Returns:
            Dictionary with execution results:
            {
                'success': bool,
                'lines_executed': int,
                'outputs': List[str],
                'error': Optional[str]
            }
        """
        # Validate file exists
        path = Path(script_path)
        if not path.exists():
            return {
                'success': False,
                'lines_executed': 0,
                'outputs': [],
                'error': f"Script file not found: {script_path}"
            }

        # Read script file
        try:
            with open(path, 'r') as f:
                lines = f.readlines()
        except IOError as e:
            return {
                'success': False,
                'lines_executed': 0,
                'outputs': [],
                'error': f"Failed to read script: {e}"
            }

        # Execute lines
        outputs = []
        lines_executed = 0

        # Create a new scope for the script
        store = get_variable_store()
        store.push_scope()

        try:
            for line_num, line in enumerate(lines, start=1):
                if verbose:
                    if line.strip() and not line.strip().startswith('#'):
                        print(f"[{line_num}] {line.rstrip()}")

                try:
                    result = self.execute_line(line, line_num)
                    if result is not None:
                        outputs.append(result)
                        lines_executed += 1
                        if verbose:
                            print(f"  → {result}")
                except Exception as e:
                    store.pop_scope()  # Clean up scope on error
                    return {
                        'success': False,
                        'lines_executed': lines_executed,
                        'outputs': outputs,
                        'error': str(e)
                    }

            # Pop the script scope
            store.pop_scope()

            return {
                'success': True,
                'lines_executed': lines_executed,
                'outputs': outputs,
                'error': None
            }

        except Exception as e:
            store.pop_scope()  # Clean up scope on unexpected error
            return {
                'success': False,
                'lines_executed': lines_executed,
                'outputs': outputs,
                'error': f"Unexpected error: {e}"
            }

    def run_script_string(self, script_content: str, verbose: bool = False) -> dict:
        """Run a script from a string (for testing).

        Args:
            script_content: Script content as string
            verbose: If True, print each line and result

        Returns:
            Dictionary with execution results (same format as run_script)
        """
        lines = script_content.split('\n')
        outputs = []
        lines_executed = 0

        # Create a new scope for the script
        store = get_variable_store()
        store.push_scope()

        try:
            for line_num, line in enumerate(lines, start=1):
                if verbose:
                    if line.strip() and not line.strip().startswith('#'):
                        print(f"[{line_num}] {line.rstrip()}")

                try:
                    result = self.execute_line(line, line_num)
                    if result is not None:
                        outputs.append(result)
                        lines_executed += 1
                        if verbose:
                            print(f"  → {result}")
                except Exception as e:
                    store.pop_scope()  # Clean up scope on error
                    return {
                        'success': False,
                        'lines_executed': lines_executed,
                        'outputs': outputs,
                        'error': str(e)
                    }

            # Pop the script scope
            store.pop_scope()

            return {
                'success': True,
                'lines_executed': lines_executed,
                'outputs': outputs,
                'error': None
            }

        except Exception as e:
            store.pop_scope()  # Clean up scope on unexpected error
            return {
                'success': False,
                'lines_executed': lines_executed,
                'outputs': outputs,
                'error': f"Unexpected error: {e}"
            }
