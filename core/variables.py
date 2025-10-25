"""Variable storage and management system for Math CLI.

This module provides a variable system that allows users to store and reference
values during interactive sessions and script execution.
"""

import json
import os
from typing import Any, Dict, Optional, Union
from pathlib import Path
import numpy as np
import pandas as pd


class VariableStore:
    """Manages variable storage with support for different scopes and persistence."""

    def __init__(self):
        """Initialize the variable store."""
        self._global_vars: Dict[str, Any] = {}
        self._scope_stack: list = []  # Stack of local scopes for nested contexts
        self._persistent_vars: Dict[str, Any] = {}
        self._persistence_path: Optional[Path] = None

    def set_persistence_path(self, path: str):
        """Set the path for persistent variable storage.

        Args:
            path: File path for storing persistent variables
        """
        self._persistence_path = Path(path)
        if self._persistence_path.exists():
            self._load_persistent_vars()

    def _load_persistent_vars(self):
        """Load persistent variables from file."""
        if not self._persistence_path or not self._persistence_path.exists():
            return

        try:
            with open(self._persistence_path, 'r') as f:
                data = json.load(f)
                # Only load simple types (no complex objects)
                for key, value in data.items():
                    if isinstance(value, (int, float, str, bool, list, dict)):
                        self._persistent_vars[key] = value
        except (json.JSONDecodeError, IOError):
            pass

    def _save_persistent_vars(self):
        """Save persistent variables to file."""
        if not self._persistence_path:
            return

        # Ensure directory exists
        self._persistence_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            # Only save simple types that are JSON serializable
            saveable_vars = {}
            for key, value in self._persistent_vars.items():
                if isinstance(value, (int, float, str, bool, list, dict)):
                    saveable_vars[key] = value

            with open(self._persistence_path, 'w') as f:
                json.dump(saveable_vars, f, indent=2)
        except (IOError, TypeError):
            pass

    def set(self, name: str, value: Any, persistent: bool = False):
        """Set a variable value.

        Args:
            name: Variable name (without $ prefix)
            value: Variable value
            persistent: If True, save across sessions
        """
        # Validate variable name
        if not name or not isinstance(name, str):
            raise ValueError("Variable name must be a non-empty string")

        if name.startswith('$'):
            name = name[1:]  # Remove $ prefix if present

        # Store in appropriate scope
        if self._scope_stack:
            # Store in current local scope
            self._scope_stack[-1][name] = value
        else:
            # Store in global scope
            self._global_vars[name] = value

        # Handle persistence
        if persistent:
            self._persistent_vars[name] = value
            self._save_persistent_vars()

    def get(self, name: str) -> Any:
        """Get a variable value.

        Args:
            name: Variable name (with or without $ prefix)

        Returns:
            Variable value

        Raises:
            NameError: If variable is not defined
        """
        if name.startswith('$'):
            name = name[1:]  # Remove $ prefix

        # Search in scope stack (most recent first)
        for scope in reversed(self._scope_stack):
            if name in scope:
                return scope[name]

        # Search in global scope
        if name in self._global_vars:
            return self._global_vars[name]

        # Search in persistent vars
        if name in self._persistent_vars:
            return self._persistent_vars[name]

        raise NameError(f"Variable '${name}' is not defined")

    def has(self, name: str) -> bool:
        """Check if a variable is defined.

        Args:
            name: Variable name (with or without $ prefix)

        Returns:
            True if variable exists, False otherwise
        """
        if name.startswith('$'):
            name = name[1:]

        # Check all scopes
        for scope in reversed(self._scope_stack):
            if name in scope:
                return True

        return name in self._global_vars or name in self._persistent_vars

    def delete(self, name: str):
        """Delete a variable.

        Args:
            name: Variable name (with or without $ prefix)

        Raises:
            NameError: If variable is not defined
        """
        if name.startswith('$'):
            name = name[1:]

        # Try to delete from current scope
        if self._scope_stack and name in self._scope_stack[-1]:
            del self._scope_stack[-1][name]
            return

        # Try to delete from global scope
        if name in self._global_vars:
            del self._global_vars[name]
            return

        # Try to delete from persistent vars
        if name in self._persistent_vars:
            del self._persistent_vars[name]
            self._save_persistent_vars()
            return

        raise NameError(f"Variable '${name}' is not defined")

    def list_all(self) -> Dict[str, Any]:
        """Get all variables in current scope.

        Returns:
            Dictionary of all visible variables
        """
        # Start with persistent vars
        all_vars = dict(self._persistent_vars)

        # Add global vars
        all_vars.update(self._global_vars)

        # Add local scope vars (most recent takes precedence)
        for scope in self._scope_stack:
            all_vars.update(scope)

        return all_vars

    def clear_all(self, include_persistent: bool = False):
        """Clear all variables.

        Args:
            include_persistent: If True, also clear persistent variables
        """
        self._global_vars.clear()
        self._scope_stack.clear()

        if include_persistent:
            self._persistent_vars.clear()
            self._save_persistent_vars()

    def push_scope(self):
        """Create a new local scope (for functions, scripts, etc.)."""
        self._scope_stack.append({})

    def pop_scope(self):
        """Remove the current local scope."""
        if self._scope_stack:
            self._scope_stack.pop()

    def format_value(self, value: Any) -> str:
        """Format a value for display.

        Args:
            value: Value to format

        Returns:
            Formatted string representation
        """
        if isinstance(value, bool):  # Check bool before int (bool is subclass of int)
            return 'true' if value else 'false'
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, str):
            return f'"{value}"'
        elif isinstance(value, list):
            return f'[{", ".join(self.format_value(v) for v in value)}]'
        elif isinstance(value, dict):
            return f'{{{", ".join(f"{k}: {self.format_value(v)}" for k, v in value.items())}}}'
        elif isinstance(value, np.ndarray):
            return f'Array{value.shape}'
        elif isinstance(value, pd.DataFrame):
            return f'DataFrame[{value.shape[0]}×{value.shape[1]}]'
        else:
            return str(type(value).__name__)


# Global variable store instance
_variable_store: Optional[VariableStore] = None


def get_variable_store() -> VariableStore:
    """Get the global variable store instance.

    Returns:
        The global VariableStore instance
    """
    global _variable_store
    if _variable_store is None:
        _variable_store = VariableStore()
        # Set default persistence path
        config_dir = Path.home() / '.mathcli'
        _variable_store.set_persistence_path(str(config_dir / 'variables.json'))
    return _variable_store
