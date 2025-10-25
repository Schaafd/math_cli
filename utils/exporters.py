"""Export utilities for Math CLI.

Provides various export formats for calculations, results, and sessions.
"""

import json
from typing import Any, Dict, List, Optional
from datetime import datetime
from pathlib import Path


class Exporter:
    """Base class for exporters."""

    def export(self, data: Any, filepath: str) -> None:
        """Export data to file.

        Args:
            data: Data to export
            filepath: Destination file path
        """
        raise NotImplementedError


class MarkdownExporter(Exporter):
    """Export calculations and results as Markdown."""

    def export_calculation(self, operation: str, args: List[str], result: Any, filepath: str) -> None:
        """Export a single calculation.

        Args:
            operation: Operation name
            args: Operation arguments
            result: Calculation result
            filepath: Destination file path
        """
        content = self._format_calculation(operation, args, result)

        with open(filepath, 'a') as f:
            f.write(content + "\n\n")

    def _format_calculation(self, operation: str, args: List[str], result: Any) -> str:
        """Format a calculation as Markdown."""
        args_str = ', '.join(str(arg) for arg in args)
        return f"**{operation}**({args_str}) = `{result}`"

    def export_session(self, session_data: Dict, filepath: str) -> None:
        """Export entire session as Markdown.

        Args:
            session_data: Session data including history, variables, functions
            filepath: Destination file path
        """
        content = []
        content.append("# Math CLI Session")
        content.append(f"\n*Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")

        # Variables
        if 'variables' in session_data and session_data['variables']:
            content.append("## Variables\n")
            for name, value in session_data['variables'].items():
                content.append(f"- `${name}` = `{value}`")
            content.append("")

        # Functions
        if 'functions' in session_data and session_data['functions']:
            content.append("## User-Defined Functions\n")
            for name, func_info in session_data['functions'].items():
                params = ', '.join(f'${p}' for p in func_info.get('parameters', []))
                body = func_info.get('body', '')
                content.append(f"- **{name}**({params}) = `{body}`")
            content.append("")

        # History
        if 'history' in session_data and session_data['history']:
            content.append("## Calculation History\n")
            for i, entry in enumerate(session_data['history'], 1):
                content.append(f"{i}. {entry}")
            content.append("")

        with open(filepath, 'w') as f:
            f.write('\n'.join(content))


class LaTeXExporter(Exporter):
    """Export calculations as LaTeX."""

    def export_calculation(self, operation: str, args: List[str], result: Any, filepath: str) -> None:
        """Export a single calculation as LaTeX.

        Args:
            operation: Operation name
            args: Operation arguments
            result: Calculation result
            filepath: Destination file path
        """
        content = self._format_calculation(operation, args, result)

        with open(filepath, 'a') as f:
            f.write(content + "\n\n")

    def _format_calculation(self, operation: str, args: List[str], result: Any) -> str:
        """Format a calculation as LaTeX."""
        # Map common operations to LaTeX
        latex_ops = {
            'add': '+',
            'subtract': '-',
            'multiply': r'\times',
            'divide': r'\div',
            'power': '^',
            'sqrt': r'\sqrt'
        }

        if operation in latex_ops and len(args) == 2:
            op_symbol = latex_ops[operation]
            if operation == 'power':
                return f"$${args[0]}^{{{args[1]}}} = {result}$$"
            else:
                return f"$${args[0]} {op_symbol} {args[1]} = {result}$$"
        elif operation == 'sqrt' and len(args) == 1:
            return f"$$\\sqrt{{{args[0]}}} = {result}$$"
        else:
            # Fallback to text format
            args_str = ', '.join(str(arg) for arg in args)
            return f"$$\\text{{{operation}}}({args_str}) = {result}$$"

    def export_session(self, session_data: Dict, filepath: str) -> None:
        """Export entire session as LaTeX document.

        Args:
            session_data: Session data
            filepath: Destination file path
        """
        content = []
        content.append(r"\documentclass{article}")
        content.append(r"\usepackage{amsmath}")
        content.append(r"\title{Math CLI Session}")
        content.append(f"\\date{{{datetime.now().strftime('%Y-%m-%d')}}}")
        content.append(r"\begin{document}")
        content.append(r"\maketitle")

        # Variables
        if 'variables' in session_data and session_data['variables']:
            content.append(r"\section{Variables}")
            content.append(r"\begin{itemize}")
            for name, value in session_data['variables'].items():
                content.append(f"\\item $${name} = {value}$$")
            content.append(r"\end{itemize}")

        # History
        if 'history' in session_data and session_data['history']:
            content.append(r"\section{Calculations}")
            content.append(r"\begin{enumerate}")
            for entry in session_data['history']:
                content.append(f"\\item {entry}")
            content.append(r"\end{enumerate}")

        content.append(r"\end{document}")

        with open(filepath, 'w') as f:
            f.write('\n'.join(content))


class JSONExporter(Exporter):
    """Export data as JSON."""

    def export(self, data: Any, filepath: str, pretty: bool = True) -> None:
        """Export data as JSON.

        Args:
            data: Data to export (must be JSON serializable)
            filepath: Destination file path
            pretty: If True, use pretty printing
        """
        with open(filepath, 'w') as f:
            if pretty:
                json.dump(data, f, indent=2, default=str)
            else:
                json.dump(data, f, default=str)

    def export_session(self, session_data: Dict, filepath: str) -> None:
        """Export session as JSON.

        Args:
            session_data: Session data
            filepath: Destination file path
        """
        # Add metadata
        export_data = {
            'exported_at': datetime.now().isoformat(),
            'version': '1.0',
            **session_data
        }
        self.export(export_data, filepath, pretty=True)


class SessionManager:
    """Manages session export and import."""

    def __init__(self):
        """Initialize session manager."""
        self.markdown_exporter = MarkdownExporter()
        self.latex_exporter = LaTeXExporter()
        self.json_exporter = JSONExporter()

    def export_session(self, session_data: Dict, filepath: str, format: str = 'json') -> None:
        """Export session to file.

        Args:
            session_data: Session data including variables, functions, history
            filepath: Destination file path
            format: Export format ('json', 'markdown', 'latex')

        Raises:
            ValueError: If format is not supported
        """
        format = format.lower()

        if format == 'json':
            self.json_exporter.export_session(session_data, filepath)
        elif format in ('markdown', 'md'):
            self.markdown_exporter.export_session(session_data, filepath)
        elif format in ('latex', 'tex'):
            self.latex_exporter.export_session(session_data, filepath)
        else:
            raise ValueError(f"Unsupported export format: {format}")

    def import_session(self, filepath: str) -> Dict:
        """Import session from JSON file.

        Args:
            filepath: Source file path

        Returns:
            Session data dictionary

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is not valid JSON
        """
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Session file not found: {filepath}")

        with open(filepath, 'r') as f:
            try:
                data = json.load(f)
                return data
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid session file: {e}")

    def get_session_data(self) -> Dict:
        """Get current session data.

        Returns:
            Dictionary with variables, functions, and other session state
        """
        from core.variables import get_variable_store
        from core.user_functions import get_function_registry

        session_data = {}

        # Get variables
        var_store = get_variable_store()
        session_data['variables'] = var_store.list_all()

        # Get functions
        func_registry = get_function_registry()
        functions = func_registry.list_all()
        session_data['functions'] = {
            name: {
                'parameters': func.parameters,
                'body': func.body,
                'description': func.description
            }
            for name, func in functions.items()
        }

        return session_data

    def restore_session(self, session_data: Dict) -> None:
        """Restore session from data.

        Args:
            session_data: Session data to restore
        """
        from core.variables import get_variable_store
        from core.user_functions import get_function_registry

        # Restore variables
        if 'variables' in session_data:
            var_store = get_variable_store()
            for name, value in session_data['variables'].items():
                var_store.set(name, value)

        # Restore functions
        if 'functions' in session_data:
            func_registry = get_function_registry()
            for name, func_info in session_data['functions'].items():
                func_registry.define(
                    name,
                    func_info.get('parameters', []),
                    func_info.get('body', ''),
                    func_info.get('description')
                )


# Global session manager instance
_session_manager: Optional[SessionManager] = None


def get_session_manager() -> SessionManager:
    """Get the global session manager instance.

    Returns:
        The global SessionManager instance
    """
    global _session_manager
    if _session_manager is None:
        _session_manager = SessionManager()
    return _session_manager
