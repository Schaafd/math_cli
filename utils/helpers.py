def format_plugin_list(operations_metadata):
    """Format the list of available operations for display."""
    if not operations_metadata:
        return "No operations available."

    output = "Available operations:\n"
    for name, metadata in sorted(operations_metadata.items()):
        args = ", ".join(metadata['args'])
        output += f"  {name} - {metadata['help']}\n"
        output += f"    Arguments: {args}\n"

    return output
