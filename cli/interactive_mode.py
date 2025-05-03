from typing import Dict, Any
from utils.history import HistoryManager

def run_interactive_mode(plugin_manager, operations_metadata: Dict) -> None:
    """Run the CLI in interactive mode."""
    print("Mathematical Operations CLI - Interactive Mode")
    print("Type 'exit' or 'quit' to exit, 'help' for available commands")

    # Initialize history manager
    history = HistoryManager()

    # Store the last result for reference
    last_result = None

    def show_help():
        """Display help information for all operations."""
        print("\nAvailable operations:")
        for op_name, op_info in operations_metadata.items():
            args_str = ' '.join(op_info['args'])
            print(f"  {op_name} {args_str} - {op_info['help']}")

        # Add history command help
        print("\nHistory commands:")
        print("  history - Show calculation history")
        print("  history <n> - Show the nth most recent calculation")
        print("  history clear - Clear calculation history")
        print("  !<n> - Re-run the nth most recent calculation")

        # Add previous result reference help
        print("\nPrevious result reference:")
        print("  $ or ans - Use the result of the previous calculation")
        print("  Example: add $ 5 (adds 5 to the previous result)")

        # Add chain calculation help
        print("\nChained calculations:")
        print("  chain <operation1> <args1> | <operation2> <args2> | ...")
        print("  Example: chain add 5 3 | multiply $ 2")
        print("  The result of each operation becomes available as $ in the next one")

    def parse_command(input_text, allow_chain=True):
        """Parse the user input command and arguments."""
        # Replace $ or ans with the last result if available
        if last_result is not None:
            input_text = input_text.replace('$', str(last_result))

            # Split the input to properly handle 'ans' replacement
            parts = input_text.split()
            for i in range(len(parts)):
                if parts[i].lower() == 'ans':
                    parts[i] = str(last_result)
            input_text = ' '.join(parts)

        # Handle chained calculations
        if allow_chain and input_text.lower().startswith('chain '):
            return "chain", input_text[6:].strip()  # Return the rest of the command after 'chain'

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
            print(f"Unknown operation: {op_name}")
            return None, None

        return op_name, parts[1:]

    def process_args(op_name, arg_parts):
        """Process and validate command arguments."""
        required_args = operations_metadata[op_name]['args']
        if len(arg_parts) < len(required_args):
            print(f"Error: Not enough arguments. {op_name} requires {len(required_args)} arguments: {', '.join(required_args)}")
            return None

        # Parse arguments
        arg_values = []
        for i, arg_name in enumerate(required_args):
            try:
                if arg_name == 'n' and op_name == 'factorial':
                    # Factorial needs integer
                    arg_values.append(int(float(arg_parts[i])))
                else:
                    arg_values.append(float(arg_parts[i]))
            except ValueError:
                print(f"Error: Invalid argument '{arg_parts[i]}' for {arg_name}. Expected a number.")
                return None

        return arg_values

    def handle_history_command(args):
        """Handle history-related commands."""
        if not args:
            # Display all history
            entries = history.get_all_entries()
            if not entries:
                print("History is empty")
                return

            print("\nCalculation History:")
            for i, entry in enumerate(entries):
                print(f"{i+1}: {entry['command']} = {entry['result']}")
        elif args[0] == "clear":
            # Clear history
            history.clear()
            print("History cleared")
        else:
            # Show specific history entry
            try:
                idx = int(args[0]) - 1  # Convert to 0-based index
                entry = history.get_entry(idx)
                if entry:
                    print(f"{args[0]}: {entry['command']} = {entry['result']}")
                else:
                    print(f"Error: History entry {args[0]} not found")
            except ValueError:
                print(f"Error: Invalid history index: {args[0]}")

    def handle_chain_command(chain_text):
        """Handle a chain of calculations."""
        # Split the chain by the pipe symbol
        operations = chain_text.split('|')
        if not operations:
            print("Error: No operations in chain")
            return

        chain_result = None
        full_command = "chain " + chain_text

        # Process each operation in the chain
        for i, operation in enumerate(operations):
            operation = operation.strip()
            if not operation:
                continue

            # Replace $ with the result of the previous operation in the chain
            if chain_result is not None:
                operation = operation.replace('$', str(chain_result))

                # Also handle 'ans' replacement
                op_parts = operation.split()
                for j in range(len(op_parts)):
                    if op_parts[j].lower() == 'ans':
                        op_parts[j] = str(chain_result)
                operation = ' '.join(op_parts)

            # Parse the operation
            op_name, arg_parts = parse_command(operation, allow_chain=False)
            if not op_name:
                print(f"Error in chain segment {i+1}: Invalid operation")
                return

            # Process arguments
            arg_values = process_args(op_name, arg_parts)
            if not arg_values:
                print(f"Error in chain segment {i+1}: Invalid arguments")
                return

            try:
                # Execute the operation
                result = plugin_manager.execute_operation(op_name, *arg_values)
                chain_result = result

                # Show intermediate result
                print(f"Step {i+1}: {operation} = {result}")

            except ValueError as e:
                print(f"Error in chain segment {i+1}: {e}")
                return

        # Store the final result and add to history
        if chain_result is not None:
            print(f"Final result: {chain_result}")
            history.add_entry(full_command, chain_result)
            return chain_result

        return None

    # Show initial help message about features
    print("\nTip: Use '$' or 'ans' to reference the previous result in calculations")
    print("Tip: Use 'chain' to perform multiple calculations in sequence (e.g., chain add 5 3 | multiply $ 2)")

    while True:
        try:
            # Show the previous result in the prompt if available
            prompt = "\nEnter command"
            if last_result is not None:
                prompt += f" (previous: {last_result})"
            prompt += ": "

            user_input = input(prompt).strip()

            if user_input.lower() in ('exit', 'quit'):
                print("Exiting interactive mode...")
                break

            if user_input.lower() == 'help':
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
                if result is not None:
                    last_result = result
                continue

            # Handle regular operations
            arg_values = process_args(op_name, arg_parts)
            if not arg_values:
                continue

            try:
                result = plugin_manager.execute_operation(op_name, *arg_values)
                print(f"Result: {result}")

                # Store as the last result for reference
                last_result = result

                # Add to history
                history.add_entry(user_input, result)

            except ValueError as e:
                print(f"Error: {e}")

        except KeyboardInterrupt:
            print("\nOperation interrupted.")
        except EOFError:
            print("\nExiting interactive mode...")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
