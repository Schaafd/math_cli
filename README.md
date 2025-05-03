# Mathematical Operations CLI Documentation

## Overview

The Mathematical Operations CLI is a command-line tool that provides access to a wide range of mathematical operations. It can be used in both command mode (for single operations) and interactive mode (for multiple sequential operations).

## Installation

Save the script as `math_cli.py` and ensure you have Python 3.x installed.

## Usage

### Command Mode

Run a single mathematical operation:

```bash
python math_cli.py <operation> <arguments>
```

### Interactive Mode

Start the CLI in interactive mode:

```bash
python math_cli.py --interactive
# or
python math_cli.py -i
```

In interactive mode, you can enter operations one after another without restarting the script. Type `help` to see all available commands, and `exit` or `quit` to exit interactive mode.

## Available Operations

| Operation | Arguments | Description | Example |
|-----------|-----------|-------------|---------|
| `add` | a b | Add two numbers | `add 5 3` |
| `subtract` | a b | Subtract b from a | `subtract 7 2` |
| `multiply` | a b | Multiply two numbers | `multiply 4 6` |
| `divide` | a b | Divide a by b | `divide 10 2` |
| `power` | base exponent | Raise base to the power of exponent | `power 2 3` |
| `sqrt` | n | Calculate the square root of n | `sqrt 16` |
| `factorial` | n | Calculate the factorial of n | `factorial 5` |
| `log` | n [base] | Calculate the logarithm of n with the given base (default: natural log) | `log 100 10` |
| `sin` | angle | Calculate the sine of an angle in radians | `sin 1.57` |
| `cos` | angle | Calculate the cosine of an angle in radians | `cos 3.14` |
| `tan` | angle | Calculate the tangent of an angle in radians | `tan 0.78` |
| `to_radians` | degrees | Convert degrees to radians | `to_radians 180` |
| `to_degrees` | radians | Convert radians to degrees | `to_degrees 3.14` |
| `abs` | n | Calculate the absolute value of n | `abs -10` |

## Examples

### Command Mode Examples

1. Add two numbers:
   ```bash
   python math_cli.py add 5 3
   # Result: 8.0
   ```

2. Calculate the square root:
   ```bash
   python math_cli.py sqrt 16
   # Result: 4.0
   ```

3. Calculate factorial:
   ```bash
   python math_cli.py factorial 5
   # Result: 120.0
   ```

4. Calculate sin of an angle:
   ```bash
   python math_cli.py sin 1.57
   # Result: 0.9999996829318346
   ```

### Interactive Mode Examples

```
$ python math_cli.py -i
Mathematical Operations CLI - Interactive Mode
Type 'exit' or 'quit' to exit, 'help' for available commands

Enter command: add 5 3
Result: 8.0

Enter command: power 2 10
Result: 1024.0

Enter command: sqrt 144
Result: 12.0

Enter command: help

Available operations:
  add a b - Add two numbers
  subtract a b - Subtract b from a
  multiply a b - Multiply two numbers
  divide a b - Divide a by b
  power base exponent - Raise base to the power of exponent
  sqrt n - Calculate the square root of n
  factorial n - Calculate the factorial of n
  log n base - Calculate the logarithm of n with the given base
  sin angle - Calculate the sine of an angle in radians
  cos angle - Calculate the cosine of an angle in radians
  tan angle - Calculate the tangent of an angle in radians
  to_radians degrees - Convert degrees to radians
  to_degrees radians - Convert radians to degrees
  abs n - Calculate the absolute value of n

Enter command: exit
Exiting interactive mode...
```

## Error Handling

The CLI handles various error conditions gracefully:

- Division by zero
- Square root of negative numbers
- Factorial of negative numbers or non-integers
- Logarithm of non-positive numbers or invalid bases
- Missing required arguments

When an error occurs, the CLI will display an error message explaining the issue.

## Getting Help

To see all available operations and their descriptions:

```bash
python math_cli.py --help
```

For help on a specific operation:

```bash
python math_cli.py <operation> --help
```

In interactive mode, type `help` to see all available commands.
