# Math CLI

A modular command-line calculator with plugin support for mathematical operations.

## Table of Contents

- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [Available Operations](#available-operations)
- [Interactive Mode](#interactive-mode)
- [Plugin System](#plugin-system)
  - [Using Custom Plugins](#using-custom-plugins)
  - [Creating Custom Plugins](#creating-custom-plugins)
  - [Plugin Examples](#plugin-examples)
- [Command-Line Arguments](#command-line-arguments)
- [Contributing](#contributing)

## Installation

Clone the repository and install the package:

```bash
git clone https://github.com/yourusername/math-cli.git
cd math-cli
pip install -e .
```

## Basic Usage

Math CLI provides a simple interface for performing mathematical operations:

```bash
# Basic arithmetic
python math_cli.py add 5 3
python math_cli.py subtract 10 4
python math_cli.py multiply 6 7
python math_cli.py divide 20 5

# Other operations
python math_cli.py sqrt 16
python math_cli.py power 2 8
python math_cli.py factorial 5
python math_cli.py abs -42
```

Each operation follows the pattern: `python math_cli.py <operation> <arguments>`

## Available Operations

To list all available operations:

```bash
python math_cli.py --list-plugins
```

Built-in operations include:

- `add` - Add two numbers
- `subtract` - Subtract the second number from the first
- `multiply` - Multiply two numbers
- `divide` - Divide the first number by the second
- `power` - Raise a base to an exponent
- `sqrt` - Calculate the square root
- `factorial` - Calculate the factorial
- `log` - Calculate logarithm with optional base
- `sin` - Calculate sine (in radians)
- `cos` - Calculate cosine (in radians)
- `tan` - Calculate tangent (in radians)
- `to_radians` - Convert degrees to radians
- `to_degrees` - Convert radians to degrees
- `abs` - Calculate absolute value

## Interactive Mode

Run Math CLI in interactive mode to perform multiple calculations in succession:

```bash
python math_cli.py --interactive
# or
python math_cli.py -i
```

In interactive mode:
- Type an operation followed by its arguments (e.g., `add 5 3`)
- Type `help` to see available commands
- Type `exit` or `quit` to exit

Example interactive session:
```
Mathematical Operations CLI - Interactive Mode
Type 'exit' or 'quit' to exit, 'help' for available commands

Enter command: sqrt 16
Result: 4.0

Enter command: power 2 10
Result: 1024.0

Enter command: exit
Exiting interactive mode...
```

## Plugin System

Math CLI features a flexible plugin system that allows you to extend its functionality without modifying the core codebase.

### Using Custom Plugins

To use custom plugins, specify the directory containing your plugin files:

```bash
python math_cli.py --plugin-dir /path/to/plugins add 5 3
```

You can specify multiple plugin directories:

```bash
python math_cli.py --plugin-dir /path/to/plugins1 --plugin-dir /path/to/plugins2 -i
```

### Creating Custom Plugins

Creating a custom plugin is straightforward:

1. Create a new Python file (e.g., `my_plugin.py`)
2. Import the base operation class: `from core.base_operations import MathOperation`
3. Define one or more classes that inherit from `MathOperation`
4. Implement the required attributes and methods:
   - `name`: Command name (string)
   - `args`: List of argument names (list of strings)
   - `help`: Help text description (string)
   - `execute()`: Static method implementing the operation logic

### Plugin Examples

**Example 1: Basic Custom Plugin**

```python
# my_plugin.py
from core.base_operations import MathOperation
import math

class HypotenuseOperation(MathOperation):
    name = "hypotenuse"
    args = ["a", "b"]
    help = "Calculate the hypotenuse of a right triangle"

    @classmethod
    def execute(cls, a, b):
        return math.sqrt(a**2 + b**2)
```

Usage:
```bash
python math_cli.py --plugin-dir /path/to/directory/containing/my_plugin.py hypotenuse 3 4
Result: 5.0
```

**Example 2: Multiple Operations in One Plugin**

```python
# advanced_plugin.py
from core.base_operations import MathOperation
import math

class CircleAreaOperation(MathOperation):
    name = "circle_area"
    args = ["radius"]
    help = "Calculate the area of a circle"

    @classmethod
    def execute(cls, radius):
        if radius < 0:
            raise ValueError("Radius cannot be negative")
        return math.pi * radius**2

class CylinderVolumeOperation(MathOperation):
    name = "cylinder_volume"
    args = ["radius", "height"]
    help = "Calculate the volume of a cylinder"

    @classmethod
    def execute(cls, radius, height):
        if radius < 0 or height < 0:
            raise ValueError("Dimensions cannot be negative")
        return math.pi * radius**2 * height
```

## Command-Line Arguments

```
usage: math_cli.py [-h] [--interactive] [--plugin-dir PLUGIN_DIR] [--list-plugins] ...

Perform mathematical operations

positional arguments:
  operation             Operation to perform

options:
  -h, --help            show this help message and exit
  --interactive, -i     Run in interactive mode
  --plugin-dir PLUGIN_DIR
                        Directory containing additional plugins
  --list-plugins        List available operation plugins
```

## Contributing

Contributions to Math CLI are welcome! Here are some ways to contribute:

1. Report bugs and suggest features by creating issues
2. Submit pull requests with bug fixes or new features
3. Create new plugins and share them with the community
4. Improve documentation and tests

When contributing code, please ensure:
- Code follows the project's style guidelines
- New features include appropriate tests
- Documentation is updated to reflect changes

---

For more information, bug reports, or to contribute, please visit:
[https://github.com/yourusername/math-cli](https://github.com/yourusername/math-cli)
