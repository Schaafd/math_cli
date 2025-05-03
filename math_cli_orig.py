import math
import argparse
import sys


class MathOperations:
    """A class that provides basic mathematical operations."""

    @staticmethod
    def add(a, b):
        """Add two numbers."""
        return a + b

    @staticmethod
    def subtract(a, b):
        """Subtract b from a."""
        return a - b

    @staticmethod
    def multiply(a, b):
        """Multiply two numbers."""
        return a * b

    @staticmethod
    def divide(a, b):
        """Divide a by b."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    @staticmethod
    def power(base, exponent):
        """Raise base to the power of exponent."""
        return math.pow(base, exponent)

    @staticmethod
    def square_root(n):
        """Calculate the square root of n."""
        if n < 0:
            raise ValueError("Cannot calculate square root of a negative number")
        return math.sqrt(n)

    @staticmethod
    def factorial(n):
        """Calculate the factorial of n."""
        if n < 0:
            raise ValueError("Cannot calculate factorial of a negative number")
        if not isinstance(n, int):
            raise ValueError("Factorial requires an integer")
        return math.factorial(n)

    @staticmethod
    def logarithm(n, base=math.e):
        """Calculate the logarithm of n with the given base."""
        if n <= 0:
            raise ValueError("Cannot calculate logarithm of a non-positive number")
        if base <= 0 or base == 1:
            raise ValueError("Invalid logarithm base")
        return math.log(n, base)

    @staticmethod
    def sin(angle):
        """Calculate the sine of an angle in radians."""
        return math.sin(angle)

    @staticmethod
    def cos(angle):
        """Calculate the cosine of an angle in radians."""
        return math.cos(angle)

    @staticmethod
    def tan(angle):
        """Calculate the tangent of an angle in radians."""
        return math.tan(angle)

    @staticmethod
    def degrees_to_radians(degrees):
        """Convert degrees to radians."""
        return math.radians(degrees)

    @staticmethod
    def radians_to_degrees(radians):
        """Convert radians to degrees."""
        return math.degrees(radians)

    @staticmethod
    def absolute(n):
        """Calculate the absolute value of n."""
        return abs(n)


def main():
    """Command-line interface for the MathOperations class."""
    operations = {
        'add': {'args': ['a', 'b'], 'help': 'Add two numbers'},
        'subtract': {'args': ['a', 'b'], 'help': 'Subtract b from a'},
        'multiply': {'args': ['a', 'b'], 'help': 'Multiply two numbers'},
        'divide': {'args': ['a', 'b'], 'help': 'Divide a by b'},
        'power': {'args': ['base', 'exponent'], 'help': 'Raise base to the power of exponent'},
        'sqrt': {'args': ['n'], 'help': 'Calculate the square root of n'},
        'factorial': {'args': ['n'], 'help': 'Calculate the factorial of n'},
        'log': {'args': ['n', 'base'], 'help': 'Calculate the logarithm of n with the given base'},
        'sin': {'args': ['angle'], 'help': 'Calculate the sine of an angle in radians'},
        'cos': {'args': ['angle'], 'help': 'Calculate the cosine of an angle in radians'},
        'tan': {'args': ['angle'], 'help': 'Calculate the tangent of an angle in radians'},
        'to_radians': {'args': ['degrees'], 'help': 'Convert degrees to radians'},
        'to_degrees': {'args': ['radians'], 'help': 'Convert radians to degrees'},
        'abs': {'args': ['n'], 'help': 'Calculate the absolute value of n'}
    }

    parser = argparse.ArgumentParser(description='Perform basic mathematical operations')
    subparsers = parser.add_subparsers(dest='operation', help='Operation to perform')

    # Add subparsers for each operation
    for op_name, op_info in operations.items():
        op_parser = subparsers.add_parser(op_name, help=op_info['help'])
        for arg in op_info['args']:
            op_parser.add_argument(arg, type=float, help=f'{arg} value')

    # Add interactive mode
    parser.add_argument('--interactive', '-i', action='store_true', help='Run in interactive mode')

    args = parser.parse_args()
    math_ops = MathOperations()

    if args.interactive:
        run_interactive_mode(math_ops, operations)
    elif args.operation:
        try:
            result = execute_operation(math_ops, args)
            print(f"Result: {result}")
        except ValueError as e:
            print(f"Error: {e}")
    else:
        parser.print_help()


def execute_operation(math_ops, args):
    """Execute the specified operation with the given arguments."""
    op = args.operation

    if op == 'add':
        return math_ops.add(args.a, args.b)
    elif op == 'subtract':
        return math_ops.subtract(args.a, args.b)
    elif op == 'multiply':
        return math_ops.multiply(args.a, args.b)
    elif op == 'divide':
        return math_ops.divide(args.a, args.b)
    elif op == 'power':
        return math_ops.power(args.base, args.exponent)
    elif op == 'sqrt':
        return math_ops.square_root(args.n)
    elif op == 'factorial':
        return math_ops.factorial(int(args.n))
    elif op == 'log':
        if hasattr(args, 'base'):
            return math_ops.logarithm(args.n, args.base)
        return math_ops.logarithm(args.n)
    elif op == 'sin':
        return math_ops.sin(args.angle)
    elif op == 'cos':
        return math_ops.cos(args.angle)
    elif op == 'tan':
        return math_ops.tan(args.angle)
    elif op == 'to_radians':
        return math_ops.degrees_to_radians(args.degrees)
    elif op == 'to_degrees':
        return math_ops.radians_to_degrees(args.radians)
    elif op == 'abs':
        return math_ops.absolute(args.n)


def run_interactive_mode(math_ops, operations):
    """Run the CLI in interactive mode."""
    print("Mathematical Operations CLI - Interactive Mode")
    print("Type 'exit' or 'quit' to exit, 'help' for available commands")

    def show_help():
        """Display help information for all operations."""
        print("\nAvailable operations:")
        for op_name, op_info in operations.items():
            args_str = ' '.join(op_info['args'])
            print(f"  {op_name} {args_str} - {op_info['help']}")

    def parse_command(input_text):
        """Parse the user input command and arguments."""
        parts = input_text.split()
        if not parts:
            return None, None

        op_name = parts[0]
        if op_name not in operations:
            print(f"Unknown operation: {op_name}")
            return None, None

        return op_name, parts[1:]

    def process_args(op_name, arg_parts):
        """Process and validate command arguments."""
        required_args = operations[op_name]['args']
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

            # Create a namespace to simulate argparse args
            class Args:
                pass
            args = Args()
            # Set operation as attribute
            setattr(args, 'operation', op_name)
            # Set argument values
            for i, arg_name in enumerate(operations[op_name]['args']):
                setattr(args, arg_name, arg_values[i])

            try:
                result = execute_operation(math_ops, args)
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

if __name__ == "__main__":
    main()
