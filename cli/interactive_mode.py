from typing import Dict, Any
from utils.history import HistoryManager
from utils.visual import (
    print_welcome_banner,
    print_result,
    print_error,
    print_info,
    print_success,
    print_tip,
    print_operations_table,
    print_history_table,
    print_chain_step,
    print_final_result,
    print_help_panel,
    console,
    preferences
)

# Phase 2: Interactive features
try:
    from prompt_toolkit import PromptSession
    from prompt_toolkit.history import InMemoryHistory
    from prompt_toolkit.formatted_text import HTML
    from cli.autocompletion import MathOperationCompleter, suggest_corrections
    from cli.keybindings import create_key_bindings, get_bottom_toolbar_text
    from cli.help_system import (
        show_operation_help,
        show_search_results,
        show_category_operations,
        show_quick_reference
    )
    PROMPT_TOOLKIT_AVAILABLE = True
except ImportError:
    PROMPT_TOOLKIT_AVAILABLE = False

def run_interactive_mode(plugin_manager, operations_metadata: Dict, enable_colors=True, enable_animations=True) -> None:
    """Run the CLI in interactive mode with rich visual enhancements."""
    # Set visual preferences
    if not enable_colors:
        preferences.disable_colors()
    if not enable_animations:
        preferences.disable_animations()

    # Display welcome banner
    print_welcome_banner()
    print_info("Type 'exit' or 'quit' to exit, 'help' for available commands")

    # Initialize history manager
    history = HistoryManager()

    # Store the last result for reference
    last_result = None

    def show_help():
        """Display help information for all operations."""
        # Show operations table
        print_operations_table(operations_metadata)

        # Show history commands help
        history_help = """
**History Commands:**
- `history` - Show calculation history
- `history <n>` - Show the nth most recent calculation
- `history clear` - Clear calculation history
- `!<n>` - Re-run the nth most recent calculation
        """
        print_help_panel("History Commands", history_help)

        # Show previous result reference help
        result_ref_help = """
**Previous Result Reference:**
- `$` or `ans` - Use the result of the previous calculation
- Example: `add $ 5` (adds 5 to the previous result)
        """
        print_help_panel("Previous Result Reference", result_ref_help)

        # Show chain calculation help
        chain_help = """
**Chained Calculations:**
- Syntax: `chain <operation1> <args1> | <operation2> <args2> | ...`
- Example: `chain add 5 3 | multiply $ 2`
- The result of each operation becomes available as `$` in the next one
        """
        print_help_panel("Chained Calculations", chain_help)

    def parse_command(input_text, allow_chain=True, current_result=None):
        """Parse the user input command and arguments.

        Args:
            input_text: The command text to parse
            allow_chain: Whether to recognize chain commands
            current_result: Override for the last_result (for chain operations)
        """
        # Use current_result if provided, otherwise default to last_result
        result_to_use = current_result if current_result is not None else last_result

        # Handle chained calculations
        if allow_chain and input_text.lower().startswith('chain '):
            return "chain", input_text[6:].strip()  # Return the rest of the command after 'chain'

        else:
            if result_to_use is not None:
                input_text = input_text.replace('$', str(result_to_use))

                # Split the input to properly handle 'ans' replacement
                parts = input_text.split()
                for i in range(len(parts)):
                    if parts[i].lower() == 'ans':
                        parts[i] = str(result_to_use)
                input_text = ' '.join(parts)

        parts = input_text.split()
        if not parts:
            return None, None

        # Handle history commands
        if parts[0] == "history":
            return "history", parts[1:] if len(parts) > 1 else []

        # Handle history recall shorthand (!n)
        if parts[0].startswith("!") and len(parts[0]) > 1:
            try:
                idx = int(parts[0][1:])
                entry = history.get_entry(idx - 1)  # Convert to 0-based index
                if entry:
                    print(f"Re-running: {entry['command']}")
                    return parse_command(entry['command'])
                else:
                    print(f"Error: History entry {idx} not found")
                    return None, None
            except ValueError:
                print(f"Error: Invalid history index: {parts[0][1:]}")
                return None, None

        op_name = parts[0]
        if op_name not in operations_metadata:
            # Use advanced fuzzy matching if available
            if PROMPT_TOOLKIT_AVAILABLE:
                suggestions = suggest_corrections(op_name, operations_metadata, max_suggestions=3)
                suggestion = f"Did you mean: {', '.join(suggestions)}?" if suggestions else "Use 'help' to see available operations"
            else:
                # Fallback to simple prefix matching
                similar_ops = [op for op in operations_metadata.keys() if op.startswith(parts[0][:3])]
                suggestion = f"Did you mean: {', '.join(similar_ops[:3])}?" if similar_ops else "Use 'help' to see available operations"
            print_error(f"Unknown operation: {op_name}", suggestion)
            return None, None

        return op_name, parts[1:]

    def process_args(op_name, arg_parts):
        """Process and validate command arguments."""
        required_args = operations_metadata[op_name]['args']
        is_variadic = operations_metadata[op_name].get('variadic', False)

        # For variadic functions, we need at least one argument (unless explicitly no args required)
        if is_variadic:
            if len(required_args) > 0 and len(arg_parts) == 0:
                print_error(f"{op_name} requires at least one argument",
                           f"Usage: {op_name} <number1> <number2> ...")
                return None
        else:
            # For non-variadic functions, check exact argument count
            if len(arg_parts) < len(required_args):
                print_error(f"Not enough arguments for {op_name}",
                           f"Expected {len(required_args)} arguments: {', '.join(required_args)}")
                return None

        # Parse arguments
        arg_values = []

        if is_variadic:
            # For variadic functions, parse all provided arguments
            for i, arg_part in enumerate(arg_parts):
                try:
                    arg_values.append(float(arg_part))
                except ValueError:
                    print_error(f"Invalid argument '{arg_part}' at position {i+1}",
                               "Expected a numeric value")
                    return None
        else:
            # For fixed-argument functions, parse only the required number
            for i, arg_name in enumerate(required_args):
                try:
                    if arg_name == 'n' and op_name == 'factorial':
                        # Factorial needs integer
                        arg_values.append(int(float(arg_parts[i])))
                    else:
                        arg_values.append(float(arg_parts[i]))
                except ValueError:
                    print_error(f"Invalid argument '{arg_parts[i]}' for parameter '{arg_name}'",
                               "Expected a numeric value")
                    return None

        return arg_values

    def handle_history_command(args):
        """Handle history-related commands."""
        if not args:
            # Display all history
            entries = history.get_all_entries()
            print_history_table(entries)
        elif args[0] == "clear":
            # Clear history
            history.clear()
            print_success("History cleared")
        else:
            # Show specific history entry
            try:
                idx = int(args[0]) - 1  # Convert to 0-based index
                entry = history.get_entry(idx)
                if entry:
                    print_info(f"{args[0]}: {entry['command']} = {entry['result']}")
                else:
                    print_error(f"History entry {args[0]} not found",
                               f"Valid range: 1-{len(history.get_all_entries())}")
            except ValueError:
                print_error(f"Invalid history index: {args[0]}",
                           "Expected a numeric index")

    def handle_chain_command(chain_text):
        """Handle a chain of calculations."""
        nonlocal last_result

        # Split the chain by the pipe symbol
        operations = chain_text.split('|')
        if not operations:
            print_error("No operations in chain",
                       "Usage: chain <op1> <args> | <op2> <args> | ...")
            return

        chain_result = None
        full_command = "chain " + chain_text
        temp_result = last_result  # Store original last_result to restore if needed

        # Process each operation in the chain
        for i, operation in enumerate(operations):
            operation = operation.strip()
            if not operation:
                continue

            # Parse the operation (with current chain result)
            # Use the updated parse_command that takes a current_result parameter
            op_name, arg_parts = parse_command(
                operation,
                allow_chain=False,
                current_result=chain_result
            )

            if not op_name:
                print_error(f"Invalid operation in chain segment {i+1}",
                           f"Check the syntax of: {operation}")
                last_result = temp_result  # Restore original last_result
                return

            # Process arguments
            arg_values = process_args(op_name, arg_parts)

            if arg_values is None:
                last_result = temp_result  # Restore original last_result
                return

            try:
                # Execute the operation
                result = plugin_manager.execute_operation(op_name, *arg_values)
                chain_result = result

                # Show intermediate result with visual formatting
                print_chain_step(i+1, operation, result)

            except ValueError as e:
                print_error(f"Error in chain segment {i+1}: {str(e)}",
                           "Check your operation arguments")
                last_result = temp_result  # Restore original last_result
                return

        # Store the final result and add to history
        if chain_result is not None:
            print_final_result(chain_result)
            history.add_entry(full_command, chain_result)
            # Update the session's last_result with the chain's final result
            last_result = chain_result
            return chain_result
        else:
            # If no result was produced, restore the original last_result
            last_result = temp_result

        return None

    # Show initial tips about features
    console.print()
    print_tip("Use '$' or 'ans' to reference the previous result in calculations")
    print_tip("Use 'chain' to perform multiple calculations in sequence")

    if PROMPT_TOOLKIT_AVAILABLE and preferences.colors_enabled:
        print_tip("Press [Tab] for autocompletion, [Ctrl+L] to clear screen")
        print_tip("Use 'help <operation>' for detailed help on any command")
    else:
        print_tip("Type 'help' for a complete list of available commands")

    # Setup prompt_toolkit session if available
    if PROMPT_TOOLKIT_AVAILABLE and preferences.colors_enabled:
        session = PromptSession(
            history=InMemoryHistory(),
            completer=MathOperationCompleter(operations_metadata),
            complete_while_typing=False,  # Only complete on Tab
            key_bindings=create_key_bindings(history),
            bottom_toolbar=lambda: get_bottom_toolbar_text(last_result, show_shortcuts=True)
        )
    else:
        session = None

    while True:
        try:
            # Get user input with prompt_toolkit or standard input
            if session:
                # Use prompt_toolkit for enhanced input
                if last_result is not None:
                    from utils.visual import format_number
                    prompt_text = HTML(f'\n<ansigreen>❯</ansigreen> <dim>(prev: {format_number(last_result)})</dim> ')
                else:
                    prompt_text = HTML('\n<ansigreen>❯</ansigreen> ')

                user_input = session.prompt(prompt_text).strip()
            else:
                # Fallback to standard input
                if last_result is not None:
                    from utils.visual import format_number
                    prompt = f"\n❯ (prev: {format_number(last_result)}) " if preferences.colors_enabled else f"\nEnter command (previous: {last_result}): "
                else:
                    prompt = "\n❯ " if preferences.colors_enabled else "\nEnter command: "

                user_input = input(prompt).strip()

            if user_input.lower() in ('exit', 'quit'):
                print_success("Goodbye! Thanks for using Math CLI")
                break

            # Handle enhanced help commands
            if user_input.lower().startswith('help'):
                parts = user_input.split(maxsplit=1)
                if len(parts) == 1:
                    # Standard help
                    show_help()
                elif PROMPT_TOOLKIT_AVAILABLE:
                    # Enhanced help with argument
                    arg = parts[1]
                    if arg.startswith('search:'):
                        # Search for operations
                        query = arg[7:].strip()
                        show_search_results(query, operations_metadata)
                    elif arg.startswith('category:'):
                        # Show category
                        category = arg[9:].strip()
                        show_category_operations(category, operations_metadata)
                    else:
                        # Show help for specific operation
                        show_operation_help(arg, operations_metadata)
                else:
                    show_help()
                continue

            op_name, arg_parts = parse_command(user_input)
            if not op_name:
                continue

            # Handle special commands
            if op_name == "history":
                handle_history_command(arg_parts)
                continue

            if op_name == "chain":
                result = handle_chain_command(arg_parts)
                # We don't need to update last_result here as it's now handled inside handle_chain_command
                continue

            # Handle regular operations
            arg_values = process_args(op_name, arg_parts)
            if arg_values is None:
                continue

            try:
                result = plugin_manager.execute_operation(op_name, *arg_values)
                print_result(result)

                # Store as the last result for reference
                last_result = result

                # Add to history
                history.add_entry(user_input, result)

            except ValueError as e:
                print_error(str(e), "Please check your input and try again")

        except KeyboardInterrupt:
            print_info("\nOperation interrupted")
        except EOFError:
            print_success("\nGoodbye! Thanks for using Math CLI")
            break
        except Exception as e:
            print_error(f"Unexpected error: {str(e)}",
                       "This might be a bug. Please report it if it persists")
