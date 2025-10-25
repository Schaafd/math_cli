"""Export operations plugin for Math CLI."""

from core.base_operations import MathOperation
from utils.exporters import get_session_manager
from pathlib import Path


class ExportSessionOperation(MathOperation):
    """Export current session to file."""

    name = "export_session"
    args = ["filepath", "?format"]
    help = "Export session: export_session session.json [json|markdown|latex]"
    category = "integration"

    @classmethod
    def execute(cls, filepath: str, format: str = "json") -> str:
        """Export current session.

        Args:
            filepath: Destination file path
            format: Export format (json, markdown, latex)

        Returns:
            Confirmation message
        """
        manager = get_session_manager()

        # Get current session data
        session_data = manager.get_session_data()

        # Export to file
        manager.export_session(session_data, filepath, format)

        # Get file size
        path = Path(filepath)
        size_kb = path.stat().st_size / 1024

        return f"✓ Session exported to {filepath} ({size_kb:.1f} KB, {format} format)"


class ImportSessionOperation(MathOperation):
    """Import session from JSON file."""

    name = "import_session"
    args = ["filepath"]
    help = "Import session: import_session session.json"
    category = "integration"

    @classmethod
    def execute(cls, filepath: str) -> str:
        """Import session from file.

        Args:
            filepath: Source file path

        Returns:
            Confirmation message
        """
        manager = get_session_manager()

        # Import session data
        session_data = manager.import_session(filepath)

        # Restore session
        manager.restore_session(session_data)

        # Count restored items
        var_count = len(session_data.get('variables', {}))
        func_count = len(session_data.get('functions', {}))

        return f"✓ Session imported: {var_count} variables, {func_count} functions"


class ExportVariablesOperation(MathOperation):
    """Export variables to JSON file."""

    name = "export_vars"
    args = ["filepath"]
    help = "Export variables: export_vars variables.json"
    category = "integration"

    @classmethod
    def execute(cls, filepath: str) -> str:
        """Export variables to JSON.

        Args:
            filepath: Destination file path

        Returns:
            Confirmation message
        """
        from core.variables import get_variable_store
        from utils.exporters import JSONExporter

        var_store = get_variable_store()
        variables = var_store.list_all()

        exporter = JSONExporter()
        exporter.export(variables, filepath)

        return f"✓ Exported {len(variables)} variables to {filepath}"


class ImportVariablesOperation(MathOperation):
    """Import variables from JSON file."""

    name = "import_vars"
    args = ["filepath"]
    help = "Import variables: import_vars variables.json"
    category = "integration"

    @classmethod
    def execute(cls, filepath: str) -> str:
        """Import variables from JSON.

        Args:
            filepath: Source file path

        Returns:
            Confirmation message
        """
        import json
        from core.variables import get_variable_store

        with open(filepath, 'r') as f:
            variables = json.load(f)

        var_store = get_variable_store()
        for name, value in variables.items():
            var_store.set(name, value)

        return f"✓ Imported {len(variables)} variables from {filepath}"


class ExportFunctionsOperation(MathOperation):
    """Export user-defined functions to JSON file."""

    name = "export_funcs"
    args = ["filepath"]
    help = "Export functions: export_funcs functions.json"
    category = "integration"

    @classmethod
    def execute(cls, filepath: str) -> str:
        """Export functions to JSON.

        Args:
            filepath: Destination file path

        Returns:
            Confirmation message
        """
        from core.user_functions import get_function_registry
        from utils.exporters import JSONExporter

        func_registry = get_function_registry()
        functions = func_registry.list_all()

        # Convert to serializable format
        func_data = {
            name: {
                'parameters': func.parameters,
                'body': func.body,
                'description': func.description
            }
            for name, func in functions.items()
        }

        exporter = JSONExporter()
        exporter.export(func_data, filepath)

        return f"✓ Exported {len(functions)} functions to {filepath}"


class ImportFunctionsOperation(MathOperation):
    """Import user-defined functions from JSON file."""

    name = "import_funcs"
    args = ["filepath"]
    help = "Import functions: import_funcs functions.json"
    category = "integration"

    @classmethod
    def execute(cls, filepath: str) -> str:
        """Import functions from JSON.

        Args:
            filepath: Source file path

        Returns:
            Confirmation message
        """
        import json
        from core.user_functions import get_function_registry

        with open(filepath, 'r') as f:
            func_data = json.load(f)

        func_registry = get_function_registry()
        for name, func_info in func_data.items():
            func_registry.define(
                name,
                func_info.get('parameters', []),
                func_info.get('body', ''),
                func_info.get('description')
            )

        return f"✓ Imported {len(func_data)} functions from {filepath}"
