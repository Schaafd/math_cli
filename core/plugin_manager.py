import importlib
import importlib.util
import inspect
import pkgutil
from pathlib import Path
from typing import Dict, List, Type, Any, Tuple
from core.base_operations import MathOperation

class PluginManager:
    """Manages math operation plugins."""

    def __init__(self):
        self.operations: Dict[str, Type[MathOperation]] = {}
        self.plugin_dirs: List[Path] = []
        self._variable_substitution_enabled = True

    def register_operation(self, operation_class: Type[MathOperation]) -> None:
        """Register a math operation."""
        if not issubclass(operation_class, MathOperation):
            raise TypeError(f"{operation_class.__name__} is not a subclass of MathOperation")

        if not operation_class.name:
            raise ValueError(f"Operation {operation_class.__name__} does not have a name")

        self.operations[operation_class.name] = operation_class

    def add_plugin_directory(self, directory: str) -> None:
        """Add a directory to search for plugins."""
        path = Path(directory).resolve()
        if path not in self.plugin_dirs and path.is_dir():
            self.plugin_dirs.append(path)

    def discover_plugins(self) -> None:
        """Discover and load plugins from the plugins directory."""
        # First load built-in plugins
        self._load_plugins_from_module("plugins")

        # Then load from additional plugin directories
        for plugin_dir in self.plugin_dirs:
            self._load_external_plugins(plugin_dir)

    def _load_external_plugins(self, plugin_dir: Path) -> None:
        """Safely load plugins from a user-specified directory."""

        for module_path in plugin_dir.glob("*.py"):
            if not module_path.is_file():
                continue
            if module_path.name in {"__init__.py", "plugin_template.py"}:
                continue
            if not module_path.name.endswith("_plugin.py"):
                continue

            module_name = module_path.stem

            if self._is_name_conflicting(module_name):
                print(
                    f"Skipping plugin {module_path.name}: name collides with existing module"
                )
                continue

            try:
                module = self._import_module_from_path(module_path)
            except ImportError as e:
                print(f"Error importing plugin {module_path.name}: {e}")
                continue

            self._register_operations_from_module(module)

    def _is_name_conflicting(self, module_name: str) -> bool:
        """Return True if the module name collides with stdlib or project modules."""

        try:
            spec = importlib.util.find_spec(module_name)
        except (ImportError, AttributeError, ValueError):
            return False

        if spec is None:
            return False

        origin = getattr(spec, "origin", None)
        if origin in (None, "built-in", "frozen"):
            return True

        try:
            origin_path = Path(origin).resolve()
        except (TypeError, OSError):
            return True

        project_root = Path(__file__).resolve().parent.parent
        if project_root in origin_path.parents:
            return True

        return True

    def _import_module_from_path(self, module_path: Path):
        """Import a module from the given path without altering sys.path."""

        unique_name = (
            f"math_cli.external_plugins.{module_path.stem}_{abs(hash(module_path.resolve()))}"
        )
        spec = importlib.util.spec_from_file_location(unique_name, module_path)

        if not spec or not spec.loader:
            raise ImportError("Unable to create module spec")

        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)  # type: ignore[union-attr]
        except Exception as exc:  # pragma: no cover - importlib surfaces various errors
            raise ImportError(exc) from exc

        return module

    def _load_plugins_from_module(self, module_name: str) -> None:
        """Load plugins from a specific module."""
        try:
            module = importlib.import_module(module_name)
            for _, submodule_name, ispkg in pkgutil.iter_modules(module.__path__, module.__name__ + '.'):
                if submodule_name.endswith('.plugin_template'):
                    continue
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

    def _convert_string_to_type(self, value: str) -> Any:
        """Convert string to appropriate type (number or boolean).

        Args:
            value: String value to convert

        Returns:
            Converted value or original string
        """
        # Try to convert to number
        try:
            if '.' not in value and 'e' not in value.lower():
                return int(value)
            else:
                return float(value)
        except ValueError:
            # Check for boolean (only 'true' and 'false', not 'yes' and 'no')
            if value.lower() == 'true':
                return True
            elif value.lower() == 'false':
                return False
            # Otherwise keep as string
            return value

    def _substitute_variables(self, args: Tuple, kwargs: Dict) -> Tuple[Tuple, Dict]:
        """Substitute variable references with their values and convert types.

        Args:
            args: Positional arguments
            kwargs: Keyword arguments

        Returns:
            Tuple of (substituted_args, substituted_kwargs)
        """
        if not self._variable_substitution_enabled:
            return args, kwargs

        try:
            from core.variables import get_variable_store
            store = get_variable_store()

            # Substitute in args
            substituted_args = []
            for arg in args:
                if isinstance(arg, str) and arg.startswith('$'):
                    # Variable reference
                    try:
                        substituted_args.append(store.get(arg))
                    except NameError:
                        # Variable not found, keep as-is (might be literal $)
                        substituted_args.append(arg)
                elif isinstance(arg, str):
                    # Try to convert string literals to appropriate types
                    substituted_args.append(self._convert_string_to_type(arg))
                else:
                    substituted_args.append(arg)

            # Substitute in kwargs
            substituted_kwargs = {}
            for key, value in kwargs.items():
                if isinstance(value, str) and value.startswith('$'):
                    # Variable reference
                    try:
                        substituted_kwargs[key] = store.get(value)
                    except NameError:
                        # Variable not found, keep as-is
                        substituted_kwargs[key] = value
                elif isinstance(value, str):
                    # Try to convert string literals to appropriate types
                    substituted_kwargs[key] = self._convert_string_to_type(value)
                else:
                    substituted_kwargs[key] = value

            return tuple(substituted_args), substituted_kwargs

        except ImportError:
            # Variable system not available, skip substitution
            return args, kwargs

    def execute_operation(self, operation_name: str, *args, **kwargs):
        """Execute a registered operation or user-defined function with variable substitution.

        Args:
            operation_name: Name of the operation to execute
            *args: Positional arguments (may include variable references like $x)
            **kwargs: Keyword arguments (may include variable references)

        Returns:
            Operation result

        Raises:
            ValueError: If operation is unknown
        """
        # Check if it's a built-in operation
        if operation_name in self.operations:
            # Substitute variables in arguments
            substituted_args, substituted_kwargs = self._substitute_variables(args, kwargs)

            operation_class = self.operations[operation_name]
            return operation_class.execute(*substituted_args, **substituted_kwargs)

        # Check if it's a user-defined function
        try:
            from core.user_functions import get_function_registry
            registry = get_function_registry()

            if registry.exists(operation_name):
                # Substitute variables in arguments
                substituted_args, substituted_kwargs = self._substitute_variables(args, kwargs)

                # Call the user function
                func = registry.get(operation_name)

                # Check argument count
                if len(substituted_args) != len(func.parameters):
                    expected = len(func.parameters)
                    got = len(substituted_args)
                    raise ValueError(
                        f"Function '{operation_name}' expects {expected} argument(s), got {got}"
                    )

                # Create new variable scope
                from core.variables import get_variable_store
                store = get_variable_store()
                store.push_scope()

                try:
                    # Bind parameters to arguments
                    for param, arg in zip(func.parameters, substituted_args):
                        store.set(param, arg)

                    # Execute function body
                    tokens = func.body.split()
                    if not tokens:
                        raise ValueError(f"Function '{operation_name}' has empty body")

                    body_operation = tokens[0]
                    body_args = tokens[1:] if len(tokens) > 1 else []

                    # Recursively execute the operation
                    result = self.execute_operation(body_operation, *body_args)
                    return result

                finally:
                    # Always pop the scope
                    store.pop_scope()

        except ImportError:
            pass  # User functions not available

        # Operation not found
        raise ValueError(f"Unknown operation: {operation_name}")
