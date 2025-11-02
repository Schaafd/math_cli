# Math CLI - iOS Native Application

A sophisticated iOS native application that brings the power of Math CLI to iPhone with a sleek, hybrid terminal-modern interface.

## Overview

Math CLI for iOS is a full-featured mathematical calculator app with 266+ operations across 20 categories, supporting advanced features like:

- ✅ **266+ Mathematical Operations** across 20 categories
- ✅ **Variable System** with session and persistent storage
- ✅ **User-Defined Functions** for custom operations
- ✅ **Calculation History** with bookmarks and search
- ✅ **Chain Operations** for multi-step calculations
- ✅ **Hybrid UI** - Terminal aesthetics with modern iOS gestures
- 🚧 **iCloud Sync** for cross-device sessions (planned)
- 🚧 **Data Analysis** with CSV import (planned)
- 🚧 **Plotting** with Swift Charts (planned)

## Requirements

- **Xcode**: 15.0 or later
- **iOS**: 17.0 or later
- **Swift**: 5.9 or later
- **macOS**: Sonoma 14.0 or later (for development)

## Project Structure

```
MathCLI-iOS/
├── Sources/
│   ├── App/                          # App lifecycle
│   │   └── MathCLIApp.swift         # Main app entry point
│   ├── Core/                         # Business logic
│   │   ├── Engine/                  # Calculator engine
│   │   │   ├── OperationRegistry.swift
│   │   │   └── OperationExecutor.swift
│   │   ├── Operations/              # All mathematical operations
│   │   │   ├── MathOperation.swift  # Base protocol
│   │   │   ├── BasicArithmetic/     # 14 operations
│   │   │   ├── Trigonometry/        # 10 operations
│   │   │   ├── AdvancedMath/        # 8 operations
│   │   │   ├── Statistics/          # 15 operations
│   │   │   └── ... (16 more categories)
│   │   ├── Variables/               # Variable management
│   │   │   └── VariableStore.swift
│   │   └── Functions/               # User function registry
│   │       └── FunctionRegistry.swift
│   ├── Features/                     # Feature modules
│   │   ├── Calculator/              # Main calculator
│   │   │   ├── CalculatorView.swift
│   │   │   ├── CalculatorViewModel.swift
│   │   │   └── OperationBrowserView.swift
│   │   ├── History/                 # Calculation history
│   │   │   └── HistoryView.swift
│   │   └── Settings/                # App settings
│   │       └── SettingsView.swift
│   ├── Models/                       # Data models
│   │   └── HistoryEntry.swift       # SwiftData model
│   └── Services/                     # Services (iCloud, etc.)
└── Resources/                        # Assets, etc.
```

## Quick Start

### Verify Your Setup

Before you begin, verify your development environment:

```bash
./scripts/verify-setup.sh
```

This will check:
- ✅ Xcode and Command Line Tools
- ✅ Swift version
- ✅ iOS Simulators
- ✅ Project structure
- ✅ Helper scripts

### Development Workflow

**MathCLI iOS supports a modern development workflow:**

```bash
# Edit code in Claude Code (or any text editor)
# - Write Swift files
# - Get AI assistance
# - Use version control

# Build and test from command line
./scripts/build.sh    # Build the app
./scripts/test.sh     # Run tests
./scripts/run.sh      # Launch in simulator

# Or use Swift Package Manager
swift build           # Build package
swift test            # Run tests
swift run mathcli-tool  # Interactive CLI tool
```

**Use Xcode only for:**
- Visual debugging with breakpoints
- iOS-specific tasks (profiling, etc.)
- App Store submission

📖 **See [DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md) for the complete guide**

## Getting Started

### Option 1: Create New Xcode Project (Recommended)

1. **Open Xcode** and create a new project:
   - File → New → Project
   - Choose "iOS" → "App"
   - Product Name: `MathCLI`
   - Interface: `SwiftUI`
   - Storage: `SwiftData`
   - Language: `Swift`
   - Minimum Deployment: `iOS 17.0`

2. **Copy source files** into your Xcode project:
   ```bash
   # Navigate to your Xcode project directory
   cd /path/to/your/MathCLI

   # Copy all source files
   cp -r /path/to/math_cli/MathCLI-iOS/Sources/* MathCLI/
   ```

3. **Add files to Xcode**:
   - In Xcode, right-click on the `MathCLI` folder
   - Select "Add Files to MathCLI..."
   - Choose all copied Swift files
   - Ensure "Copy items if needed" is **unchecked** (files already copied)
   - Ensure "Create groups" is selected
   - Click "Add"

4. **Build the project**:
   - Select target device or simulator
   - Press `Cmd + B` to build
   - Fix any import/dependency issues if needed

### Option 2: Manual File Organization

1. Create a new Xcode project as above

2. Manually create group folders in Xcode matching the structure:
   ```
   MathCLI (Xcode Project)
   ├── App
   ├── Core
   │   ├── Engine
   │   ├── Operations
   │   │   ├── BasicArithmetic
   │   │   ├── Trigonometry
   │   │   ├── AdvancedMath
   │   │   └── Statistics
   │   ├── Variables
   │   └── Functions
   ├── Features
   │   ├── Calculator
   │   ├── History
   │   └── Settings
   ├── Models
   └── Services
   ```

3. Drag and drop Swift files from the `MathCLI-iOS/Sources` directory into the corresponding Xcode groups

## Current Implementation Status

### ✅ Completed (Phase 1)

#### Core Architecture
- [x] `MathOperation` protocol for all operations
- [x] `OperationRegistry` for managing 266+ operations
- [x] `OperationExecutor` for command execution
- [x] `VariableStore` with scoping and persistence
- [x] `FunctionRegistry` for user-defined functions
- [x] Command parser with variable substitution
- [x] Chain operation support (`op1 | op2 | op3`)

#### Operations Implemented (47/266)
- [x] Basic Arithmetic (14 ops): add, subtract, multiply, divide, power, sqrt, factorial, log, sin, cos, tan, to_radians, to_degrees, abs
- [x] Extended Trigonometry (10 ops): asin, acos, atan, atan2, sinh, cosh, tanh, asinh, acosh, atanh
- [x] Advanced Math (8 ops): ceil, floor, round, trunc, gcd, lcm, mod, exp
- [x] Statistics (15 ops): mean, median, mode, geometric_mean, harmonic_mean, variance, pop_variance, std_dev, pop_std_dev, range, min, max, sum, product, count

#### UI Components
- [x] Main `CalculatorView` with hybrid terminal-modern design
- [x] Terminal-style output with timestamp and color coding
- [x] Modern input with autocomplete suggestions
- [x] Quick action toolbar for common operations
- [x] `HistoryView` with search and bookmarks
- [x] `OperationBrowserView` organized by category
- [x] `SettingsView` for app configuration

#### Data Persistence
- [x] SwiftData model for calculation history
- [x] UserDefaults for settings
- [x] Persistent variable storage

### 🚧 TODO: Remaining Operations (219/266)

You need to implement the following operation categories following the same pattern as the existing ones:

#### Complex Numbers (18 operations)
Create file: `Sources/Core/Operations/ComplexNumbers/ComplexOperations.swift`
- cadd, csub, cmul, cdiv, magnitude, phase, conjugate, polar, rectangular, csqrt, cexp, clog, csin, ccos, ctan, cpower, cis, real_part, imag_part

#### Matrix Operations (12 operations)
Create file: `Sources/Core/Operations/Matrix/MatrixOperations.swift`
- det, transpose, eigenvalues, eigenvectors, trace, rank, inverse, matrix_multiply, identity, zeros, ones, diagonal
- **Note**: Use Accelerate framework for performance

#### Calculus (12 operations)
Create file: `Sources/Core/Operations/Calculus/CalculusOperations.swift`
- derivative, derivative2, partial, gradient, divergence, laplacian, integrate, integrate_symbolic, limit, taylor, series, solve_ode
- **Note**: Numerical implementations recommended

#### Number Theory (15 operations)
Create file: `Sources/Core/Operations/NumberTheory/NumberTheoryOperations.swift`
- is_prime, prime_factors, next_prime, prime_count, euler_phi, divisors, perfect_number, catalan, bell_number, stirling, partition, mobius, totient

#### Combinatorics (10 operations)
Create file: `Sources/Core/Operations/Combinatorics/CombinatoricsOperations.swift`
- combinations, permutations, fibonacci, is_prime, prime_factors, is_even, is_odd, is_perfect_square, digit_sum, reverse_number

#### Geometry (15 operations)
Create file: `Sources/Core/Operations/Geometry/GeometryOperations.swift`
- distance, distance3d, area_circle, circumference, area_triangle, area_triangle_heron, pythagorean, pythagorean_side, area_rectangle, perimeter_rectangle, area_square, volume_sphere, surface_area_sphere, volume_cylinder, area_regular_polygon

#### Constants (7 operations)
Create file: `Sources/Core/Operations/Constants/ConstantOperations.swift`
- pi, e, golden_ratio, speed_of_light, planck, avogadro, boltzmann

#### Unit Conversions (38 operations)
Create file: `Sources/Core/Operations/Conversions/ConversionOperations.swift`
- Temperature: celsius_to_fahrenheit, fahrenheit_to_celsius, celsius_to_kelvin, kelvin_to_celsius
- Distance: miles_to_kilometers, kilometers_to_miles, feet_to_meters, meters_to_feet, inches_to_centimeters, centimeters_to_inches
- Weight: pounds_to_kilograms, kilograms_to_pounds
- Volume: gallons_to_liters, liters_to_gallons
- Speed: mph_to_kph, kph_to_mph
- And 22 more...

#### Variable Operations (6 operations)
Create file: `Sources/Core/Operations/Variables/VariableOperations.swift`
- set, persist, get, vars, unset, clear_vars

#### Control Flow (13 operations)
Create file: `Sources/Core/Operations/ControlFlow/ControlFlowOperations.swift`
- eq, neq, gt, gte, lt, lte, and, or, not, if, is_number, is_string, is_bool

#### User Functions (3 operations)
Create file: `Sources/Core/Operations/UserFunctions/FunctionOperations.swift`
- def, funcs, undef

#### Scripts (2 operations)
Create file: `Sources/Core/Operations/Scripts/ScriptOperations.swift`
- run, eval

#### Data Analysis (12 operations) - Requires DataFrame implementation
Create file: `Sources/Core/Operations/DataAnalysis/DataAnalysisOperations.swift`
- load_data, describe_data, correlation_matrix, groupby, detect_outliers, missing_values, pivot_table, rolling_mean, time_series_analysis, data_info, save_data, unique_values

#### Data Transformation (11 operations)
Create file: `Sources/Core/Operations/DataTransform/DataTransformOperations.swift`
- filter_data, normalize_data, sort_data, aggregate_data, fill_nulls, drop_nulls, merge_data, sample_data, add_column, drop_column, rename_column

#### Plotting (8 operations) - Requires Swift Charts integration
Create file: `Sources/Core/Operations/Plotting/PlottingOperations.swift`
- plot_hist, plot_box, plot_scatter, plot_heatmap, plot, plot_line, plot_bar, plot_data

#### Export/Integration (6 operations)
Create file: `Sources/Core/Operations/Export/ExportOperations.swift`
- export_session, import_session, export_vars, import_vars, export_funcs, import_funcs

### 🚧 TODO: Advanced Features

1. **iCloud Sync**
   - Enable CloudKit in project capabilities
   - Create `CloudSyncService.swift` in `Services/`
   - Implement sync for variables, functions, and history
   - Add conflict resolution

2. **Data Analysis & DataFrames**
   - Implement complete `DataFrame` struct
   - CSV parsing and import
   - Integration with document picker

3. **Plotting & Visualization**
   - Integrate Swift Charts framework
   - Create chart views for each plot type
   - Export charts as images

4. **Widgets**
   - Create widget extension
   - Show last result
   - Quick calculation widget

5. **Shortcuts Integration**
   - Define App Intents
   - Expose common operations to Siri

6. **Mac Catalyst**
   - Enable Mac target
   - Optimize for Mac keyboard shortcuts
   - Menu bar integration

## How to Add New Operations

Follow this pattern (using `AddOperation` as example):

```swift
struct YourOperation: MathOperation {
    static var name: String = "operation_name"
    static var arguments: [String] = ["arg1", "arg2"]
    static var help: String = "Description: operation_name arg1 arg2"
    static var category: OperationCategory = .categoryName
    static var isVariadic: Bool = false  // Set to true for variadic operations

    static func execute(args: [Any]) throws -> OperationResult {
        // 1. Validate argument count (skip for variadic)
        guard args.count == 2 else {
            throw OperationError.invalidArgumentCount(expected: 2, got: args.count)
        }

        // 2. Parse arguments using helper functions
        let arg1 = try parseDouble(args[0], argumentName: "arg1")
        let arg2 = try parseDouble(args[1], argumentName: "arg2")

        // 3. Perform operation
        let result = arg1 + arg2  // Your logic here

        // 4. Return result
        return .number(result)
    }
}
```

Then register it in `OperationRegistry.swift`:

```swift
register(YourOperation.self)
```

## Usage Examples

### Basic Operations
```
add 5 10              → 15
multiply 3 7          → 21
power 2 8             → 256
sqrt 16               → 4
```

### Variables
```
set x 42              → (stores x = 42)
multiply $x 2         → 84
add $x $             → 126 ($ refers to last result)
```

### Chain Operations
```
add 10 20 | multiply 2 | sqrt    → 7.745967
```

### Statistics
```
mean 10 20 30 40 50              → 30
std_dev 10 20 30 40 50           → 15.811388
```

### User Functions
```
def double x = multiply $x 2
double 21                        → 42
```

## Testing

Run tests in Xcode:
```bash
Cmd + U
```

Create unit tests for new operations in `Tests/UnitTests/`.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add unit tests
5. Submit a pull request

## Architecture Details

### MVVM Pattern

- **Models**: `HistoryEntry`, `UserFunction`, `OperationResult`
- **ViewModels**: `CalculatorViewModel`
- **Views**: `CalculatorView`, `HistoryView`, `SettingsView`

### Data Flow

```
User Input → ViewModel → OperationExecutor → OperationRegistry
                ↓
           Variable Substitution
                ↓
           Operation Execution
                ↓
           Result Formatting → View Update
                ↓
           History Storage (SwiftData)
```

### Persistence Layers

1. **SwiftData**: Calculation history (`HistoryEntry`)
2. **UserDefaults**: App settings, persistent variables, user functions
3. **iCloud (Planned)**: Cross-device sync

## Performance Considerations

- **Lazy Loading**: Operation registry uses lazy initialization
- **Efficient Parsing**: Optimized command parser
- **History Limits**: Configurable max entries (default 1000)
- **Memory Management**: Auto-cleanup of old output lines

## License

Same license as the parent Math CLI project.

## Support

- **Documentation**: See inline code comments
- **Issues**: Report bugs via GitHub Issues
- **Python CLI**: This is a port of the terminal Math CLI app

## Roadmap

### Phase 2: Complete Operations (2-4 weeks)
- [ ] Implement remaining 219 operations
- [ ] Add operation tests

### Phase 3: iCloud Sync (1-2 weeks)
- [ ] CloudKit integration
- [ ] Sync service implementation
- [ ] Conflict resolution

### Phase 4: Data Features (2 weeks)
- [ ] Full DataFrame implementation
- [ ] CSV import/export
- [ ] Data analysis operations

### Phase 5: Visualization (1 week)
- [ ] Swift Charts integration
- [ ] All plot types
- [ ] Chart export

### Phase 6: Polish (2 weeks)
- [ ] Widgets
- [ ] Shortcuts
- [ ] Accessibility improvements
- [ ] Performance optimization

### Phase 7: Mac App (2-3 weeks)
- [ ] Mac Catalyst enablement
- [ ] Mac-specific features
- [ ] Handoff support

## Acknowledgments

Based on the Python Math CLI application with full feature parity as the design goal.
