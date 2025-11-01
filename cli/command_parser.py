"""Utilities for building and validating command line parsers."""

import argparse
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


def create_global_argument_parser() -> argparse.ArgumentParser:
    """Create a parser that understands CLI-wide options.

    The returned parser intentionally disables the automatic ``-h/--help``
    handling so that it can be safely reused as a parent for operation
    specific parsers. This keeps the help output consistent while allowing the
    main CLI to parse the global flags up-front.
    """

    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument('--interactive', '-i', action='store_true', help='Run in interactive mode')
    parser.add_argument('--plugin-dir', action='append', help='Directory containing additional plugins')
    parser.add_argument('--list-plugins', action='store_true', help='List available operation plugins')

    # Accessibility options
    parser.add_argument('--no-color', action='store_true', help='Disable colored output (accessibility)')
    parser.add_argument('--no-animations', action='store_true', help='Disable animations (accessibility)')
    parser.add_argument('--screen-reader', action='store_true', help='Enable screen reader mode (accessibility)')
    parser.add_argument('--high-contrast', action='store_true', help='Enable high contrast mode (accessibility)')

    return parser


def parse_global_args(
    parser: argparse.ArgumentParser,
    argv: Sequence[str],
) -> Tuple[argparse.Namespace, List[str]]:
    """Parse known global arguments and return the remainder of ``argv``."""

    return parser.parse_known_args(argv)


def create_argument_parser(
    operations_metadata: Dict[str, Dict[str, Any]],
    *,
    global_parser: Optional[argparse.ArgumentParser] = None,
) -> argparse.ArgumentParser:
    """Create and configure an argument parser based on registered operations."""

    parents: Iterable[argparse.ArgumentParser] = (global_parser,) if global_parser else ()
    parser = argparse.ArgumentParser(
        description='Perform mathematical operations',
        parents=list(parents),
    )
    subparsers = parser.add_subparsers(dest='operation', help='Operation to perform')

    # Add subparsers for each operation
    for op_name, op_info in operations_metadata.items():
        op_parser = subparsers.add_parser(op_name, help=op_info['help'])
        is_variadic = op_info.get('variadic', False)

        if is_variadic:
            # For variadic functions, use nargs='+' to accept one or more arguments
            op_parser.add_argument('values', type=float, nargs='+', help='Numbers to process')
        else:
            # For fixed-argument functions, add each argument individually
            for arg in op_info['args']:
                op_parser.add_argument(arg, type=float, help=f'{arg} value')

    # Global options are handled separately in the main function

    return parser

def parse_and_validate_args(args_namespace: Any, operations_metadata: Dict) -> Dict:
    """Parse and validate command line arguments."""
    if args_namespace.operation:
        operation = args_namespace.operation
        if operation not in operations_metadata:
            raise ValueError(f"Unknown operation: {operation}")

        is_variadic = operations_metadata[operation].get('variadic', False)

        if is_variadic:
            # For variadic functions, get the values list
            if hasattr(args_namespace, 'values'):
                op_args = args_namespace.values
            else:
                raise ValueError(f"No arguments provided for variadic operation '{operation}'")
        else:
            # Get required arguments for fixed-argument operations
            required_args = operations_metadata[operation]['args']

            # Prepare arguments for operation execution
            op_args = []
            for arg_name in required_args:
                if not hasattr(args_namespace, arg_name):
                    raise ValueError(f"Missing required argument '{arg_name}' for operation '{operation}'")
                op_args.append(getattr(args_namespace, arg_name))

        return {
            'operation': operation,
            'args': op_args
        }

    return {}
