import argparse
from typing import Dict, List, Any

def create_argument_parser(operations_metadata: Dict) -> argparse.ArgumentParser:
    """Create and configure argument parser based on registered operations."""
    parser = argparse.ArgumentParser(description='Perform mathematical operations')
    subparsers = parser.add_subparsers(dest='operation', help='Operation to perform')

    # Add subparsers for each operation
    for op_name, op_info in operations_metadata.items():
        op_parser = subparsers.add_parser(op_name, help=op_info['help'])
        for arg in op_info['args']:
            op_parser.add_argument(arg, type=float, help=f'{arg} value')

    # Add interactive mode
    parser.add_argument('--interactive', '-i', action='store_true', help='Run in interactive mode')

    # Add plugin directory option
    parser.add_argument('--plugin-dir', action='append', help='Directory containing additional plugins')

    # Add list plugins option
    parser.add_argument('--list-plugins', action='store_true', help='List available operation plugins')

    return parser

def parse_and_validate_args(args_namespace: Any, operations_metadata: Dict) -> Dict:
    """Parse and validate command line arguments."""
    if args_namespace.operation:
        operation = args_namespace.operation
        if operation not in operations_metadata:
            raise ValueError(f"Unknown operation: {operation}")

        # Get required arguments for this operation
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
