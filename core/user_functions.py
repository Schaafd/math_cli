"""User-defined functions for Math CLI.

Allows users to define custom functions that can be called like built-in operations.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class UserFunction:
    """Represents a user-defined function."""

    name: str
    parameters: List[str]
    body: str  # The command to execute (e.g., "multiply $x $x")
    description: Optional[str] = None

    def __repr__(self):
        params_str = ', '.join(self.parameters)
        return f"def {self.name}({params_str}) = {self.body}"


class FunctionRegistry:
    """Registry for user-defined functions."""

    def __init__(self):
        """Initialize the function registry."""
        self._functions: Dict[str, UserFunction] = {}

    def define(self, name: str, parameters: List[str], body: str, description: Optional[str] = None):
        """Define a new function.

        Args:
            name: Function name
            parameters: List of parameter names
            body: Function body (command to execute)
            description: Optional description

        Raises:
            ValueError: If function name is invalid or already defined as built-in
        """
        # Validate name
        if not name or not isinstance(name, str):
            raise ValueError("Function name must be a non-empty string")

        if not name.isidentifier():
            raise ValueError(f"Invalid function name: {name}")

        # Store function
        func = UserFunction(
            name=name,
            parameters=parameters,
            body=body,
            description=description
        )
        self._functions[name] = func

    def get(self, name: str) -> Optional[UserFunction]:
        """Get a function by name.

        Args:
            name: Function name

        Returns:
            UserFunction if found, None otherwise
        """
        return self._functions.get(name)

    def exists(self, name: str) -> bool:
        """Check if a function is defined.

        Args:
            name: Function name

        Returns:
            True if function exists
        """
        return name in self._functions

    def delete(self, name: str):
        """Delete a function.

        Args:
            name: Function name

        Raises:
            KeyError: If function doesn't exist
        """
        if name not in self._functions:
            raise KeyError(f"Function '{name}' is not defined")
        del self._functions[name]

    def list_all(self) -> Dict[str, UserFunction]:
        """Get all defined functions.

        Returns:
            Dictionary of all functions
        """
        return dict(self._functions)

    def clear_all(self):
        """Clear all functions."""
        self._functions.clear()


# Global function registry
_function_registry: Optional[FunctionRegistry] = None


def get_function_registry() -> FunctionRegistry:
    """Get the global function registry.

    Returns:
        The global FunctionRegistry instance
    """
    global _function_registry
    if _function_registry is None:
        _function_registry = FunctionRegistry()
    return _function_registry
