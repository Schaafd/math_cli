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
        """
        Add a directory to the plugin search path.
        
        If the path exists and is not already registered, it is appended to the manager's plugin_dirs.
        If the path does not exist, the directory is not added and a warning is emitted.
        Calling this with a directory already in plugin_dirs is a no-op.
        """
        if directory not in self.plugin_dirs and os.path.isdir(directory):
            self.plugin_dirs.append(directory)
            logger.info(f"Added plugin directory: {directory}")
        elif not os.path.isdir(directory):
            logger.warning(f"Plugin directory does not exist: {directory}")

    def discover_plugins(self) -> None:
        """
        Discover and load math operation plugins.
        
        Loads built-in plugins from the package named "plugins", then scans each directory in self.plugin_dirs and loads any plugin modules found there. Successfully discovered plugin classes are registered into the manager's operations mapping. This method has no return value and will log errors for modules that fail to load without raising.
        """
        # First load built-in plugins
        self._load_plugins_from_module("plugins")

        # Then load from additional plugin directories
        for plugin_dir in self.plugin_dirs:
            self._load_plugins_from_directory(plugin_dir)

    def _load_plugins_from_directory(self, plugin_dir: str) -> None:
        """
        Load Python plugin modules from a filesystem directory and register their operations.
        
        Scans the given directory for top-level modules (packages are skipped). For each module it looks for a corresponding .py file and, when present, loads the module via importlib.util.spec_from_file_location (so sys.path is not modified), executes it, and calls self._register_operations_from_module(module) to register any MathOperation subclasses found. Missing files and errors while loading or registering are logged and do not stop discovery.
        
        Parameters:
            plugin_dir (str): Filesystem path to the directory containing plugin modules.
        """
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
        """
        Discover and load plugin modules from a named package and register any MathOperation subclasses found.
        
        Given the dotted package name in module_name, imports that package and iterates its immediate submodules (not subpackages). For each submodule it:
        - skips packages,
        - skips submodules whose base name starts with '_' or ends with 'plugin_template',
        - imports the submodule and calls self._register_operations_from_module(submodule) to register any contained operations.
        
        Does not raise on import failures; import errors are handled internally so discovery can continue."""
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
        """
        Scan the given module for MathOperation subclasses and register each valid operation.
        
        The function inspects the provided module for classes that are subclasses of MathOperation (excluding MathOperation itself)
        and that define a non-empty `name` attribute. Each matching class is passed to register_operation. Errors raised
        by register_operation (e.g., invalid subclass or missing/empty name) are caught and logged; failing registrations
        do not stop the scan.
        
        Parameters:
            module: A loaded Python module to scan for MathOperation subclasses.
        
        Returns:
            None
        """
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
        """
        Execute a registered operation by name and return its result.
        
        Looks up the operation class registered under `operation_name` and calls its
        `execute(*args, **kwargs)`, forwarding all positional and keyword arguments.
        Raises ValueError if no operation with the given name is registered.
        
        Parameters:
            operation_name (str): Name of the registered operation to run.
            *args: Positional arguments forwarded to the operation's `execute` method.
            **kwargs: Keyword arguments forwarded to the operation's `execute` method.
        
        Returns:
            Any: The value returned by the operation's `execute` method.
        
        Raises:
            ValueError: If `operation_name` is not found among registered operations.
        """
        if operation_name not in self.operations:
            raise ValueError(f"Unknown operation: {operation_name}")

        operation_class = self.operations[operation_name]
        return operation_class.execute(*args, **kwargs)
