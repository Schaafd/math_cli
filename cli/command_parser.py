import argparse
from typing import Dict, List, Any, Optional

def create_argument_parser(operations_metadata: Dict[str, Dict[str, Any]]) -> argparse.ArgumentParser:
    """
    Create and configure an argparse.ArgumentParser for the given operations.
    
    Builds a parser with subcommands for each operation described in `operations_metadata`.
    Each operation gets its own subparser (name = operation key) with help text from
    op_info['help'] and positional arguments for every name listed in op_info['args']
    (each parsed as float). Also adds global options:
      - --interactive / -i : enable interactive mode (store_true)
      - --plugin-dir         : can be provided multiple times to collect plugin directories (append)
      - --list-plugins       : list available operation plugins (store_true)
    
    Parameters:
        operations_metadata (Dict[str, Dict[str, Any]]): Mapping from operation name to its metadata.
            Each metadata dict must include:
              - 'help' (str): help text for the operation
              - 'args' (Iterable[str]): ordered names of positional arguments for the operation
    
    Returns:
        argparse.ArgumentParser: Configured parser with subparsers and global options.
    """
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

def parse_and_validate_args(args_namespace: Any, operations_metadata: Dict[str, Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    Validate parsed CLI arguments against registered operations and extract the selected operation with its ordered arguments.
    
    Checks that args_namespace.operation (if set) matches a key in operations_metadata, ensures all required argument names listed in operations_metadata[operation]['args'] are present on the namespace, and returns a mapping with the operation name and a list of argument values in the order defined by the metadata. If no operation is specified on the namespace, an empty dict is returned.
    
    Parameters:
        args_namespace: The namespace object produced by argparse.parse_args() (or equivalent). Must expose an 'operation' attribute and attributes for each operation argument name.
        operations_metadata: Mapping of operation name -> metadata dict. Each metadata dict must include an 'args' sequence listing required argument names (in order).
    
    Returns:
        A dict with keys:
          - 'operation' (str): the chosen operation name
          - 'args' (List[Any]): positional list of argument values in the order specified by the operation metadata
        Returns an empty dict if no operation is specified.
    
    Raises:
        ValueError: If the specified operation is not present in operations_metadata or if a required argument is missing on args_namespace.
    """
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
