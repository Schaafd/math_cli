from typing import Dict, Any

def run_interactive_mode(plugin_manager, operations_metadata: Dict) -> None:
    """Run the CLI in interactive mode."""
    print("Mathematical Operations CLI - Interactive Mode")
    print("Type 'exit' or 'quit' to exit, 'help' for available commands")

    def show_help():
        """Display help information for all operations."""
        print("\nAvailable operations:")
        for op_name, op_info in operations_metadata.items():
            args_str = ' '.join(op_info['args'])
            print(f"  {op_name} {args_str} - {op_info['help']}")

    def parse_command(input_text):
        """Parse the user input command and arguments."""
        parts = input_text.split()
        if not parts:
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
                    arg_values.append(int(arg_parts[i]))
                else:
                    arg_values.append(float(arg_parts[i]))
            except ValueError:
                print(f"Error: Invalid argument '{arg_parts[i]}' for {arg_name}. Expected a number.")
                return None

        return arg_values

    while True:
        try:
            user_input = input("\nEnter command: ").strip()

            if user_input.lower() in ('exit', 'quit'):
                print("Exiting interactive mode...")
                break

            if user_input.lower() == 'help':
                show_help()
                continue

            op_name, arg_parts = parse_command(user_input)
            if not op_name:
                continue

            arg_values = process_args(op_name, arg_parts)
            if not arg_values:
                continue

            try:
                result = plugin_manager.execute_operation(op_name, *arg_values)
                print(f"Result: {result}")
            except ValueError as e:
                print(f"Error: {e}")

        except KeyboardInterrupt:
            print("\nOperation interrupted.")
        except EOFError:
            print("\nExiting interactive mode...")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
