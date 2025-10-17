# Math CLI

A modular command-line calculator with plugin support for mathematical operations.

## Table of Contents

- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [Available Operations](#available-operations)
- [Core Plugins](#core-plugins)
- [Interactive Mode](#interactive-mode)
  - [History Feature](#history-feature)
  - [Previous Result Reference](#previous-result-reference)
  - [Chained Calculations](#chained-calculations)
- [Plugin System](#plugin-system)
  - [Using Custom Plugins](#using-custom-plugins)
  - [Creating Custom Plugins](#creating-custom-plugins)
  - [Plugin Examples](#plugin-examples)
- [Code Structure Diagrams](#code-structure-diagrams)
- [Command-Line Arguments](#command-line-arguments)
- [Contributing](#contributing)

## Installation

Clone the repository and install the package:

```bash
git clone https://github.com/yourusername/math-cli.git
cd math-cli

# Option 1: Using uv (recommended - faster!)
uv venv
uv pip install -r requirements.txt

# Option 2: Using standard venv
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Or install in editable mode
pip install -e .
```

### Requirements

- Python 3.8 or higher
- rich >= 14.0.0 (for visual enhancements)
- prompt_toolkit >= 3.0.0 (for autocompletion and interactive features)
- uv (optional, but recommended for faster dependency installation)

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

Math CLI includes **142+ mathematical operations** across 8 specialized domains:

**Core Mathematical Operations:**
- `add`, `subtract`, `multiply`, `divide` - Basic arithmetic
- `power`, `sqrt`, `factorial` - Advanced arithmetic
- `sin`, `cos`, `tan` - Trigonometric functions
- `log`, `abs` - Logarithmic (explicit base argument required) and absolute functions

**Extended Operations:** (via core plugins)
- **Statistical Functions:** `mean`, `median`, `std_dev`, `max`, `min` (variadic)
- **Complex Numbers:** `complex_add`, `complex_multiply`, `complex_magnitude`
- **Geometric Calculations:** `area_circle`, `volume_sphere`, `distance`
- **Unit Conversions:** `celsius_to_fahrenheit`, `miles_to_kilometers`
- **Combinatorics:** `combinations`, `fibonacci`, `is_prime`
- **Constants:** `pi`, `e`, `golden_ratio`, `speed_of_light`
- **Advanced Math:** `ceil`, `floor`, `gcd`, `lcm`
- **Extended Trigonometry:** `asin`, `sinh`, `atan2`

## Core Plugins

Math CLI includes 8 comprehensive plugin modules that extend functionality beyond basic arithmetic, providing **110+ additional mathematical operations** across various domains:

- **[Extended Trigonometric Functions](docs/Core_Plugins.md#extended-trigonometric-functions)** - Inverse trig and hyperbolic functions
- **[Statistical Functions](docs/Core_Plugins.md#statistical-functions)** - Mean, median, standard deviation (15 variadic operations)
- **[Complex Number Operations](docs/Core_Plugins.md#complex-number-operations)** - Complete complex arithmetic and conversions
- **[Geometric Functions](docs/Core_Plugins.md#geometric-functions)** - Areas, volumes, distances, and shape calculations  
- **[Unit Conversions](docs/Core_Plugins.md#unit-conversions)** - Temperature, length, weight, speed, energy conversions
- **[Combinatorics & Number Theory](docs/Core_Plugins.md#combinatorics--number-theory)** - Fibonacci, primes, combinations
- **[Mathematical Constants](docs/Core_Plugins.md#mathematical-constants)** - π, e, physical constants
- **[Advanced Mathematical Functions](docs/Core_Plugins.md#advanced-mathematical-functions)** - GCD, LCM, rounding, modulo

### Key Features:
- **Variadic Operations:** 15 functions accept multiple arguments (e.g., `mean 10 20 30 40 50`)
- **Template-Based:** All plugins follow consistent architecture
- **Error Handling:** Comprehensive input validation and clear error messages
- **Chain Compatible:** Works seamlessly with chain operations

### Quick Examples:
```bash
# Statistical analysis
python math_cli.py mean 85 92 78 96 88 91 87 94 89 93
python math_cli.py std_dev 10 12 14 16 18

# Complex numbers  
python math_cli.py complex_add 3 4 2 -1

# Unit conversions
python math_cli.py celsius_to_fahrenheit 25

# Geometric calculations
python math_cli.py area_circle 5
```

**📖 For complete documentation of all core plugins, see: [Core Plugins Guide](docs/Core_Plugins.md)**

## Interactive Mode

Run Math CLI in interactive mode to perform multiple calculations in succession with beautiful visual enhancements:

```bash
python math_cli.py --interactive
# or
python math_cli.py -i
```

### Visual Enhancements (Phase 1)

Math CLI features a **delightful interactive experience** with:

- 🎨 **Colorful Output** - Syntax-highlighted commands and color-coded results
- ✨ **Animated Banner** - Welcoming startup animation
- ✓ **Success Indicators** - Visual feedback for completed calculations
- 📊 **Rich History Display** - Beautifully formatted calculation history tables
- 💡 **Helpful Tips** - Contextual guidance as you work
- 🎯 **Smart Error Messages** - Clear, friendly error messages with suggestions
- ⚡ **Chain Visualization** - Step-by-step display for chained calculations

### Interactive Features (Phase 2)

Enhanced interactivity with intelligent assistance:

- ⌨️ **Smart Autocompletion** - Press Tab to autocomplete operation names with parameter hints
- 🔍 **Advanced Help System** - Use `help <operation>` for detailed documentation
- 🎯 **Fuzzy Error Matching** - Get intelligent suggestions for typos (e.g., "squrt" → "sqrt")
- 📚 **Searchable Operations** - Use `help search:trig` to find trigonometric functions
- 📂 **Category Browsing** - Use `help category:statistics` to see all statistical operations
- ⌨️ **Keyboard Shortcuts** - Ctrl+L to clear, Ctrl+D to exit, ↑↓ for history
- 📊 **Bottom Toolbar** - See previous results and available shortcuts at a glance

### Session Management & Personalization (Phase 3 - NEW!)

Professional data management and customization:

- 🎨 **8 Beautiful Themes** - Choose from default, dark, light, ocean, forest, sunset, and more
- ⚙️ **Configuration System** - Customize every aspect of Math CLI behavior
- 💾 **Persistent History** - Automatic save/load of calculation history across sessions
- 📤 **Export Functionality** - Export history to JSON, CSV, or Markdown formats
- 🔖 **Bookmark System** - Save important results with custom names for quick retrieval
- 🎯 **Cross-Platform** - Config stored in proper system directories (XDG/APPDATA)

**Phase 3 Commands:**
```bash
# Configuration
config                        # Show all settings
config set theme ocean        # Change theme
config get history_limit      # Get specific setting

# Themes
theme                         # List available themes
theme set dark                # Switch to dark theme
theme preview ocean           # Preview a theme

# Export
export json ~/calc.json       # Export to JSON
export csv ~/data.csv         # Export to CSV
export markdown ~/report.md   # Export to Markdown

# Bookmarks
bookmark                      # List all bookmarks
bookmark save 1 pi_value      # Bookmark history entry
bookmark get pi_value         # Retrieve bookmark
```

### Accessibility Options

For users who prefer minimal visuals or have accessibility needs:

```bash
# Disable colored output
python math_cli.py --interactive --no-color

# Disable animations
python math_cli.py --interactive --no-animations

# Disable both
python math_cli.py --interactive --no-color --no-animations
```

### Features in Interactive Mode

- Type an operation followed by its arguments (e.g., `add 5 3`)
- Type `help` to see a beautifully formatted list of available commands
- Type `exit` or `quit` to exit
- Enjoy real-time visual feedback with every calculation

Example interactive session:
```
╔═══════════════════════════════════════════════════════════╗
║     __  __       _   _        ____ _     ___              ║
║    |  \/  | __ _| |_| |__    / ___| |   |_ _|             ║
║    | |\/| |/ _` | __| '_ \  | |   | |    | |              ║
║    | |  | | (_| | |_| | | | | |___| |___ | |              ║
║    |_|  |_|\__,_|\__|_| |_|  \____|_____|___|             ║
║         Interactive Mathematical Operations               ║
╚═══════════════════════════════════════════════════════════╝

💡 Tip: Use '$' or 'ans' to reference the previous result

❯ sqrt 16
Result: 4 ✓

❯ (prev: 4) power 2 10
Result: 1,024 ✓

❯ (prev: 1024) exit
✓ Goodbye! Thanks for using Math CLI
```

### History Feature

In interactive mode, you can access your calculation history:

- `history` - Show all past calculations in the current session
- `history <n>` - Show the nth most recent calculation
- `history clear` - Clear all history
- `!<n>` - Re-run the nth calculation from history

Example:
```
Enter command: add 5 10
Result: 15.0

Enter command: multiply 3 7
Result: 21.0

Enter command: history
Calculation History:
1: multiply 3 7 = 21.0
2: add 5 10 = 15.0

Enter command: !2
Re-running: add 5 10
Result: 15.0
```
### Previous Result Reference

In interactive mode, you can use the result of the previous calculation in your next operation:

- Use `$` or `ans` to reference the previous result
- The previous result is also shown in the command prompt

Example:
```
Enter command: multiply 8 5
Result: 40.0

Enter command (previous: 40.0): add $ 10
Result: 50.0

Enter command (previous: 50.0): divide ans 2
Result: 25.0

Enter command (previous: 25.0): power 2 $
Result: 33554432.0
```

This feature makes it easy to chain calculations without having to re-type previous results.

### Chained Calculations

In interactive mode, you can chain multiple calculations in a single command:

- Use the `chain` command followed by operations separated by the pipe symbol `|`
- Each operation's result becomes available as `$` or `ans` in the next operation
- Each step's result is displayed, along with the final result

Example:

```
Enter command: chain add 10 5 | multiply $ 2 | sqrt $
Step 1: add 10 5 = 15.0
Step 2: multiply 15.0 2 = 30.0
Step 3: sqrt 30.0 = 5.477225575051661
Final result: 5.477225575051661

Enter command (previous: 5.477225575051661): power $ 2
Result: 30.000000000000004
```

Benefits of chained calculations:
- Perform complex multi-step calculations in a single command
- See intermediate results at each step
- Avoid having to manually use the previous result for sequential operations
- All chain results are stored in history as a single entry

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
usage: math_cli.py [-h] [--interactive] [--plugin-dir PLUGIN_DIR]
                   [--list-plugins] [--no-color] [--no-animations] ...

Perform mathematical operations

positional arguments:
  operation             Operation to perform

options:
  -h, --help            Show this help message and exit
  --interactive, -i     Run in interactive mode with visual enhancements
  --plugin-dir PLUGIN_DIR
                        Directory containing additional plugins
  --list-plugins        List available operation plugins
  --no-color            Disable colored output (accessibility)
  --no-animations       Disable animations (accessibility)
```

### Accessibility Flags

The `--no-color` and `--no-animations` flags ensure Math CLI is accessible to all users:

- **`--no-color`**: Removes all color formatting, useful for screen readers and terminals without color support
- **`--no-animations`**: Disables animated elements like the startup banner and loading spinners
- Both flags can be combined for maximum compatibility

## Code Structure Diagrams

To better understand the structure and flow of the Math CLI application, refer to these diagrams:

- [Class Diagram (UML)](docs/class-diagram.md) - Shows the main classes and their relationships
- [Package Structure](docs/package-structure.md) - Shows how the code is organized into packages and modules
- [Plugin System Flowchart](docs/plugin-system.md) - Explains how the plugin system works
- [Command Execution Sequence](docs/command-execution.md) - Details how commands are processed
- [Interactive Mode State Diagram](docs/interactive-mode.md) - Shows the state transitions in interactive mode
- [User Interaction Diagram](docs/user-interaction.md) - Shows how users interact with the application
- [Plugin Loading Process](docs/plugin-loading.md) - Details how plugins are discovered and loaded

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
