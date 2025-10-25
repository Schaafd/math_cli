# Math CLI

A modular command-line calculator with plugin support for mathematical operations.

## Table of Contents

- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [Available Operations](#available-operations)
- [Core Plugins](#core-plugins)
- [Advanced Mathematical Operations](#advanced-mathematical-operations-phase-51)
  - [Complex Numbers](#complex-numbers-18-operations)
  - [Matrix Operations](#matrix-operations-12-operations)
  - [Calculus](#calculus-12-operations)
  - [Number Theory](#number-theory-15-operations)
- [Data Analysis & Visualization](#data-analysis--visualization-phase-52---new)
  - [Data Import/Export](#data-importexport)
  - [Statistical Analysis](#statistical-analysis-12-operations)
  - [Data Transformation](#data-transformation-11-operations)
  - [CLI Plotting Operations](#cli-plotting-operations-phase-525---new)
- [Programmability & Scripting](#programmability--scripting-phase-53---new)
  - [Variables](#variables-6-operations)
  - [Control Flow](#control-flow-13-operations)
  - [User-Defined Functions](#user-defined-functions-3-operations)
  - [Script Files](#script-files-2-operations)
- [Interactive Mode](#interactive-mode)
  - [Visual Enhancements](#visual-enhancements-phase-1)
  - [Interactive Features](#interactive-features-phase-2)
  - [Session Management & Personalization](#session-management--personalization-phase-3---new)
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

**Core Dependencies:**
- Python 3.8 or higher
- rich >= 14.0.0 (for visual enhancements)
- prompt_toolkit >= 3.0.0 (for autocompletion and interactive features)
- psutil >= 5.9.0 (for performance monitoring)

**Advanced Mathematical Operations (Phase 5.1):**
- numpy >= 1.24.0 (matrix operations, numerical computing)
- scipy >= 1.10.0 (statistical functions, integration)
- sympy >= 1.12 (symbolic mathematics, calculus)

**Data Analysis & Visualization (Phase 5.2):**
- pandas >= 2.0.0 (data manipulation and analysis)
- matplotlib >= 3.7.0 (plotting backend reference)
- seaborn >= 0.12.0 (statistical visualization patterns)

**Development Tools:**
- pytest >= 7.0.0 (testing)
- pytest-cov >= 4.0.0 (code coverage)
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

Math CLI includes **260+ mathematical operations** organized into 16 logical categories:

The operations are organized into these categories (use `--list-plugins` to see all):

1. **Basic Arithmetic** (14 ops) - add, subtract, multiply, divide, power, sqrt, abs
2. **Trigonometry** (18 ops) - sin, cos, tan, asin, acos, atan, sinh, cosh, tanh, atan2
3. **Algebra** (12 ops) - log, exp, floor, ceil, round, mod
4. **Calculus** (12 ops) - derivative, integrate, limit, taylor, gradient, laplacian
5. **Statistics** (23 ops) - mean, median, stdev, correlation, linear_regression, zscore
6. **Matrix Operations** (12 ops) - determinant, inverse, eigenvalues, transpose, rank
7. **Complex Numbers** (18 ops) - cadd, cmul, magnitude, phase, conjugate, csqrt
8. **Number Theory** (15 ops) - is_prime, gcd, lcm, factorial, fibonacci, euler_phi
9. **Geometry** (9 ops) - area_circle, volume_sphere, distance, perimeter
10. **Data Analysis** (12 ops) - load_data, describe_data, correlation_matrix, groupby
11. **Data Transformation** (11 ops) - filter_data, normalize_data, sort_data, aggregate_data
12. **Visualization** (8 ops) - plot_hist, plot_box, plot_scatter, plot_heatmap, plot, plot_line, plot_bar, plot_data
13. **Scripting** (24 ops) - Variables (6), Control Flow (13), Functions (3), Scripts (2)
14. **Unit Conversions** (38 ops) - celsius_to_fahrenheit, miles_to_kilometers, etc.
15. **Constants** (7 ops) - pi, e, golden_ratio, speed_of_light, avogadro
16. **Other Operations** (23 ops) - Various utility functions

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

## Advanced Mathematical Operations (Phase 5.1)

Math CLI now includes advanced mathematical capabilities for professional scientific computing:

### Complex Numbers (18 operations)
Comprehensive support for complex number arithmetic and analysis:

```bash
# Basic complex operations
python math_cli.py cadd 3 4 1 2              # (3+4i) + (1+2i) = 4+6i
python math_cli.py cmul 3 4 1 2              # (3+4i) * (1+2i) = -5+10i
python math_cli.py magnitude 3 4              # |3+4i| = 5.0
python math_cli.py phase 1 1                  # arg(1+i) = 0.785 rad

# Advanced complex functions
python math_cli.py csqrt -1 0                 # √(-1) = i
python math_cli.py cexp 0 3.14159             # e^(iπ) ≈ -1
```

### Matrix Operations (12 operations)
Linear algebra operations using NumPy:

```bash
# Create and analyze matrices
python math_cli.py det 2 1 2 3 4              # det([[1,2],[3,4]]) = -2
python math_cli.py transpose 2 3 1 2 3 4 5 6  # Transpose 2x3 matrix
python math_cli.py eigenvalues 2 4 1 2 3      # Find eigenvalues
python math_cli.py trace 3 1 0 0 0 2 0 0 0 3  # Trace = 6
```

### Calculus (12 operations)
Symbolic and numerical calculus with SymPy:

```bash
# Derivatives
python math_cli.py derivative 'x**2' x        # d/dx(x²) = 2*x
python math_cli.py derivative2 'x**3' x       # d²/dx²(x³) = 6*x
python math_cli.py gradient 'x**2+y**2' x y   # ∇(x²+y²) = [2*x, 2*y]

# Integration
python math_cli.py integrate 'x**2' 0 1       # ∫₀¹ x² dx = 0.333
python math_cli.py integrate_symbolic 'x' x   # ∫ x dx = x²/2

# Limits and series
python math_cli.py limit 'sin(x)/x' x 0       # lim(x→0) sin(x)/x = 1
python math_cli.py taylor 'exp(x)' x 0 5      # Taylor series of eˣ
```

### Number Theory (15 operations)
Prime numbers, combinatorics, and modular arithmetic:

```bash
# Prime operations
python math_cli.py is_prime 17                # True
python math_cli.py prime_factors 84           # {2: 2, 3: 1, 7: 1}
python math_cli.py next_prime 100             # 101
python math_cli.py prime_count 100            # 25 primes ≤ 100

# Combinatorics
python math_cli.py factorial 5                # 5! = 120
python math_cli.py fibonacci 10               # F₁₀ = 55
python math_cli.py combinations 5 3           # C(5,3) = 10
python math_cli.py euler_phi 12               # φ(12) = 4
```

## Data Analysis & Visualization (Phase 5.2 - NEW!)

Transform Math CLI into a powerful data analysis tool with support for loading, analyzing, and visualizing datasets:

### Data Import/Export

Load and save datasets from CSV and JSON files:

```bash
# In interactive mode
❯ load_data 'sales_data.csv' csv mydata
Loaded 1000 rows × 5 columns

❯ data_info mydata
{
  'rows': 1000,
  'columns': 5,
  'column_names': ['date', 'product', 'quantity', 'price', 'region'],
  'memory_usage': 40000
}

❯ save_data mydata 'output.json' json
Saved to output.json
```

### Statistical Analysis (12 operations)

Perform comprehensive statistical analysis on datasets:

```bash
# Descriptive statistics
❯ describe_data mydata
       quantity      price
count   1000.00    1000.00
mean      50.23      99.87
std       15.42      25.13
min       10.00      50.00
max       95.00     150.00

# Correlation analysis
❯ correlation_matrix mydata pearson
           quantity  price
quantity      1.000  0.752
price         0.752  1.000

# Group by operations
❯ groupby mydata region mean
        quantity  price
North      48.2   95.3
South      52.1  102.4
East       49.8   98.7
West       51.3  103.2

# Outlier detection
❯ detect_outliers mydata price 1.5
{
  'n_outliers': 12,
  'outlier_percentage': 1.2,
  'lower_bound': 45.5,
  'upper_bound': 155.2
}

# Missing values analysis
❯ missing_values mydata
         missing_count  missing_percent
price              15             1.5
quantity            3             0.3

# Pivot tables
❯ pivot_table mydata price region product mean
              Product_A  Product_B  Product_C
North            95.2      98.5      102.1
South           100.3      99.8       97.5
```

### Data Transformation (11 operations)

Clean, filter, and transform your data:

```bash
# Filter data
❯ filter_data mydata price > 100 expensive
Filtered to 423 rows (from 1000 rows)

# Sort data
❯ sort_data mydata price false sorted_desc
Sorted 1000 rows by 'price' (descending)

# Normalize data
❯ normalize_data mydata minmax normalized
Normalized 2 columns using minmax

# Handle missing values
❯ fill_nulls mydata mean filled
Filled 18 null values with mean

❯ drop_nulls mydata cleaned
Dropped 18 rows with null values (982 rows remain)

# Sample data
❯ sample_data mydata 100 sample
Sampled 100 rows from 1000 total rows

# Add columns
❯ add_column mydata status active updated
Added column 'status' with value 'active'

# Aggregate data
❯ aggregate_data mydata mean
quantity    50.23
price       99.87
```

### CLI Plotting Operations (Phase 5.2.5 - NEW!)

Create beautiful ASCII visualizations directly from the command line using loaded datasets:

#### Statistical Plots (4 operations)

```bash
# Load your dataset first
❯ load_data sales.csv csv sales
Loaded 10 rows × 4 columns

# 1. HISTOGRAM - Distribution analysis
❯ plot_hist sales price 5
Histogram (5 bins)
────────────────────────────────────────────────────────────
   15.50-   30.40 │██████████████████████████ 2
   30.40-   45.30 │█████████████ 1
   45.30-   60.20 │██████████████████████████ 2
   60.20-   75.10 │█████████████ 1
   75.10-   90.00 │████████████████████████████████████████ 4
────────────────────────────────────────────────────────────
Min: 15.50, Max: 89.99, Mean: 43.92, Std: 23.84

# 2. BOX PLOT - Shows quartiles and outliers
❯ plot_box sales revenue Revenue
Box Plot: Revenue
────────────────────────────────────────────────────────────
          ├─────├─────│───────┤───────────────────
────────────────────────────────────────────────────────────
Min: 1038.50  Q1: 1507.75  Median: 1727.00  Q3: 1965.89  Max: 2175.00
IQR: 458.14  Outliers: 0

# 3. SCATTER PLOT with Linear Regression
❯ plot_scatter sales quantity revenue
Scatter Plot with Linear Regression
y = -13.058x + 2288.939  (R² = 0.336)
────────────────────────────────────────────────────────────
        ●
                 ●
  ●
           ●
                        ●
                              ●
                                    ●
                                             ●
────────────────────────────────────────────────────────────
X: [23.00, 78.00]  Y: [1038.50, 2175.00]

# 4. CORRELATION HEATMAP - See relationships between all numeric columns
❯ plot_heatmap sales
Correlation Heatmap
────────────────────────────────────────────────────────────
quantity  │ @   .
price     │   @ %
revenue   │ . % @
────────────────────────────────────────────────────────────
Scale: -1.0 [  ] 0.0 [:-] +1.0 [@#]
```

**Available Plotting Operations:**
- `plot_hist <dataset> <column> <bins>` - Histogram with customizable bins
- `plot_box <dataset> <column> <label>` - Box plot showing quartiles and outliers
- `plot_scatter <dataset> <x_col> <y_col>` - Scatter plot with regression line and R²
- `plot_heatmap <dataset>` - Correlation matrix heatmap for all numeric columns

#### Python API (Advanced Users)

For more control, you can also use the plotting utilities directly in Python:

```python
from utils.advanced_plotting import plot_histogram, plot_boxplot, plot_scatter_regression, plot_heatmap
import numpy as np
import pandas as pd

# Create custom plots with full control
data = np.random.randn(1000)
print(plot_histogram(data, bins=20, width=80, height=25))

# Use with pandas DataFrames
df = pd.DataFrame({'A': [1,2,3], 'B': [2,4,6]})
print(plot_heatmap(df.corr()))
```

### Complete Data Analysis Workflow Example

Here's a real-world example analyzing sales data:

```bash
# Start interactive mode
python math_cli.py --interactive

# Load data
❯ load_data 'monthly_sales.csv' csv sales
Loaded 365 rows × 4 columns

# Inspect the data
❯ data_info sales
rows: 365, columns: 4
columns: ['date', 'product', 'revenue', 'units_sold']

# Get statistical summary
❯ describe_data sales

# Check for missing values
❯ missing_values sales
No missing values found

# Filter to high-revenue transactions
❯ filter_data sales revenue > 1000 high_value
Filtered to 89 rows

# Analyze by product
❯ groupby sales product sum
              revenue  units_sold
Product_A    125000      5234
Product_B     98500      4102
Product_C    145000      6789

# Calculate correlation
❯ correlation_matrix sales

# Detect outliers in revenue
❯ detect_outliers sales revenue 1.5
Found 8 outliers (2.2% of data)

# Visualize the data (Phase 5.2.5 - NEW!)
❯ plot_hist sales revenue 10
[Displays revenue distribution histogram]

❯ plot_box sales units_sold
[Shows units_sold quartiles and outliers]

❯ plot_scatter sales revenue units_sold
[Scatter plot showing revenue vs units correlation]

❯ plot_heatmap sales
[Correlation matrix of all numeric columns]

# Export results
❯ save_data high_value 'high_value_sales.csv' csv
Saved to high_value_sales.csv
```

## Programmability & Scripting (Phase 5.3 - NEW!)

Math CLI now supports variables, control flow, user-defined functions, and script files, transforming it into a programmable calculator!

### Variables (6 operations)

Store and reuse values across calculations:

```bash
# Set variables
❯ set x 10
$x = 10

❯ set y 20
$y = 20

# Use variables in calculations
❯ add $x $y
30

❯ multiply $x $y
200

# List all variables
❯ vars
Variables:
--------------------------------------------------
  $x               = 10
  $y               = 20

# Persistent variables (saved across sessions)
❯ persist pi 3.14159
$pi = 3.14159 (persistent)

# Delete variables
❯ unset x
Deleted variable $x

# Clear all variables
❯ clear_vars
Cleared all session variables
```

**Available Variable Operations:**
- `set <name> <value>` - Set variable value
- `persist <name> <value>` - Set persistent variable (saved to ~/.mathcli/variables.json)
- `get <name>` - Get variable value
- `vars` - List all variables
- `unset <name>` - Delete variable
- `clear_vars [true|false]` - Clear variables (optionally including persistent)

### Control Flow (13 operations)

Make decisions and create conditional logic:

#### Comparisons (6 operations)

```bash
# Comparison operations
❯ eq 5 5           # Equal
true

❯ neq 5 10         # Not equal
true

❯ gt 10 5          # Greater than
true

❯ gte 10 10        # Greater or equal
true

❯ lt 5 10          # Less than
true

❯ lte 5 5          # Less or equal
true
```

#### Logical Operations (3 operations)

```bash
# Logical operations
❯ and true false
false

❯ or true false
true

❯ not true
false
```

#### Conditionals (1 operation)

```bash
# If/then/else
❯ set x 15
❯ if (gt $x 10) "big" "small"
big

# With variables
❯ set threshold 100
❯ set value 150
❯ if (gt $value $threshold) "Above threshold" "Below threshold"
Above threshold
```

#### Type Checking (3 operations)

```bash
❯ is_number 42
true

❯ is_string "hello"
true

❯ is_bool true
true
```

### User-Defined Functions (3 operations)

Create custom reusable functions:

```bash
# Define a function
❯ def square x = multiply $x $x
✓ Defined function: square($x) = multiply $x $x

# Call the function
❯ square 7
49

# Define function with multiple parameters
❯ def hypotenuse a b = sqrt (add (multiply $a $a) (multiply $b $b))
❯ hypotenuse 3 4
5.0

# List all functions
❯ funcs
User-defined functions:
----------------------------------------------------------------------
  hypotenuse($a, $b)
    = sqrt (add (multiply $a $a) (multiply $b $b))
  square($x)
    = multiply $x $x

# Delete a function
❯ undef square
✓ Deleted function: square
```

**Available Function Operations:**
- `def <name> <params...> = <body>` - Define function
- `funcs` - List all user-defined functions
- `undef <name>` - Delete function

### Script Files (2 operations)

Execute sequences of commands from .mathcli files:

#### Example Script File (compound_interest.mathcli)

```mathcli
# Compound Interest Calculator
# Save this as compound_interest.mathcli

# Initial values
set principal 1000
set rate 1.05
set years 5

# Year 1
set amount = multiply $principal $rate
set principal $amount

# Year 2
set amount = multiply $principal $rate
set principal $amount

# Display result
set final $principal
```

#### Running Scripts

```bash
# Execute a script file
❯ run compound_interest.mathcli
✓ Script completed: 8 commands executed

# Run with verbose output (shows each line)
❯ run compound_interest.mathcli true
[1] # Compound Interest Calculator
[3] set principal 1000
  → $principal = 1000
[4] set rate 1.05
  → $rate = 1.05
...
✓ Script completed: 8 commands executed

# Execute inline script
❯ eval 'set x 10; add $x 5'
15
```

### Complete Scripting Example

Here's a comprehensive example combining all Phase 5.3 features:

**File: math_toolkit.mathcli**
```mathcli
# Math Toolkit Script
# Demonstrates variables, functions, and control flow

# Define utility functions
def square x = multiply $x $x
def double x = multiply $x 2
def is_even n = eq (mod $n 2) 0

# Set test values
set a 5
set b 10
set c 15

# Perform calculations
square $a
double $b

# Conditional logic
gt $c $b
if (gt $c $b) "c is bigger" "b is bigger"

# Use functions with variables
set result = square $a
multiply $result 2
```

**Running the script:**
```bash
❯ run math_toolkit.mathcli
✓ Script completed: 12 commands executed
```

### Real-World Use Cases

**1. Financial Calculations**
```mathcli
# mortgage_calculator.mathcli
set loan_amount 200000
set annual_rate 0.05
set monthly_rate = divide $annual_rate 12
set months 360

# Calculate monthly payment (simplified)
set payment = multiply $loan_amount $monthly_rate
```

**2. Data Processing Pipeline**
```mathcli
# data_pipeline.mathcli
load_data raw_data.csv csv data
describe_data data
filter_data data revenue > 1000 filtered
save_data filtered processed_data.csv csv
plot_hist filtered revenue 20
```

**3. Scientific Calculations**
```mathcli
# physics_calc.mathcli
def kinetic_energy mass velocity = multiply (multiply 0.5 $mass) (multiply $velocity $velocity)

set mass 10
set velocity 5
kinetic_energy $mass $velocity
```

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
