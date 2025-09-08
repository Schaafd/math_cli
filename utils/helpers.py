from typing import Dict, Any


def format_plugin_list(operations_metadata: Dict[str, Dict[str, Any]]) -> str:
    """
    Return a human-readable list of available operations.
    
    Given operations_metadata mapping operation names to metadata dicts, returns a multi-line
    string listing each operation and its arguments. If operations_metadata is empty or falsy,
    returns "No operations available." Operations are listed in sorted (deterministic) order
    by name.
    
    Expected metadata shape for each operation:
    - 'args': iterable of strings (used to form the comma-separated Arguments line)
    - 'help': string description
    
    Returns:
        str: Formatted operations list or the "No operations available." message.
    
    Raises:
        KeyError: If a metadata dict is missing the 'args' or 'help' key.
        TypeError: If 'args' is not an iterable of strings (so ", ".join(...) fails).
    """
    if not operations_metadata:
        return "No operations available."

    output = "Available operations:\n"
    for name, metadata in sorted(operations_metadata.items()):
        args = ", ".join(metadata['args'])
        output += f"  {name} - {metadata['help']}\n"
        output += f"    Arguments: {args}\n"

    return output
