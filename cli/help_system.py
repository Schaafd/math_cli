"""Enhanced help system for math_cli with detailed operation information."""

from typing import Dict, List
from utils.visual import console, print_help_panel
from rich.table import Table
from rich import box
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text


def show_operation_help(operation: str, operations_metadata: Dict):
    """Show detailed help for a specific operation.

    Args:
        operation: The operation name
        operations_metadata: Dictionary of operation metadata
    """
    if operation not in operations_metadata:
        from utils.visual import print_error
        print_error(f"Unknown operation: {operation}", "Type 'help' for a list of operations")
        return

    op_info = operations_metadata[operation]

    # Build help content
    title = f"[bold cyan]{operation}[/bold cyan]"

    # Arguments section
    if op_info['args']:
        args_list = [f"<{arg}>" for arg in op_info['args']]
        if op_info.get('variadic', False):
            args_list.append("...")
        args_str = " ".join(args_list)
        signature = f"[yellow]{operation}[/yellow] [cyan]{args_str}[/cyan]"
    else:
        signature = f"[yellow]{operation}[/yellow]"

    # Build the help text
    help_text = f"""
{signature}

[bold]Description:[/bold]
{op_info['help']}
"""

    # Add argument details
    if op_info['args']:
        help_text += "\n[bold]Arguments:[/bold]\n"
        for arg in op_info['args']:
            help_text += f"  • [cyan]{arg}[/cyan] - Parameter value\n"

        if op_info.get('variadic', False):
            help_text += "  • [dim]...[/dim] - Accepts multiple values\n"

    # Add examples if available (could be enhanced in future)
    help_text += "\n[bold]Examples:[/bold]\n"
    if op_info['args']:
        if op_info.get('variadic', False):
            help_text += f"  [dim]❯[/dim] {operation} 10 20 30\n"
        elif len(op_info['args']) == 1:
            help_text += f"  [dim]❯[/dim] {operation} 16\n"
        elif len(op_info['args']) == 2:
            help_text += f"  [dim]❯[/dim] {operation} 10 5\n"
        else:
            example_args = " ".join(["10"] * len(op_info['args']))
            help_text += f"  [dim]❯[/dim] {operation} {example_args}\n"
    else:
        help_text += f"  [dim]❯[/dim] {operation}\n"

    # Find related operations (same category or similar name prefix)
    related = find_related_operations(operation, operations_metadata, max_related=5)
    if related:
        help_text += "\n[bold]Related Operations:[/bold]\n"
        help_text += "  " + ", ".join([f"[cyan]{op}[/cyan]" for op in related])

    # Display the help panel
    panel = Panel(
        help_text.strip(),
        title=title,
        border_style="cyan",
        box=box.ROUNDED,
        padding=(1, 2)
    )
    console.print(panel)


def search_operations(query: str, operations_metadata: Dict) -> List[str]:
    """Search for operations matching a query.

    Args:
        query: Search query string
        operations_metadata: Dictionary of operation metadata

    Returns:
        List of matching operation names
    """
    query_lower = query.lower()
    matches = []

    for op_name, op_info in operations_metadata.items():
        # Check if query matches operation name
        if query_lower in op_name.lower():
            matches.append(op_name)
            continue

        # Check if query matches description
        if query_lower in op_info['help'].lower():
            matches.append(op_name)
            continue

    return sorted(matches)


def show_search_results(query: str, operations_metadata: Dict):
    """Show search results for operations.

    Args:
        query: Search query
        operations_metadata: Dictionary of operation metadata
    """
    matches = search_operations(query, operations_metadata)

    if not matches:
        from utils.visual import print_info
        print_info(f"No operations found matching '{query}'")
        return

    # Create results table
    table = Table(
        title=f"Search Results for '{query}' ({len(matches)} found)",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan"
    )
    table.add_column("Operation", style="yellow")
    table.add_column("Arguments", style="dim")
    table.add_column("Description", style="white")

    for op_name in matches[:20]:  # Limit to 20 results
        op_info = operations_metadata[op_name]
        args_str = ' '.join(f'<{arg}>' for arg in op_info['args'])
        if op_info.get('variadic', False):
            args_str += ' ...'

        table.add_row(op_name, args_str, op_info['help'])

    console.print(table)

    if len(matches) > 20:
        from utils.visual import print_info
        print_info(f"Showing first 20 of {len(matches)} results")


def show_category_operations(category: str, operations_metadata: Dict):
    """Show operations by category.

    Args:
        category: Category name
        operations_metadata: Dictionary of operation metadata
    """
    # Define categories based on operation name patterns
    categories = {
        'arithmetic': ['add', 'subtract', 'multiply', 'divide', 'mod', 'power', 'sqrt'],
        'trigonometry': ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'sinh', 'cosh', 'tanh'],
        'statistics': ['mean', 'median', 'mode', 'std_dev', 'variance', 'max', 'min'],
        'geometry': ['area_', 'volume_', 'circumference', 'perimeter', 'distance'],
        'conversion': ['_to_', 'celsius', 'fahrenheit', 'kelvin', 'meters', 'feet'],
        'complex': ['complex_'],
        'constants': ['pi', 'e', 'golden_ratio', 'speed_of_light'],
    }

    category_lower = category.lower()

    # Find operations matching the category
    matches = []
    if category_lower in categories:
        patterns = categories[category_lower]
        for op_name in operations_metadata.keys():
            for pattern in patterns:
                if pattern in op_name.lower():
                    matches.append(op_name)
                    break

    if not matches:
        from utils.visual import print_error
        valid_categories = ', '.join(categories.keys())
        print_error(
            f"Unknown category: {category}",
            f"Valid categories: {valid_categories}"
        )
        return

    # Show results
    table = Table(
        title=f"{category.title()} Operations ({len(matches)} found)",
        box=box.ROUNDED
    )
    table.add_column("Operation", style="yellow bold")
    table.add_column("Description", style="white")

    for op_name in sorted(matches):
        op_info = operations_metadata[op_name]
        table.add_row(op_name, op_info['help'])

    console.print(table)


def find_related_operations(operation: str, operations_metadata: Dict, max_related: int = 5) -> List[str]:
    """Find operations related to the given operation.

    Args:
        operation: The operation name
        operations_metadata: Dictionary of operation metadata
        max_related: Maximum number of related operations to return

    Returns:
        List of related operation names
    """
    if operation not in operations_metadata:
        return []

    related = []

    # Find operations with similar prefixes
    prefix = operation.split('_')[0] if '_' in operation else operation[:4]

    for op_name in operations_metadata.keys():
        if op_name == operation:
            continue

        # Check for common prefix
        if op_name.startswith(prefix) or (prefix in op_name):
            related.append(op_name)

    # Limit results
    return related[:max_related]


def show_quick_reference():
    """Show a quick reference guide with common operations."""
    console.print("\n[bold cyan]Quick Reference Guide[/bold cyan]\n")

    # Common operations by category
    categories_ref = {
        "Basic Arithmetic": ["add", "subtract", "multiply", "divide", "power", "sqrt"],
        "Statistics": ["mean", "median", "std_dev", "max", "min"],
        "Trigonometry": ["sin", "cos", "tan", "asin", "acos", "atan"],
        "Special Commands": ["help", "history", "chain", "exit"]
    }

    for category, ops in categories_ref.items():
        console.print(f"[yellow]{category}:[/yellow]", end=" ")
        console.print(", ".join([f"[cyan]{op}[/cyan]" for op in ops]))

    console.print("\n[dim]💡 Tip: Use 'help <operation>' for detailed help on any operation[/dim]\n")
