def format_plugin_list(operations_metadata):
    """Format the list of available operations for display, organized by category."""
    if not operations_metadata:
        return "No operations available."

    # Define category display order and friendly names
    category_info = {
        'arithmetic': ('Basic Arithmetic', 1),
        'trigonometry': ('Trigonometry', 2),
        'algebra': ('Algebra', 3),
        'calculus': ('Calculus', 4),
        'statistics': ('Statistics', 5),
        'matrix': ('Matrix Operations', 6),
        'complex': ('Complex Numbers', 7),
        'number_theory': ('Number Theory & Combinatorics', 8),
        'geometry': ('Geometry', 9),
        'data_analysis': ('Data Analysis', 10),
        'data_transform': ('Data Transformation', 11),
        'conversion': ('Unit Conversions', 12),
        'constants': ('Mathematical & Physical Constants', 13),
        'general': ('Other Operations', 99),
    }

    # Group operations by category
    categorized = {}
    for name, metadata in operations_metadata.items():
        category = metadata.get('category', 'general')

        # Auto-categorize if still in 'general'
        if category == 'general':
            category = _auto_categorize(name)

        if category not in categorized:
            categorized[category] = []
        categorized[category].append((name, metadata))

    # Sort categories by priority, then alphabetically
    sorted_categories = sorted(
        categorized.keys(),
        key=lambda c: (category_info.get(c, (c, 50))[1], c)
    )

    # Build output
    output = []
    output.append("=" * 80)
    output.append("MATH CLI - AVAILABLE OPERATIONS")
    output.append("=" * 80)
    output.append("")
    output.append(f"Total: {len(operations_metadata)} operations across {len(categorized)} categories")
    output.append("Use --help with any operation for detailed information")
    output.append("")

    for category in sorted_categories:
        if category not in categorized:
            continue

        # Get friendly category name
        friendly_name = category_info.get(category, (category.replace('_', ' ').title(), 50))[0]

        operations = sorted(categorized[category], key=lambda x: x[0])  # Sort alphabetically

        output.append("-" * 80)
        output.append(f"{friendly_name} ({len(operations)} operations)")
        output.append("-" * 80)

        for name, metadata in operations:
            # Format arguments
            if metadata['args']:
                args_display = ' '.join(f'<{arg}>' for arg in metadata['args'])
                if metadata.get('variadic', False):
                    args_display += ' ...'
            else:
                args_display = ''

            # Create operation line
            op_line = f"  {name}"
            if args_display:
                op_line += f" {args_display}"

            output.append(op_line)

            # Add description with indentation
            help_text = metadata['help']
            if len(help_text) > 70:
                # Wrap long descriptions
                help_text = help_text[:67] + "..."
            output.append(f"      {help_text}")

        output.append("")

    output.append("=" * 80)
    output.append("For more information:")
    output.append("  • Interactive mode: math_cli --interactive")
    output.append("  • Operation help: math_cli <operation> --help")
    output.append("  • Documentation: See README.md")
    output.append("=" * 80)

    return "\n".join(output)


def _auto_categorize(operation_name):
    """Automatically categorize an operation based on its name."""
    name_lower = operation_name.lower()

    # Arithmetic
    if any(x in name_lower for x in ['add', 'subtract', 'multiply', 'divide', 'power', 'sqrt', 'abs', 'negate', 'reciprocal']):
        return 'arithmetic'

    # Trigonometry
    if any(x in name_lower for x in ['sin', 'cos', 'tan', 'cot', 'sec', 'csc', 'atan2']):
        return 'trigonometry'

    # Algebra
    if any(x in name_lower for x in ['root', 'log', 'ln', 'exp', 'floor', 'ceil', 'round', 'mod', 'gcd', 'lcm']):
        return 'algebra'

    # Geometry
    if any(x in name_lower for x in ['area_', 'volume_', 'circumference', 'perimeter', 'distance', 'hypotenuse']):
        return 'geometry'

    # Conversion
    if '_to_' in name_lower or any(x in name_lower for x in ['celsius', 'fahrenheit', 'kelvin', 'meters', 'feet', 'miles', 'pounds', 'kilograms']):
        return 'conversion'

    # Constants
    if any(x in name_lower for x in ['pi', 'euler', 'golden_ratio', 'speed_of_light', 'gravity', 'planck', 'avogadro', 'boltzmann', 'gas_constant']):
        return 'constants'

    # Statistics (if not already categorized by plugin)
    if any(x in name_lower for x in ['mean', 'median', 'mode', 'stdev', 'variance', 'max', 'min']):
        return 'statistics'

    return 'general'
