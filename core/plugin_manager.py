import importlib
import importlib.util
import os
import pkgutil
import inspect
import sys
import logging
from pathlib import Path
from typing import Dict, List, Type, Optional, Any
from core.base_operations import MathOperation

# Configure logging
logger = logging.getLogger(__name__)

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
            logger.info(f"Added plugin directory: {directory}")
        elif not os.path.isdir(directory):
            logger.warning(f"Plugin directory does not exist: {directory}")

    def discover_plugins(self) -> None:
        """Discover and load plugins from plugin directories."""
        # First load built-in plugins
        self._load_plugins_from_module("plugins")

        # Then load from additional plugin directories
        for plugin_dir in self.plugin_dirs:
            self._load_plugins_from_directory(plugin_dir)

    def _load_plugins_from_directory(self, plugin_dir: str) -> None:
        """Load plugins from a directory using secure importlib mechanisms."""
        for finder, name, ispkg in pkgutil.iter_modules([plugin_dir]):
            if ispkg:
                continue  # Skip packages, only load modules
            
            try:
                # Use importlib.util to safely load modules without modifying sys.path
                module_path = os.path.join(plugin_dir, f"{name}.py")
                if os.path.exists(module_path):
                    spec = importlib.util.spec_from_file_location(f"plugin_{name}", module_path)
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        self._register_operations_from_module(module)
                        logger.info(f"Successfully loaded plugin: {name}")
                    else:
                        logger.error(f"Failed to create spec for plugin: {name}")
                else:
                    logger.warning(f"Plugin file not found: {module_path}")
            except Exception as e:
                logger.error(f"Error loading plugin '{name}' from directory {plugin_dir}: {e}")
                # Continue to next plugin instead of stopping the entire loading process

    def _load_plugins_from_module(self, module_name: str) -> None:
        """Load plugins from a specific module."""
        try:
            module = importlib.import_module(module_name)
            for _, submodule_name, ispkg in pkgutil.iter_modules(module.__path__, module.__name__ + '.'):
                if not ispkg:  # Only process modules, not packages
                    base_name = submodule_name.rsplit('.', 1)[-1]
                    # Skip templates and private modules
                    if base_name.endswith('plugin_template') or base_name.startswith('_'):
                        continue
                    try:
                        submodule = importlib.import_module(submodule_name)
                        self._register_operations_from_module(submodule)
                        logger.info(f"Successfully loaded built-in plugin: {submodule_name}")
                    except ImportError as e:
                        logger.error(f"Error importing {submodule_name}: {e}")
        except ImportError as e:
            logger.error(f"Error importing {module_name}: {e}")

    def _register_operations_from_module(self, module) -> None:
        """Register all MathOperation subclasses from a module."""
        for _, obj in inspect.getmembers(module):
            if (inspect.isclass(obj) and issubclass(obj, MathOperation)
                    and obj is not MathOperation and hasattr(obj, 'name')):
                try:
                    self.register_operation(obj)
                    logger.debug(f"Registered operation: {obj.name}")
                except (TypeError, ValueError) as e:
                    logger.error(f"Error registering operation from {module.__name__}: {e}")

    def get_operations_metadata(self) -> Dict[str, Dict[str, Any]]:
        """Return metadata for all registered operations."""
        return {name: op.get_metadata() for name, op in self.operations.items()}

    def execute_operation(self, operation_name: str, *args: Any, **kwargs: Any) -> Any:
        """Execute a registered operation."""
        if operation_name not in self.operations:
            raise ValueError(f"Unknown operation: {operation_name}")

        operation_class = self.operations[operation_name]
        return operation_class.execute(*args, **kwargs)
