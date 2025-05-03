import importlib
import os
import pkgutil
import inspect
import sys
from pathlib import Path
from typing import Dict, List, Type
from core.base_operations import MathOperation

class PluginManager:
    """Manages math operation plugins."""

    def __init__(self):
        self.operations: Dict[str, Type[MathOperation]] = {}
        self.plugin_dirs = []

    def register_operation(self, operation_class: Type[MathOperation]) -> None:
        """Register a math operation."""
        if not issubclass(operation_class, MathOperation):
            raise TypeError(f"{operation_class.__name__} is not a subclass of MathOperation")

        if not operation_class.name:
            raise ValueError(f"Operation {operation_class.__name__} does not have a name")

        self.operations[operation_class.name] = operation_class

    def add_plugin_directory(self, directory: str) -> None:
        """Add a directory to search for plugins."""
        if directory not in self.plugin_dirs and os.path.isdir(directory):
            self.plugin_dirs.append(directory)
            # Add to Python path so plugins can be imported
            if directory not in sys.path:
                sys.path.insert(0, directory)

    def discover_plugins(self) -> None:
        """Discover and load plugins from the plugins directory."""
        # First load built-in plugins
        self._load_plugins_from_module("plugins")

        # Then load from additional plugin directories
        for plugin_dir in self.plugin_dirs:
            for finder, name, ispkg in pkgutil.iter_modules([plugin_dir]):
                try:
                    module = importlib.import_module(name)
                    self._register_operations_from_module(module)
                except ImportError as e:
                    print(f"Error importing plugin {name}: {e}")

    def _load_plugins_from_module(self, module_name: str) -> None:
        """Load plugins from a specific module."""
        try:
            module = importlib.import_module(module_name)
            for _, submodule_name, ispkg in pkgutil.iter_modules(module.__path__, module.__name__ + '.'):
                if not ispkg:  # Only process modules, not packages
                    try:
                        submodule = importlib.import_module(submodule_name)
                        self._register_operations_from_module(submodule)
                    except ImportError as e:
                        print(f"Error importing {submodule_name}: {e}")
        except ImportError as e:
            print(f"Error importing {module_name}: {e}")

    def _register_operations_from_module(self, module) -> None:
        """Register all MathOperation subclasses from a module."""
        for _, obj in inspect.getmembers(module):
            if (inspect.isclass(obj) and issubclass(obj, MathOperation)
                    and obj is not MathOperation and hasattr(obj, 'name')):
                try:
                    self.register_operation(obj)
                except (TypeError, ValueError) as e:
                    print(f"Error registering operation from {module.__name__}: {e}")

    def get_operations_metadata(self) -> Dict:
        """Return metadata for all registered operations."""
        return {name: op.get_metadata() for name, op in self.operations.items()}

    def execute_operation(self, operation_name: str, *args, **kwargs):
        """Execute a registered operation."""
        if operation_name not in self.operations:
            raise ValueError(f"Unknown operation: {operation_name}")

        operation_class = self.operations[operation_name]
        return operation_class.execute(*args, **kwargs)
