"""Variable operations plugin for Math CLI.

Provides operations for managing variables in scripts and interactive sessions.
"""

from core.base_operations import MathOperation
from core.variables import get_variable_store
from typing import Any


class SetVariableOperation(MathOperation):
    """Set a variable value."""

    name = "set"
    args = ["name", "value"]
    help = "Set variable: set x 42"
    category = "scripting"

    @classmethod
    def execute(cls, name: str, value: Any) -> str:
        """Set a variable.

        Args:
            name: Variable name (without $ prefix)
            value: Value to store

        Returns:
            Confirmation message
        """
        store = get_variable_store()

        # Remove $ prefix if present
        if name.startswith('$'):
            name = name[1:]

        # Convert string values to appropriate types
        if isinstance(value, str):
            # Try to convert to number
            try:
                # Try int first
                if '.' not in value and 'e' not in value.lower():
                    value = int(value)
                else:
                    value = float(value)
            except ValueError:
                # Check for boolean
                if value.lower() in ('true', 'yes'):
                    value = True
                elif value.lower() in ('false', 'no'):
                    value = False
                # Otherwise keep as string

        # Store the value
        store.set(name, value)

        # Format value for display
        formatted_value = store.format_value(value)

        return f"${name} = {formatted_value}"


class PersistVariableOperation(MathOperation):
    """Set a persistent variable (saved across sessions)."""

    name = "persist"
    args = ["name", "value"]
    help = "Set persistent variable: persist pi 3.14159"
    category = "scripting"

    @classmethod
    def execute(cls, name: str, value: Any) -> str:
        """Set a persistent variable.

        Args:
            name: Variable name (without $ prefix)
            value: Value to store

        Returns:
            Confirmation message
        """
        store = get_variable_store()

        # Remove $ prefix if present
        if name.startswith('$'):
            name = name[1:]

        # Convert string values to appropriate types (same as set operation)
        if isinstance(value, str):
            try:
                if '.' not in value and 'e' not in value.lower():
                    value = int(value)
                else:
                    value = float(value)
            except ValueError:
                if value.lower() in ('true', 'yes'):
                    value = True
                elif value.lower() in ('false', 'no'):
                    value = False

        # Store the value as persistent
        store.set(name, value, persistent=True)

        # Format value for display
        formatted_value = store.format_value(value)

        return f"${name} = {formatted_value} (persistent)"


class GetVariableOperation(MathOperation):
    """Get a variable value."""

    name = "get"
    args = ["name"]
    help = "Get variable: get x"
    category = "scripting"

    @classmethod
    def execute(cls, name: str) -> Any:
        """Get a variable value.

        Args:
            name: Variable name (with or without $ prefix)

        Returns:
            Variable value
        """
        store = get_variable_store()
        value = store.get(name)
        return value


class ListVariablesOperation(MathOperation):
    """List all variables."""

    name = "vars"
    args = []
    help = "List all variables: vars"
    category = "scripting"

    @classmethod
    def execute(cls) -> str:
        """List all variables.

        Returns:
            Formatted list of variables
        """
        store = get_variable_store()
        all_vars = store.list_all()

        if not all_vars:
            return "No variables defined"

        # Format output
        lines = ["Variables:"]
        lines.append("-" * 50)

        for name, value in sorted(all_vars.items()):
            formatted_value = store.format_value(value)
            lines.append(f"  ${name:15} = {formatted_value}")

        return "\n".join(lines)


class UnsetVariableOperation(MathOperation):
    """Delete a variable."""

    name = "unset"
    args = ["name"]
    help = "Delete variable: unset x"
    category = "scripting"

    @classmethod
    def execute(cls, name: str) -> str:
        """Delete a variable.

        Args:
            name: Variable name (with or without $ prefix)

        Returns:
            Confirmation message
        """
        store = get_variable_store()

        # Remove $ prefix if present
        if name.startswith('$'):
            name = name[1:]

        store.delete(name)

        return f"Deleted variable ${name}"


class ClearVariablesOperation(MathOperation):
    """Clear all variables."""

    name = "clear_vars"
    args = ["?persistent"]
    help = "Clear all variables: clear_vars [true|false]"
    category = "scripting"

    @classmethod
    def execute(cls, persistent: str = "false") -> str:
        """Clear all variables.

        Args:
            persistent: If 'true', also clear persistent variables

        Returns:
            Confirmation message
        """
        store = get_variable_store()

        include_persistent = persistent.lower() in ('true', 'yes', '1')
        store.clear_all(include_persistent=include_persistent)

        if include_persistent:
            return "Cleared all variables (including persistent)"
        else:
            return "Cleared all session variables"
