#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path
from typing import Iterable, Sequence

from cli.command_parser import (
    create_argument_parser,
    create_global_argument_parser,
    parse_and_validate_args,
    parse_global_args,
)
from cli.interactive_mode import run_interactive_mode
from core.plugin_manager import PluginManager
from utils.helpers import format_plugin_list

def main(argv: Sequence[str] | None = None) -> int:
    """Main entry point for the math CLI."""

    argv = list(argv) if argv is not None else sys.argv[1:]

    base_dir = Path(__file__).parent
    global_parser = create_global_argument_parser()
    global_args, remaining_args = parse_global_args(global_parser, argv)

    plugin_manager = _initialize_plugin_manager(
        base_dir,
        global_args.plugin_dir or [],
    )

    operations_metadata = plugin_manager.get_operations_metadata()

    if not operations_metadata:
        print("Error: No math operations found.")
        return 1

    operation_parser = create_argument_parser(
        operations_metadata,
        global_parser=global_parser,
    )

    if not argv:
        operation_parser.print_help()
        return 0

    if global_args.list_plugins:
        print(format_plugin_list(operations_metadata))
        return 0

    if global_args.interactive:
        enable_colors = not global_args.no_color
        enable_animations = not global_args.no_animations

        accessibility_settings = {
            'screen_reader_mode': getattr(global_args, 'screen_reader', False),
            'high_contrast': getattr(global_args, 'high_contrast', False),
        }

        run_interactive_mode(
            plugin_manager,
            operations_metadata,
            enable_colors,
            enable_animations,
            accessibility_settings,
        )
        return 0

    if not remaining_args:
        operation_parser.print_help()
        return 0

    try:
        args = operation_parser.parse_args(remaining_args)
        if args.operation:
            parsed_args = parse_and_validate_args(args, operations_metadata)
            if parsed_args:
                result = plugin_manager.execute_operation(
                    parsed_args['operation'],
                    *parsed_args['args'],
                )
                print(f"Result: {result}")
                return 0
        operation_parser.print_help()
    except SystemExit as exc:
        if exc.code == 0:
            return 0

        if remaining_args:
            op_name = remaining_args[0]
            if op_name not in operations_metadata:
                print(f"Error: Unknown operation '{op_name}'")
                print("\nUse --list-plugins to see available operations")
        return exc.code

    return 0


def _initialize_plugin_manager(
    base_dir: Path,
    extra_directories: Iterable[str],
) -> PluginManager:
    """Create a plugin manager configured with built-in and custom plugins."""

    plugin_manager = PluginManager()

    builtin_dir = base_dir / "plugins"
    directories: Iterable[Path] = [builtin_dir, *map(Path, extra_directories)]

    for directory in directories:
        plugin_manager.add_plugin_directory(str(directory.resolve()))

    plugin_manager.discover_plugins()
    return plugin_manager


if __name__ == "__main__":
    sys.exit(main())
