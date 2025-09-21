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

    # First, check for global options that don't require operation parsing
    # Create a simple parser for global options only
    global_parser = create_global_argument_parser()

    # If no arguments provided, show help and exit
    if len(sys.argv) == 1:
        global_parser.print_help()
        return 0

    # Parse only known global arguments first
    global_args, remaining_args = global_parser.parse_known_args()

    # Add any user-specified plugin directories
    if global_args.plugin_dir:
        for directory in global_args.plugin_dir:
            plugin_manager.add_plugin_directory(directory)

    # Discover plugins from all registered directories
    plugin_manager.discover_plugins()

    # Get metadata from all loaded operations
    operations_metadata = plugin_manager.get_operations_metadata()

    # If no operations were found, print an error and exit
    if not operations_metadata:
        print("Error: No math operations found.")
        return 1

    # Handle list-plugins option
    if global_args.list_plugins:
        print(format_plugin_list(operations_metadata))
        return 0

    # Handle interactive mode
    if global_args.interactive:
        run_interactive_mode(plugin_manager, operations_metadata)
        return 0

    # If we get here, we should have an operation command
    # Create the full parser with all operations
    parser = create_argument_parser(operations_metadata)

    try:
        args = parser.parse_args()

        # Handle operation command
        if args.operation:
            parsed_args = parse_and_validate_args(args, operations_metadata)
            if parsed_args:
                result = plugin_manager.execute_operation(
                    parsed_args['operation'],
                    *parsed_args['args']
                )
                print(f"Result: {result}")
                return 0
        else:
            # No operation specified, show help
            parser.print_help()
    except SystemExit as e:
        # argparse calls sys.exit on error, catch it to show our help
        if remaining_args:
            print(f"Error: Unknown operation '{remaining_args[0]}'")
            print("\nUse --list-plugins to see available operations")
        return e.code

    return 0

def create_global_argument_parser():
    """Create argument parser for global options only."""
    import argparse
    parser = argparse.ArgumentParser(description='Perform mathematical operations', add_help=False)

    # Add global options
    parser.add_argument('--interactive', '-i', action='store_true', help='Run in interactive mode')
    parser.add_argument('--plugin-dir', action='append', help='Directory containing additional plugins')
    parser.add_argument('--list-plugins', action='store_true', help='List available operation plugins')
    parser.add_argument('--help', '-h', action='store_true', help='Show help message')

    return parser

if __name__ == "__main__":
    sys.exit(main())
