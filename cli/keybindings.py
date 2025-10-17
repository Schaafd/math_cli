"""Keyboard bindings and shortcuts for math_cli interactive mode."""

from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.application import get_app
from prompt_toolkit.filters import Condition


def create_key_bindings(history_manager=None) -> KeyBindings:
    """Create custom key bindings for the math CLI.

    Args:
        history_manager: Optional history manager for history search

    Returns:
        KeyBindings object with custom shortcuts
    """
    kb = KeyBindings()

    # Ctrl+L to clear screen
    @kb.add('c-l')
    def clear_screen(event):
        """Clear the screen."""
        event.app.renderer.clear()

    # Ctrl+D to exit (in addition to EOF)
    @kb.add('c-d')
    def exit_on_ctrl_d(event):
        """Exit on Ctrl+D."""
        event.app.exit(result='exit')

    # Ctrl+C to gracefully handle keyboard interrupt
    @kb.add('c-c')
    def handle_ctrl_c(event):
        """Handle Ctrl+C gracefully."""
        # Clear the current input buffer
        event.app.current_buffer.reset()

    return kb


def get_bottom_toolbar_text(previous_result=None, show_shortcuts=True):
    """Generate bottom toolbar text with shortcuts and info.

    Args:
        previous_result: The previous calculation result
        show_shortcuts: Whether to show keyboard shortcuts

    Returns:
        Formatted toolbar text
    """
    from prompt_toolkit.formatted_text import HTML

    parts = []

    # Show previous result if available
    if previous_result is not None:
        from utils.visual import format_number
        parts.append(f"Previous: {format_number(previous_result)}")

    # Show keyboard shortcuts
    if show_shortcuts:
        shortcuts = [
            "Ctrl+C: Clear",
            "Ctrl+D: Exit",
            "Ctrl+L: Clear Screen",
            "Tab: Complete",
            "↑↓: History"
        ]
        if parts:
            parts.append(" | ")
        parts.append(" | ".join(shortcuts))

    return HTML(" ".join(parts)) if parts else ""


class ValidationHelper:
    """Helper class for real-time input validation."""

    def __init__(self, operations_metadata):
        """Initialize the validation helper.

        Args:
            operations_metadata: Dictionary of operation metadata
        """
        self.operations_metadata = operations_metadata

    def validate_command(self, text: str) -> tuple:
        """Validate a command input.

        Args:
            text: The command text to validate

        Returns:
            Tuple of (is_valid, error_message, suggestion)
        """
        if not text.strip():
            return (True, "", "")

        # Split into words
        parts = text.strip().split()
        if not parts:
            return (True, "", "")

        # Check if it's a special command
        special_commands = ['help', 'history', 'exit', 'quit', 'chain']
        if parts[0].lower() in special_commands:
            return (True, "", "")

        # Check if operation exists
        op_name = parts[0]
        if op_name not in self.operations_metadata:
            # Try to find suggestions
            from cli.autocompletion import suggest_corrections
            suggestions = suggest_corrections(op_name, self.operations_metadata, max_suggestions=1)
            if suggestions:
                return (False, f"Unknown operation: {op_name}", f"Did you mean '{suggestions[0]}'?")
            return (False, f"Unknown operation: {op_name}", "Type 'help' for available commands")

        # Validate argument count (basic check)
        op_info = self.operations_metadata[op_name]
        required_args = op_info['args']
        provided_args = parts[1:]

        # For variadic functions, just check we have at least one argument if required
        if op_info.get('variadic', False):
            if len(required_args) > 0 and len(provided_args) == 0:
                return (False, f"{op_name} requires at least one argument", "")
        else:
            # For non-variadic, check exact count
            if len(provided_args) < len(required_args):
                missing = len(required_args) - len(provided_args)
                return (False, f"{op_name} needs {missing} more argument(s)", "")

        return (True, "", "")
