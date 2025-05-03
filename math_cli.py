#!/usr/bin/env python3
import sys
import os
from pathlib import Path
from core.plugin_manager import PluginManager
from cli.command_parser import create_argument_parser, parse_and_validate_args
from cli.interactive_mode import run_interactive_mode
from utils.helpers import format_plugin_list

def main():
    """Main entry point for the math CLI."""
    # Create plugin manager and discover built-in plugins
    plugin_manager = PluginManager()

    # Add the 'plugins' directory from the installation directory
    base_dir = Path(__file__).parent
    plugin_dir = base_dir / "plugins"
    if plugin_dir.exists():
        plugin_manager.add_plugin_directory(str(plugin_dir))

    # Parse command line arguments
    parser = create_argument_parser({})  # Empty initially, will be updated
    args, unknown = parser.parse_known_args()

    # Add any user-specified plugin directories
    if args.plugin_dir:
        for directory in args.plugin_dir:
            plugin_manager.add_plugin_directory(directory)

    # Discover plugins from all registered directories
    plugin_manager.discover_plugins()

    # Get metadata from all loaded operations
    operations_metadata = plugin_manager.get_operations_metadata()

    # If no operations were found, print an error and exit
    if not operations_metadata:
        print("Error: No math operations found.")
        return 1

    # Now that we have the operations, recreate the parser with complete info
    parser = create_argument_parser(operations_metadata)
    args = parser.parse_args()

    # Handle list-plugins option
    if args.list_plugins:
        print(format_plugin_list(operations_metadata))
        return 0

    # Handle interactive mode
    if args.interactive:
        run_interactive_mode(plugin_manager, operations_metadata)
        return 0

    # Handle operation command
    if args.operation:
        try:
            parsed_args = parse_and_validate_args(args, operations_metadata)
            if parsed_args:
                result = plugin_manager.execute_operation(
                    parsed_args['operation'],
                    *parsed_args['args']
                )
                print(f"Result: {result}")
                return 0
        except ValueError as e:
            print(f"Error: {e}")
            return 1
    else:
        # No operation specified, show help
        parser.print_help()

    return 0

if __name__ == "__main__":
    sys.exit(main())
