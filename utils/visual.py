"""Visual formatting utilities for math_cli using the rich library."""

from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
from rich import box
from rich.markdown import Markdown
import time
from contextlib import contextmanager

# Global console instance
console = Console()

# Color scheme configuration (can be updated by theme system)
COLORS = {
    'input': 'cyan',
    'output': 'green bold',
    'error': 'red bold',
    'warning': 'yellow',
    'info': 'blue',
    'success': 'green',
    'operator': 'magenta',
    'number': 'cyan',
    'command': 'yellow bold',
    'help': 'blue',
    'prompt': 'white',
    'dim': 'dim',
    'highlight': 'bright_cyan bold',
    'banner_primary': 'bright_cyan bold',
    'banner_secondary': 'cyan',
    'banner_title': 'bright_yellow bold',
    'table_header': 'bold cyan',
    'table_border': 'cyan',
}

# User preferences (can be loaded from config file)
class VisualPreferences:
    """Store user preferences for visual output."""
    def __init__(self):
        self.colors_enabled = True
        self.animations_enabled = True
        self.theme = 'default'  # default, light, dark, high-contrast
        self.show_tips = True

    def disable_colors(self):
        """Disable all color output."""
        self.colors_enabled = False

    def disable_animations(self):
        """Disable all animations."""
        self.animations_enabled = False

# Global preferences instance
preferences = VisualPreferences()


def load_theme_from_config():
    """Load and apply the theme from configuration."""
    try:
        from utils.config import get_config
        from utils.themes import apply_theme_to_visual

        config = get_config()
        theme_name = config.get('theme', 'default')

        # Apply the theme
        apply_theme_to_visual(theme_name)

        # Update preferences from config
        preferences.colors_enabled = config.get('colors_enabled', True)
        preferences.animations_enabled = config.get('animations_enabled', True)
        preferences.show_tips = config.get('show_tips', True)

    except ImportError:
        # If config or themes not available, use defaults
        pass


def print_welcome_banner():
    """Display an animated welcome banner."""
    if not preferences.colors_enabled:
        print("Math CLI - Interactive Mode")
        return

    banner_text = r"""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║     __  __       _   _        ____ _     ___              ║
║    |  \/  | __ _| |_| |__    / ___| |   |_ _|             ║
║    | |\/| |/ _` | __| '_ \  | |   | |    | |              ║
║    | |  | | (_| | |_| | | | | |___| |___ | |              ║
║    |_|  |_|\__,_|\__|_| |_|  \____|_____|___|             ║
║                                                           ║
║         Interactive Mathematical Operations               ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """

    if preferences.animations_enabled:
        # Animated banner with color gradient
        lines = banner_text.strip().split('\n')
        for i, line in enumerate(lines):
            if i < 3 or i > len(lines) - 3:
                style = COLORS.get('banner_primary', 'bright_cyan bold')
            elif i == len(lines) // 2:
                style = COLORS.get('banner_title', 'bright_yellow bold')
            else:
                style = COLORS.get('banner_secondary', 'cyan')
            console.print(line, style=style)
            time.sleep(0.05)
    else:
        console.print(banner_text, style=COLORS.get('banner_primary', 'bright_cyan bold'))

    console.print()


def print_result(value, label="Result"):
    """Print a calculation result with rich formatting."""
    if not preferences.colors_enabled:
        print(f"{label}: {value}")
        return

    # Format the number nicely
    formatted_value = format_number(value)

    # Create a panel for the result
    result_text = Text()
    result_text.append(f"{label}: ", style=COLORS['info'])
    result_text.append(formatted_value, style=COLORS['output'])

    if preferences.animations_enabled:
        # Add success indicator
        result_text.append(" ✓", style=COLORS['success'])

    console.print(result_text)


def format_number(value):
    """Format a number for display with proper notation."""
    if isinstance(value, (int, float)):
        # Handle very large or very small numbers
        if abs(value) > 1e6 or (abs(value) < 1e-3 and value != 0):
            return f"{value:.6e}"
        # Handle integers
        elif isinstance(value, int) or value.is_integer():
            return f"{int(value):,}"
        # Handle floats
        else:
            return f"{value:,.6f}".rstrip('0').rstrip('.')
    return str(value)


def print_error(message, suggestion=None):
    """Print an error message with rich formatting."""
    if not preferences.colors_enabled:
        print(f"Error: {message}")
        if suggestion:
            print(f"Suggestion: {suggestion}")
        return

    error_panel = Panel(
        Text(message, style=COLORS['error']),
        title="[bold red]Error[/bold red]",
        border_style="red",
        box=box.ROUNDED
    )
    console.print(error_panel)

    if suggestion:
        console.print(f"💡 [yellow]Suggestion:[/yellow] {suggestion}")


def print_warning(message):
    """Print a warning message with rich formatting."""
    if not preferences.colors_enabled:
        print(f"Warning: {message}")
        return

    console.print(f"⚠️  [yellow]{message}[/yellow]")


def print_info(message):
    """Print an informational message with rich formatting."""
    if not preferences.colors_enabled:
        print(message)
        return

    console.print(f"ℹ️  [blue]{message}[/blue]")


def print_success(message):
    """Print a success message with rich formatting."""
    if not preferences.colors_enabled:
        print(message)
        return

    if preferences.animations_enabled:
        console.print(f"✓ [green bold]{message}[/green bold]")
    else:
        console.print(f"[green]{message}[/green]")


def highlight_expression(expression):
    """Highlight mathematical expression with syntax colors."""
    if not preferences.colors_enabled:
        return expression

    # Create a Text object with syntax highlighting
    text = Text()

    # Simple tokenization for mathematical expressions
    import re
    tokens = re.findall(r'\d+\.?\d*|\+|\-|\*|\/|\(|\)|[a-zA-Z_]\w*', expression)

    for token in tokens:
        if token.replace('.', '').replace('-', '').isdigit():
            # Number
            text.append(token, style=COLORS['number'])
        elif token in ['+', '-', '*', '/', '(', ')']:
            # Operator
            text.append(token, style=COLORS['operator'])
        else:
            # Function or variable
            text.append(token, style=COLORS['command'])

    return text


def print_history_table(entries):
    """Print calculation history as a formatted table."""
    if not entries:
        print_info("History is empty")
        return

    if not preferences.colors_enabled:
        print("\nCalculation History:")
        for i, entry in enumerate(entries):
            print(f"{i+1}: {entry['command']} = {entry['result']}")
        return

    table = Table(
        title="Calculation History",
        box=box.ROUNDED,
        header_style=COLORS.get('table_header', 'bold cyan'),
        border_style=COLORS.get('table_border', 'cyan')
    )
    table.add_column("#", style=COLORS.get('number', 'cyan'), width=5)
    table.add_column("Command", style=COLORS.get('command', 'yellow'))
    table.add_column("Result", style=COLORS.get('output', 'green bold'))
    table.add_column("Time", style=COLORS.get('dim', 'dim'))

    for i, entry in enumerate(entries):
        timestamp = entry.get('timestamp', '')
        table.add_row(
            str(i + 1),
            entry['command'],
            format_number(entry['result']),
            timestamp
        )

    console.print(table)


def print_help_panel(title, content):
    """Print a help panel with formatted content."""
    if not preferences.colors_enabled:
        print(f"\n{title}")
        print(content)
        return

    panel = Panel(
        Markdown(content),
        title=f"[bold blue]{title}[/bold blue]",
        border_style="blue",
        box=box.ROUNDED,
        padding=(1, 2)
    )
    console.print(panel)


def print_operations_table(operations_metadata):
    """Print available operations as a formatted table."""
    if not preferences.colors_enabled:
        print("\nAvailable operations:")
        for op_name, op_info in operations_metadata.items():
            args_str = ' '.join(op_info['args'])
            print(f"  {op_name} {args_str} - {op_info['help']}")
        return

    table = Table(
        title="Available Operations",
        box=box.ROUNDED,
        header_style=COLORS.get('table_header', 'bold cyan'),
        border_style=COLORS.get('table_border', 'cyan')
    )
    table.add_column("Operation", style=COLORS.get('command', 'yellow bold'))
    table.add_column("Arguments", style=COLORS.get('number', 'cyan'))
    table.add_column("Description", style=COLORS.get('info', 'white'))

    # Group operations by category if available
    for op_name, op_info in sorted(operations_metadata.items()):
        args_str = ' '.join(op_info['args'])
        if op_info.get('variadic', False):
            args_str += " ..."

        table.add_row(
            op_name,
            args_str,
            op_info['help']
        )

    console.print(table)


@contextmanager
def loading_spinner(message="Calculating..."):
    """Context manager for showing a loading spinner during long operations."""
    if not preferences.animations_enabled:
        yield
        return

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True
    ) as progress:
        progress.add_task(description=message, total=None)
        yield


def print_chain_step(step_num, operation, result):
    """Print a step in a chain calculation."""
    if not preferences.colors_enabled:
        print(f"Step {step_num}: {operation} = {result}")
        return

    text = Text()
    text.append(f"Step {step_num}: ", style=COLORS['info'])
    text.append(operation, style=COLORS['command'])
    text.append(" = ", style=COLORS['dim'])
    text.append(format_number(result), style=COLORS['output'])

    if preferences.animations_enabled:
        text.append(" →", style=COLORS['success'])

    console.print(text)


def print_final_result(result):
    """Print the final result of a chain calculation."""
    if not preferences.colors_enabled:
        print(f"Final result: {result}")
        return

    text = Text()
    text.append("Final result: ", style="bright_yellow bold")
    text.append(format_number(result), style="bright_green bold")

    if preferences.animations_enabled:
        text.append(" ✓", style="bright_green")

    console.print(text)


def print_tip(message):
    """Print a helpful tip message."""
    if not preferences.show_tips or not preferences.colors_enabled:
        return

    console.print(f"💡 [dim italic]Tip: {message}[/dim italic]")


def get_styled_prompt(previous_result=None):
    """Get a styled prompt string for input."""
    if not preferences.colors_enabled:
        prompt = "\nEnter command"
        if previous_result is not None:
            prompt += f" (previous: {previous_result})"
        prompt += ": "
        return prompt

    text = Text()
    text.append("\n", style="")
    text.append("❯ ", style=COLORS['highlight'])

    if previous_result is not None:
        text.append(f"(prev: {format_number(previous_result)}) ", style=COLORS['dim'])

    # Rich doesn't directly support styled input prompts, so we'll return the plain string
    # and print the styled prefix separately
    return text


def clear_screen():
    """Clear the terminal screen."""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def print_separator(char='─', style='dim'):
    """Print a separator line."""
    if not preferences.colors_enabled:
        print(char * 60)
        return

    console.print(char * 60, style=style)
