# Core Plugins Documentation

This document provides a comprehensive guide to the core plugins included with Math CLI that extend beyond the basic mathematical operations. These plugins demonstrate the power and flexibility of the Math CLI plugin system while providing practical mathematical functionality across various domains.

## Table of Contents

- [Overview](#overview)
- [Plugin Categories](#plugin-categories)
  - [Extended Trigonometric Functions](#extended-trigonometric-functions)
  - [Advanced Mathematical Functions](#advanced-mathematical-functions)
  - [Statistical Functions](#statistical-functions)
  - [Combinatorics & Number Theory](#combinatorics--number-theory)
  - [Geometric Functions](#geometric-functions)
  - [Complex Number Operations](#complex-number-operations)
  - [Mathematical Constants](#mathematical-constants)
  - [Unit Conversions](#unit-conversions)
- [Usage Examples](#usage-examples)
- [Plugin Architecture](#plugin-architecture)
- [Creating Your Own Plugins](#creating-your-own-plugins)

## Overview

Math CLI includes 8 core plugin categories that provide over 110 additional mathematical operations beyond the basic arithmetic functions. These plugins are automatically loaded and demonstrate various mathematical domains and computational techniques.

**Total Operations Available:** 142+ mathematical operations  
**Variadic Operations:** 15 operations supporting multiple arguments  
**Plugin Files:** 8 specialized plugin modules  

All plugins follow the same template-based architecture, making them easy to understand, modify, and use as examples for creating your own plugins.

## Plugin Categories

### Extended Trigonometric Functions
**File:** `plugins/extended_trig.py`  
**Operations:** 10 functions

Provides inverse trigonometric and hyperbolic functions that extend the basic trigonometric operations.

#### Inverse Trigonometric Functions
- `asin <x>` - Calculate arcsine (inverse sine), returns result in radians
- `acos <x>` - Calculate arccosine (inverse cosine), returns result in radians  
- `atan <x>` - Calculate arctangent (inverse tangent), returns result in radians
- `atan2 <y> <x>` - Calculate arctangent of y/x, determining correct quadrant

#### Hyperbolic Functions
- `sinh <x>` - Calculate hyperbolic sine
- `cosh <x>` - Calculate hyperbolic cosine
- `tanh <x>` - Calculate hyperbolic tangent

#### Inverse Hyperbolic Functions
- `asinh <x>` - Calculate inverse hyperbolic sine
- `acosh <x>` - Calculate inverse hyperbolic cosine (x ≥ 1)
- `atanh <x>` - Calculate inverse hyperbolic tangent (-1 < x < 1)

**Example Usage:**
```bash
python math_cli.py asin 0.5          # Result: 0.5236 (30 degrees in radians)
python math_cli.py sinh 1            # Result: 1.1752
python math_cli.py atan2 1 1         # Result: 0.7854 (45 degrees in radians)
```

### Advanced Mathematical Functions
**File:** `plugins/advanced_math.py`  
**Operations:** 8 functions

Provides advanced mathematical operations including rounding, number theory, and special functions.

#### Rounding and Floor/Ceiling
- `ceil <x>` - Return smallest integer ≥ x
- `floor <x>` - Return largest integer ≤ x  
- `round <x> <digits>` - Round to specified decimal places
- `trunc <x>` - Remove fractional part

#### Number Theory
- `gcd <a> <b>` - Greatest common divisor of two integers
- `lcm <a> <b>` - Least common multiple of two integers
- `mod <a> <b>` - Modulo operation (remainder)
- `remainder <a> <b>` - IEEE remainder

#### Special Functions
- `exp <x>` - Calculate e^x

**Example Usage:**
```bash
python math_cli.py ceil 3.2          # Result: 4
python math_cli.py gcd 48 18         # Result: 6
python math_cli.py round 3.14159 2   # Result: 3.14
```

### Statistical Functions
**File:** `plugins/statistics.py`  
**Operations:** 15 functions (all variadic)

Provides comprehensive statistical analysis capabilities. All functions accept multiple arguments.

#### Central Tendency
- `mean <numbers...>` - Arithmetic mean (average)
- `median <numbers...>` - Median value
- `mode <numbers...>` - Most frequent value
- `geometric_mean <numbers...>` - Geometric mean (all positive numbers)
- `harmonic_mean <numbers...>` - Harmonic mean (all positive numbers)

#### Variability Measures  
- `variance <numbers...>` - Sample variance
- `pop_variance <numbers...>` - Population variance
- `std_dev <numbers...>` - Sample standard deviation
- `pop_std_dev <numbers...>` - Population standard deviation
- `range <numbers...>` - Difference between max and min

#### Aggregation Functions
- `min <numbers...>` - Minimum value
- `max <numbers...>` - Maximum value
- `sum <numbers...>` - Sum of all values
- `product <numbers...>` - Product of all values
- `count <numbers...>` - Count of values provided

**Example Usage:**
```bash
python math_cli.py mean 10 20 30 40 50           # Result: 30.0
python math_cli.py std_dev 2 4 4 4 5 5 7 9       # Result: 2.138
python math_cli.py max 15 8 23 12 19              # Result: 23.0
```

### Combinatorics & Number Theory
**File:** `plugins/combinatorics.py`  
**Operations:** 10 functions

Provides combinatorial calculations, number theory functions, and sequence operations.

#### Combinatorial Functions
- `combinations <n> <r>` - nCr (n choose r) combinations
- `permutations <n> <r>` - nPr (n permute r) arrangements

#### Number Sequences
- `fibonacci <n>` - nth Fibonacci number (0-indexed)

#### Number Theory
- `is_prime <n>` - Check if number is prime (returns 1/0)
- `prime_factors <n>` - Product of prime factors
- `is_even <n>` - Check if number is even (returns 1/0)
- `is_odd <n>` - Check if number is odd (returns 1/0)
- `is_perfect_square <n>` - Check if number is perfect square (returns 1/0)

#### Number Manipulation
- `digit_sum <n>` - Sum of digits in a number
- `reverse_number <n>` - Reverse the digits of a number

**Example Usage:**
```bash
python math_cli.py combinations 10 3     # Result: 120
python math_cli.py fibonacci 12          # Result: 144
python math_cli.py is_prime 17           # Result: 1 (true)
```

### Geometric Functions
**File:** `plugins/geometry.py`  
**Operations:** 15 functions

Provides geometric calculations for 2D and 3D shapes, distances, and areas.

#### Distance Calculations
- `distance <x1> <y1> <x2> <y2>` - 2D Euclidean distance
- `distance3d <x1> <y1> <z1> <x2> <y2> <z2>` - 3D Euclidean distance

#### Circle Calculations
- `area_circle <radius>` - Circle area
- `circumference <radius>` - Circle circumference

#### Triangle Calculations
- `area_triangle <base> <height>` - Triangle area (base × height)
- `area_triangle_heron <a> <b> <c>` - Triangle area using Heron's formula
- `pythagorean <a> <b>` - Calculate hypotenuse
- `pythagorean_side <hypotenuse> <side>` - Calculate unknown side

#### Rectangle/Square Calculations
- `area_rectangle <length> <width>` - Rectangle area
- `perimeter_rectangle <length> <width>` - Rectangle perimeter
- `area_square <side>` - Square area

#### 3D Shape Calculations
- `volume_sphere <radius>` - Sphere volume
- `surface_area_sphere <radius>` - Sphere surface area
- `volume_cylinder <radius> <height>` - Cylinder volume

#### Regular Polygons
- `area_regular_polygon <sides> <length>` - Regular polygon area

**Example Usage:**
```bash
python math_cli.py distance 0 0 3 4      # Result: 5.0
python math_cli.py area_circle 5         # Result: 78.54
python math_cli.py volume_sphere 2       # Result: 33.51
```

### Complex Number Operations
**File:** `plugins/complex_math.py`  
**Operations:** 11 functions

Provides comprehensive complex number arithmetic and conversions.

#### Basic Arithmetic
- `complex_add <real1> <imag1> <real2> <imag2>` - Add complex numbers
- `complex_subtract <real1> <imag1> <real2> <imag2>` - Subtract complex numbers
- `complex_multiply <real1> <imag1> <real2> <imag2>` - Multiply complex numbers
- `complex_divide <real1> <imag1> <real2> <imag2>` - Divide complex numbers

#### Properties and Conversions
- `complex_magnitude <real> <imag>` - Calculate magnitude (absolute value)
- `complex_phase <real> <imag>` - Calculate phase (argument) in radians
- `complex_conjugate <real> <imag>` - Calculate complex conjugate

#### Coordinate Conversions
- `polar_to_rect <magnitude> <phase>` - Convert polar to rectangular form
- `rect_to_polar <real> <imag>` - Convert rectangular to polar form

#### Advanced Operations
- `complex_power <real> <imag> <exponent>` - Raise complex number to power
- `complex_exp <real> <imag>` - Calculate e^(complex number)
- `complex_log <real> <imag>` - Natural logarithm of complex number

**Example Usage:**
```bash
python math_cli.py complex_add 3 4 2 -1      # Result: 5.0 + 3.0i
python math_cli.py complex_magnitude 3 4     # Result: 5.0
python math_cli.py polar_to_rect 5 0.927     # Result: 3.0 + 4.0i
```

### Mathematical Constants
**File:** `plugins/constants.py`  
**Operations:** 15 constants (zero arguments)

Provides access to important mathematical and physical constants.

#### Mathematical Constants
- `pi` - π (3.14159...)
- `e` - Euler's number (2.71828...)
- `tau` - τ = 2π (6.28318...)
- `golden_ratio` - φ (phi) ≈ 1.618
- `sqrt2` - √2 ≈ 1.414
- `sqrt3` - √3 ≈ 1.732
- `euler_gamma` - Euler-Mascheroni constant γ ≈ 0.5772
- `ln2` - Natural logarithm of 2
- `ln10` - Natural logarithm of 10

#### Physical Constants
- `speed_of_light` - c = 299,792,458 m/s
- `planck` - Planck's constant (6.626×10⁻³⁴ J⋅s)
- `gravitational_constant` - G (6.674×10⁻¹¹ m³/kg⋅s²)
- `avogadro` - Avogadro's number (6.022×10²³ mol⁻¹)
- `boltzmann` - Boltzmann constant (1.381×10⁻²³ J/K)
- `elementary_charge` - e = 1.602×10⁻¹⁹ C
- `electron_mass` - mₑ (9.109×10⁻³¹ kg)
- `proton_mass` - mₚ (1.673×10⁻²⁷ kg)
- `neutron_mass` - mₙ (1.675×10⁻²⁷ kg)

**Example Usage:**
```bash
python math_cli.py pi                     # Result: 3.141592653589793
python math_cli.py golden_ratio           # Result: 1.618033988749895
python math_cli.py speed_of_light         # Result: 299792458
```

### Unit Conversions
**File:** `plugins/conversions.py`  
**Operations:** 35 functions

Provides comprehensive unit conversion capabilities across multiple measurement systems.

#### Temperature Conversions
- `celsius_to_fahrenheit <celsius>` - °C to °F
- `fahrenheit_to_celsius <fahrenheit>` - °F to °C
- `celsius_to_kelvin <celsius>` - °C to K
- `kelvin_to_celsius <kelvin>` - K to °C  
- `fahrenheit_to_kelvin <fahrenheit>` - °F to K
- `kelvin_to_fahrenheit <kelvin>` - K to °F

#### Length Conversions
- `meters_to_feet <meters>` - m to ft
- `feet_to_meters <feet>` - ft to m
- `inches_to_meters <inches>` - in to m
- `meters_to_inches <meters>` - m to in
- `kilometers_to_miles <km>` - km to mi
- `miles_to_kilometers <miles>` - mi to km
- `inches_to_centimeters <inches>` - in to cm
- `centimeters_to_inches <cm>` - cm to in

#### Weight/Mass Conversions
- `kilograms_to_pounds <kg>` - kg to lb
- `pounds_to_kilograms <pounds>` - lb to kg
- `grams_to_pounds <grams>` - g to lb
- `pounds_to_grams <pounds>` - lb to g
- `grams_to_ounces <grams>` - g to oz
- `ounces_to_grams <ounces>` - oz to g

#### Volume Conversions
- `liters_to_gallons <liters>` - L to gal (US)
- `gallons_to_liters <gallons>` - gal (US) to L
- `liters_to_quarts <liters>` - L to qt (US)
- `quarts_to_liters <quarts>` - qt (US) to L
- `milliliters_to_fluid_ounces <ml>` - mL to fl oz (US)
- `fluid_ounces_to_milliliters <fl_oz>` - fl oz (US) to mL

#### Area Conversions
- `square_meters_to_square_feet <sq_m>` - m² to ft²
- `square_feet_to_square_meters <sq_ft>` - ft² to m²
- `acres_to_square_meters <acres>` - acres to m²
- `square_meters_to_acres <sq_m>` - m² to acres

#### Speed Conversions
- `mps_to_mph <mps>` - m/s to mph
- `mph_to_mps <mph>` - mph to m/s
- `kph_to_mph <kph>` - km/h to mph
- `mph_to_kph <mph>` - mph to km/h

#### Energy Conversions
- `joules_to_calories <joules>` - J to cal
- `calories_to_joules <calories>` - cal to J
- `kwh_to_joules <kwh>` - kWh to J
- `joules_to_kwh <joules>` - J to kWh

**Example Usage:**
```bash
python math_cli.py celsius_to_fahrenheit 25    # Result: 77.0
python math_cli.py miles_to_kilometers 100     # Result: 160.93
python math_cli.py kilograms_to_pounds 70      # Result: 154.32
```

## Usage Examples

### Command Line Usage

#### Basic Operations
```bash
# Statistical analysis
python math_cli.py mean 85 92 78 96 88 91 87 94 89 93
python math_cli.py std_dev 85 92 78 96 88 91 87 94 89 93

# Complex number arithmetic
python math_cli.py complex_add 3 4 2 -1
python math_cli.py complex_magnitude 3 4

# Unit conversions
python math_cli.py celsius_to_fahrenheit 25
python math_cli.py miles_to_kilometers 100

# Geometric calculations
python math_cli.py area_circle 5
python math_cli.py volume_sphere 3
```

### Interactive Mode Usage

```bash
python math_cli.py --interactive
```

#### Statistical Analysis Session
```
Enter command: mean 100 200 300 400 500
Result: 300.0

Enter command: std_dev 100 200 300 400 500  
Result: 158.11

Enter command: max 100 200 300 400 500
Result: 500.0

Enter command: min 100 200 300 400 500
Result: 100.0
```

#### Chain Operations
```
Enter command: chain mean 10 20 30 40 50 | sqrt $ | round $ 2
Step 1: mean 10 20 30 40 50 = 30.0
Step 2: sqrt $ = 5.477225575051661  
Step 3: round $ 2 = 5.48
Final result: 5.48

Enter command: chain sum 1 2 3 4 5 | factorial $
Step 1: sum 1 2 3 4 5 = 15.0
Step 2: factorial $ = 1307674368000.0
Final result: 1307674368000.0
```

#### Complex Number Calculations
```
Enter command: complex_add 2 3 1 -2
Result: 3.0 + 1.0i

Enter command: complex_magnitude 3 1
Result: 3.1622776601683795

Enter command: rect_to_polar 3 1  
Result: Magnitude: 3.1622776601683795, Phase: 0.32175 radians
```

## Plugin Architecture

### Variadic Operations

15 operations support variable arguments (marked with `variadic = True`):

#### Statistical Functions (All Variadic)
- `mean`, `median`, `mode`
- `variance`, `pop_variance` 
- `std_dev`, `pop_std_dev`
- `min`, `max`, `range`
- `sum`, `product`, `count`
- `geometric_mean`, `harmonic_mean`

These functions can accept any number of arguments:
```bash
python math_cli.py mean 1 2 3                    # 3 arguments
python math_cli.py sum 5 10 15 20 25 30          # 6 arguments
python math_cli.py max 3 7 2 9 1 5 8 4           # 8 arguments
```

### Error Handling

All plugins include comprehensive error handling:

```python
# Example from statistical functions
def execute(cls, *numbers):
    if len(numbers) == 0:
        raise ValueError("Cannot calculate mean of empty list")
    return sum(numbers) / len(numbers)

# Example from geometric functions  
def execute(cls, radius):
    if radius < 0:
        raise ValueError("Radius must be non-negative")
    return math.pi * radius ** 2
```

### Plugin Template Structure

Each plugin follows this structure:

```python
"""
Plugin Name Plugin

Brief description of plugin functionality.
"""

import math
from core.base_operations import MathOperation

class ExampleOperation(MathOperation):
    name = "operation_name"           # Command name
    args = ["arg1", "arg2"]          # Argument names  
    help = "Description of operation"  # Help text
    variadic = False                 # True for variable arguments
    
    @classmethod
    def execute(cls, arg1, arg2):
        """Implementation with error checking."""
        # Input validation
        if arg1 < 0:
            raise ValueError("arg1 must be non-negative")
            
        # Calculation
        result = arg1 + arg2
        return result
```

## Creating Your Own Plugins

### Basic Plugin Creation

1. **Create a new Python file** in the `plugins/` directory
2. **Import the base class:** `from core.base_operations import MathOperation`
3. **Define operation classes** inheriting from `MathOperation`
4. **Set required attributes:** `name`, `args`, `help`
5. **Implement the `execute()` method**

### Example: Custom Physics Plugin

```python
# plugins/physics.py
"""
Physics Calculations Plugin

Provides physics-related calculations and formulas.
"""

import math
from core.base_operations import MathOperation

class KineticEnergyOperation(MathOperation):
    name = "kinetic_energy"
    args = ["mass", "velocity"]
    help = "Calculate kinetic energy (KE = 0.5 * m * v²)"
    
    @classmethod
    def execute(cls, mass, velocity):
        if mass <= 0:
            raise ValueError("Mass must be positive")
        return 0.5 * mass * velocity ** 2

class PotentialEnergyOperation(MathOperation):
    name = "potential_energy"  
    args = ["mass", "height"]
    help = "Calculate gravitational potential energy (PE = mgh)"
    
    @classmethod
    def execute(cls, mass, height):
        if mass <= 0:
            raise ValueError("Mass must be positive")
        g = 9.81  # gravitational acceleration
        return mass * g * height

class WaveSpeedOperation(MathOperation):
    name = "wave_speed"
    args = ["frequency", "wavelength"]
    help = "Calculate wave speed (v = f * λ)"
    
    @classmethod  
    def execute(cls, frequency, wavelength):
        if frequency <= 0 or wavelength <= 0:
            raise ValueError("Frequency and wavelength must be positive")
        return frequency * wavelength
```

### Best Practices for Plugin Development

1. **Error Handling:** Always validate inputs and provide clear error messages
2. **Documentation:** Include comprehensive help text and docstrings
3. **Domain Validation:** Check for mathematically valid inputs (e.g., non-negative radii)
4. **Consistent Naming:** Use clear, descriptive operation names
5. **Logical Grouping:** Group related operations in the same plugin file
6. **Unit Considerations:** Clearly document expected units in help text

### Advanced Features

#### Variadic Operations
For operations accepting multiple arguments:

```python
class AverageOperation(MathOperation):
    name = "average"
    args = ["numbers"]
    help = "Calculate average of multiple numbers"
    variadic = True  # Enable variable arguments
    
    @classmethod
    def execute(cls, *numbers):
        if len(numbers) == 0:
            raise ValueError("Cannot calculate average of empty list")
        return sum(numbers) / len(numbers)
```

#### Complex Return Values
For operations returning formatted strings:

```python  
class ComplexAddOperation(MathOperation):
    name = "complex_add"
    args = ["real1", "imag1", "real2", "imag2"]
    help = "Add two complex numbers"
    
    @classmethod
    def execute(cls, real1, imag1, real2, imag2):
        real_result = real1 + real2
        imag_result = imag1 + imag2
        
        # Format as complex number string
        if imag_result >= 0:
            return f"{real_result} + {imag_result}i"
        else:
            return f"{real_result} - {abs(imag_result)}i"
```

The core plugins demonstrate these techniques and serve as excellent templates for developing your own specialized mathematical operations.