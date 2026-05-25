"""Utilities for building and validating command line parsers."""

import argparse
from difflib import get_close_matches
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


def coerce_argument_value(value: Any) -> Any:
    """Convert CLI tokens to primitive values while preserving text inputs."""

    if not isinstance(value, str):
        return value

    if value.startswith('$'):
        return value

    lowered = value.lower()
    if lowered == 'true':
        return True
    if lowered == 'false':
        return False

    try:
        if '.' not in value and 'e' not in lowered:
            return int(value)
        return float(value)
    except ValueError:
        return value


def _argument_specs(op_info: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Return normalized argument specs for operation metadata."""

    if op_info.get('arg_specs'):
        return op_info['arg_specs']

    specs = []
    for raw_arg in op_info.get('args', []):
        name = str(raw_arg)
        required = True
        variadic = False
        if name.startswith('?'):
            required = False
            name = name[1:]
        if name.startswith('*'):
            variadic = True
            name = name[1:]
        specs.append({
            'name': name,
            'display': raw_arg,
            'required': required,
            'variadic': variadic,
            'type': 'string',
        })
    return specs


def create_global_argument_parser() -> argparse.ArgumentParser:
    """Create a parser that understands CLI-wide options.

    The returned parser intentionally disables the automatic ``-h/--help``
    handling so that it can be safely reused as a parent for operation
    specific parsers. This keeps the help output consistent while allowing the
    main CLI to parse the global flags up-front.
    """

    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument('--interactive', '-i', action='store_true', help='Run the full-screen interactive app')
    parser.add_argument(
        '--classic-interactive',
        action='store_true',
        help='Run the classic prompt-loop interactive mode',
    )
    parser.add_argument(
        '--full-screen-tui',
        '--tui',
        action='store_true',
        help='Compatibility alias for the full-screen interactive app',
    )
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
        arg_specs = _argument_specs(op_info)
        is_variadic = op_info.get('variadic', False)

        if is_variadic and not any(spec.get('variadic') for spec in arg_specs):
            dest = arg_specs[0]['name'] if arg_specs else 'values'
            op_parser.add_argument(dest, nargs='+', help='Values to process')
            continue

        for spec in arg_specs:
            kwargs = {'help': f"{spec['name']} value"}
            if spec.get('variadic'):
                kwargs['nargs'] = '+'
            elif not spec.get('required', True):
                kwargs['nargs'] = '?'
                kwargs['default'] = None

            op_parser.add_argument(spec['name'], **kwargs)

    # Global options are handled separately in the main function

    return parser


def suggest_operation_names(
    unknown_operation: str,
    operations_metadata: Dict[str, Dict[str, Any]],
    max_suggestions: int = 3,
) -> List[str]:
    """Return likely operation names for a mistyped command."""

    if not unknown_operation or max_suggestions <= 0:
        return []

    candidates = sorted(operations_metadata.keys())
    unknown_lower = unknown_operation.lower()

    prefix_matches = [
        candidate for candidate in candidates
        if candidate.lower().startswith(unknown_lower)
    ]
    if prefix_matches:
        return prefix_matches[:max_suggestions]

    token_prefix_matches = [
        candidate for candidate in candidates
        if candidate not in prefix_matches
        and any(part.startswith(unknown_lower) for part in candidate.lower().split('_'))
    ]
    close_matches = get_close_matches(
        unknown_operation,
        candidates,
        n=max_suggestions * 2,
        cutoff=0.6,
    )
    substring_matches = [
        candidate for candidate in candidates
        if len(unknown_lower) >= 3
        and unknown_lower in candidate.lower()
        and candidate not in prefix_matches
        and candidate not in token_prefix_matches
    ]

    suggestions = []
    for group in (
        prefix_matches,
        token_prefix_matches,
        close_matches,
        substring_matches,
    ):
        for candidate in group:
            if candidate not in suggestions:
                suggestions.append(candidate)
            if len(suggestions) >= max_suggestions:
                return suggestions

    return suggestions


def format_operation_usage(
    operation: str,
    operation_metadata: Dict[str, Any],
) -> str:
    """Return a compact one-line usage example for an operation."""

    arg_specs = _argument_specs(operation_metadata)
    usage_parts = [operation]

    is_variadic = operation_metadata.get('variadic', False)
    if is_variadic and not any(spec.get('variadic') for spec in arg_specs):
        dest = arg_specs[0]['name'] if arg_specs else 'values'
        usage_parts.append(f"<{dest}> ...")
        return " ".join(usage_parts)

    for spec in arg_specs:
        placeholder = f"<{spec['name']}>"
        if spec.get('variadic'):
            placeholder = f"{placeholder} ..."
        elif not spec.get('required', True):
            placeholder = f"[{placeholder}]"

        usage_parts.append(placeholder)

    return " ".join(usage_parts)


def format_unknown_operation_error(
    unknown_operation: str,
    operations_metadata: Dict[str, Dict[str, Any]],
    *,
    prog: str = "math",
) -> str:
    """Return a concise, user-focused error for an unknown operation."""

    lines = [f"Error: Unknown operation '{unknown_operation}'"]
    suggestions = suggest_operation_names(unknown_operation, operations_metadata)

    if suggestions:
        lines.append(f"Did you mean: {', '.join(suggestions)}?")
        lines.append("")
        lines.append("Try:")
        best_match = suggestions[0]
        usage = format_operation_usage(
            best_match,
            operations_metadata[best_match],
        )
        lines.append(f"  {prog} {usage}")
    else:
        lines.append("No close operation names found.")

    lines.append("")
    lines.append("Use --list-plugins to see available operations.")
    return "\n".join(lines)


def parse_and_validate_args(args_namespace: Any, operations_metadata: Dict) -> Dict:
    """Parse and validate command line arguments."""
    if args_namespace.operation:
        operation = args_namespace.operation
        if operation not in operations_metadata:
            raise ValueError(f"Unknown operation: {operation}")

        is_variadic = operations_metadata[operation].get('variadic', False)
        arg_specs = _argument_specs(operations_metadata[operation])

        if is_variadic and not any(spec.get('variadic') for spec in arg_specs):
            dest = arg_specs[0]['name'] if arg_specs else 'values'
            if hasattr(args_namespace, dest):
                op_args = [coerce_argument_value(value) for value in getattr(args_namespace, dest)]
            else:
                raise ValueError(f"No arguments provided for variadic operation '{operation}'")
        else:
            # Get required arguments for fixed-argument operations
            op_args = []
            for spec in arg_specs:
                arg_name = spec['name']
                if not hasattr(args_namespace, arg_name):
                    raise ValueError(f"Missing required argument '{arg_name}' for operation '{operation}'")
                value = getattr(args_namespace, arg_name)
                if value is None and not spec.get('required', True):
                    continue
                if spec.get('variadic'):
                    op_args.extend(coerce_argument_value(item) for item in value)
                else:
                    op_args.append(coerce_argument_value(value))

        return {
            'operation': operation,
            'args': op_args
        }

    return {}
