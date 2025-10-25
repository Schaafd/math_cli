"""User-defined function operations for Math CLI."""

from core.base_operations import MathOperation
from core.user_functions import get_function_registry
from core.variables import get_variable_store
from core.plugin_manager import PluginManager
from typing import Any


class DefineFunctionOperation(MathOperation):
    """Define a new function.

    Syntax: def function_name param1 param2 ... = body
    Example: def square x = multiply $x $x
    """

    name = "def"
    args = ["definition"]
    help = "Define function: def square x = multiply $x $x"
    category = "scripting"
    variadic = True

    @classmethod
    def execute(cls, *args) -> str:
        """Define a new function.

        Args:
            *args: Function definition tokens

        Returns:
            Confirmation message
        """
        if len(args) < 3:
            raise ValueError("Function definition requires: def name param1 ... = body")

        # Find the '=' separator
        try:
            equals_index = args.index('=')
        except ValueError:
            raise ValueError("Function definition must contain '=' separator")

        if equals_index < 1:
            raise ValueError("Function name is required before '='")

        # Parse function definition
        name = str(args[0])
        parameters = [str(p) for p in args[1:equals_index]]
        body = ' '.join(str(arg) for arg in args[equals_index + 1:])

        if not body:
            raise ValueError("Function body cannot be empty")

        # Register the function
        registry = get_function_registry()
        registry.define(name, parameters, body)

        params_str = ', '.join(f'${p}' for p in parameters)
        return f"✓ Defined function: {name}({params_str}) = {body}"


class ListFunctionsOperation(MathOperation):
    """List all user-defined functions."""

    name = "funcs"
    args = []
    help = "List all functions: funcs"
    category = "scripting"

    @classmethod
    def execute(cls) -> str:
        """List all user-defined functions.

        Returns:
            Formatted list of functions
        """
        registry = get_function_registry()
        functions = registry.list_all()

        if not functions:
            return "No functions defined"

        lines = ["User-defined functions:"]
        lines.append("-" * 70)

        for name, func in sorted(functions.items()):
            params_str = ', '.join(f'${p}' for p in func.parameters)
            lines.append(f"  {name}({params_str})")
            lines.append(f"    = {func.body}")

        return "\n".join(lines)


class DeleteFunctionOperation(MathOperation):
    """Delete a user-defined function."""

    name = "undef"
    args = ["name"]
    help = "Delete function: undef square"
    category = "scripting"

    @classmethod
    def execute(cls, name: str) -> str:
        """Delete a function.

        Args:
            name: Function name

        Returns:
            Confirmation message
        """
        registry = get_function_registry()

        if not registry.exists(name):
            raise ValueError(f"Function '{name}' is not defined")

        registry.delete(name)
        return f"✓ Deleted function: {name}"


class CallUserFunctionOperation(MathOperation):
    """Call a user-defined function.

    This is a special operation that intercepts calls to user-defined functions.
    """

    name = "_call_user_function"
    args = ["function_name"]
    help = "Internal: Call user function"
    category = "internal"
    variadic = True

    @classmethod
    def execute(cls, function_name: str, *args) -> Any:
        """Call a user-defined function.

        Args:
            function_name: Name of the function to call
            *args: Arguments to pass to the function

        Returns:
            Function result
        """
        registry = get_function_registry()
        func = registry.get(function_name)

        if func is None:
            raise ValueError(f"Function '{function_name}' is not defined")

        # Check argument count
        if len(args) != len(func.parameters):
            expected = len(func.parameters)
            got = len(args)
            raise ValueError(
                f"Function '{function_name}' expects {expected} argument(s), got {got}"
            )

        # Create new variable scope
        store = get_variable_store()
        store.push_scope()

        try:
            # Bind parameters to arguments
            for param, arg in zip(func.parameters, args):
                store.set(param, arg)

            # Execute function body
            # Parse the body as a command
            tokens = func.body.split()
            if not tokens:
                raise ValueError(f"Function '{function_name}' has empty body")

            operation = tokens[0]
            operation_args = tokens[1:] if len(tokens) > 1 else []

            # Execute the operation
            from core.plugin_manager import PluginManager
            mgr = PluginManager()
            mgr.discover_plugins()
            result = mgr.execute_operation(operation, *operation_args)

            return result

        finally:
            # Always pop the scope
            store.pop_scope()


# Helper function to check if a name is a user function
def is_user_function(name: str) -> bool:
    """Check if a name corresponds to a user-defined function.

    Args:
        name: Name to check

    Returns:
        True if it's a user function
    """
    registry = get_function_registry()
    return registry.exists(name)
