#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path
from typing import Sequence

from cli.command_parser import (
    create_argument_parser,
    create_global_argument_parser,
    format_unknown_operation_error,
    parse_and_validate_args,
    parse_global_args,
)
from core.plugin_manager import PluginManager
from utils.helpers import format_plugin_list

def main(argv: Sequence[str] | None = None) -> int:
    """Main entry point for the math CLI."""

    argv = list(argv) if argv is not None else sys.argv[1:]

    global_parser = create_global_argument_parser()
    global_args, remaining_args = parse_global_args(global_parser, argv)

    plugin_manager = _initialize_plugin_manager(
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
        from cli.interactive_mode import run_interactive_mode

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

    if global_args.full_screen_tui:
        from cli.full_screen_tui import run_full_screen_tui

        try:
            run_full_screen_tui(plugin_manager, operations_metadata)
        except RuntimeError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
        return 0

    if not remaining_args:
        operation_parser.print_help()
        return 0

    expression_input = " ".join(remaining_args)
    if _should_use_command_engine(expression_input, remaining_args, operations_metadata):
        from cli.command_engine import MathCommandEngine

        try:
            execution = MathCommandEngine(
                plugin_manager,
                operations_metadata,
                record_history=False,
            ).execute(expression_input)
            print(f"Result: {execution.result}")
            return 0
        except ValueError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 2

    operation_name = remaining_args[0]
    if not operation_name.startswith('-') and operation_name not in operations_metadata:
        print(
            format_unknown_operation_error(
                operation_name,
                operations_metadata,
                prog=operation_parser.prog,
            ),
            file=sys.stderr,
        )
        return 2

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
        return exc.code

    return 0


def _should_use_command_engine(
    expression_input: str,
    remaining_args: Sequence[str],
    operations_metadata: dict,
) -> bool:
    """Return True for one-shot inputs that use iOS-style syntax."""

    from cli.command_engine import MathCommandEngine

    if not remaining_args:
        return False

    if remaining_args[0].startswith("-"):
        return False

    if "|" in remaining_args or "|" in expression_input:
        return True

    if remaining_args[0] == "chain":
        return True

    if "=" in remaining_args or "=" in expression_input:
        return True

    if (
        remaining_args[0] == "set"
        and len(remaining_args) > 3
        and MathCommandEngine.should_treat_as_expression(
            " ".join(remaining_args[2:]),
            operations_metadata,
        )
    ):
        return True

    return MathCommandEngine.should_treat_as_expression(
        expression_input,
        operations_metadata,
    )


def _initialize_plugin_manager(
    extra_directories: Sequence[str],
) -> PluginManager:
    """Create a plugin manager configured with built-in and custom plugins."""

    plugin_manager = PluginManager()

    for directory in map(Path, extra_directories):
        plugin_manager.add_plugin_directory(str(directory.resolve()))

    plugin_manager.discover_plugins()
    return plugin_manager


if __name__ == "__main__":
    sys.exit(main())
