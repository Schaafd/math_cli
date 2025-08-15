#!/usr/bin/env python3
import sys
import os
from pathlib import Path
from core.plugin_manager import PluginManager
from cli.command_parser import create_argument_parser, parse_and_validate_args
from cli.interactive_mode import run_interactive_mode
from utils.helpers import format_plugin_list

def create_temp_parser():
    """Create a temporary parser that only handles global options."""
    import argparse
    parser = argparse.ArgumentParser(description='Perform mathematical operations', add_help=False)
    parser.add_argument('--plugin-dir', action='append', help='Directory containing additional plugins')
    parser.add_argument('--interactive', '-i', action='store_true', help='Run in interactive mode')
    parser.add_argument('--list-plugins', action='store_true', help='List available operation plugins')
    return parser

def main():
    """Main entry point for the math CLI."""
    # Create plugin manager and discover built-in plugins
    plugin_manager = PluginManager()

    # Add the 'plugins' directory from the installation directory
    base_dir = Path(__file__).parent
    plugin_dir = base_dir / "plugins"
    if plugin_dir.exists():
        plugin_manager.add_plugin_directory(str(plugin_dir))

    # Use a simple parser to extract plugin directories and special flags
    temp_parser = create_temp_parser()
    temp_args, remaining_args = temp_parser.parse_known_args()
    
    # Add any user-specified plugin directories
    if temp_args.plugin_dir:
        for directory in temp_args.plugin_dir:
            plugin_manager.add_plugin_directory(directory)

    # Discover plugins from all registered directories
    plugin_manager.discover_plugins()

    # Get metadata from all loaded operations
    operations_metadata = plugin_manager.get_operations_metadata()

    # If no operations were found, print an error and exit
    if not operations_metadata:
        print("Error: No math operations found.")
        return 1

    # Handle special cases first
    if temp_args.list_plugins:
        print(format_plugin_list(operations_metadata))
        return 0
    
    if temp_args.interactive:
        run_interactive_mode(plugin_manager, operations_metadata)
        return 0
    
    # Now create the full parser with all operations
    parser = create_argument_parser(operations_metadata)
    
    # For operation commands, parse normally
    try:
        args = parser.parse_args()
    except SystemExit as e:
        # If parsing fails, it might be because no operation was specified
        if len(sys.argv) == 1:  # No arguments provided
            parser.print_help()
            return 0
        else:
            # Re-raise the SystemExit to show the original error
            raise

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
