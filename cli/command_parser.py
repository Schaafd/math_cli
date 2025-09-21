import argparse
from typing import Dict, List, Any

def create_argument_parser(operations_metadata: Dict) -> argparse.ArgumentParser:
    """Create and configure argument parser based on registered operations."""
    parser = argparse.ArgumentParser(description='Perform mathematical operations')
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
