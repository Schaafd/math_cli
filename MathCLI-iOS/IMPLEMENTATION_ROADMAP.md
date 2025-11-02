# Implementation Roadmap

This document provides a detailed roadmap for completing the Math CLI iOS app implementation.

## Current Status

### ✅ Phase 1: Foundation (COMPLETED)

**Completed Components:**
- Core architecture (MVVM pattern with SwiftUI)
- Operation protocol and registry system
- Variable store with persistence
- Function registry for user-defined functions
- Command parser with variable substitution
- Chain operation support
- 47 operations across 4 categories
- Full UI implementation (Calculator, History, Operations, Settings)
- SwiftData persistence for history
- Terminal-modern hybrid interface

**Files Created:** 17 Swift files totaling ~3,500 lines of code

**Time Spent:** ~4 hours

## Phase 2: Complete Core Operations (Estimated: 2-4 weeks)

### Priority 1: Essential Math Operations (1 week)

#### 2.1 Complex Numbers (18 operations)
**File:** `ComplexNumbers/ComplexOperations.swift`

**Implementation Steps:**
1. Define `ComplexNumber` struct:
```swift
struct ComplexNumber {
    let real: Double
    let imaginary: Double
}
```

2. Implement operations:
- [ ] cadd, csub, cmul, cdiv (arithmetic)
- [ ] magnitude, phase (properties)
- [ ] conjugate (transformation)
- [ ] polar, rectangular (conversion)
- [ ] csqrt, cexp, clog (functions)
- [ ] csin, ccos, ctan (trig)
- [ ] cpower, cis (special)
- [ ] real_part, imag_part (extractors)

**Register:** Add 18 `register()` calls to `OperationRegistry`

**Test:** Create unit tests for each operation

---

#### 2.2 Geometry (15 operations)
**File:** `Geometry/GeometryOperations.swift`

**Implementation:**
- [ ] distance, distance3d (point operations)
- [ ] area_circle, circumference (circle)
- [ ] area_triangle, area_triangle_heron (triangle)
- [ ] pythagorean, pythagorean_side (right triangle)
- [ ] area_rectangle, perimeter_rectangle, area_square (quadrilaterals)
- [ ] volume_sphere, surface_area_sphere (sphere)
- [ ] volume_cylinder (cylinder)
- [ ] area_regular_polygon (general polygon)

**Complexity:** Low - mostly formulas

---

#### 2.3 Combinatorics (10 operations)
**File:** `Combinatorics/CombinatoricsOperations.swift`

**Implementation:**
- [ ] combinations, permutations (core)
- [ ] fibonacci (sequence)
- [ ] is_prime, prime_factors (number properties)
- [ ] is_even, is_odd (parity)
- [ ] is_perfect_square (property)
- [ ] digit_sum, reverse_number (digit operations)

**Note:** Some overlap with NumberTheory

---

#### 2.4 Constants (7 operations)
**File:** `Constants/ConstantOperations.swift`

**Implementation:**
```swift
struct PiOperation: MathOperation {
    static var name = "pi"
    static var arguments: [String] = []
    static var help = "Return value of π"
    static var category = .constants

    static func execute(args: [Any]) throws -> OperationResult {
        return .number(Double.pi)
    }
}
```

Similar for:
- [ ] pi, e, golden_ratio (math constants)
- [ ] speed_of_light, planck, avogadro, boltzmann (physical constants)

**Complexity:** Very low - just return values

---

#### 2.5 Unit Conversions (38 operations)
**File:** `Conversions/ConversionOperations.swift`

**Categories:**
- [ ] Temperature (4): celsius_to_fahrenheit, fahrenheit_to_celsius, celsius_to_kelvin, kelvin_to_celsius
- [ ] Distance (6): miles_to_kilometers, kilometers_to_miles, feet_to_meters, meters_to_feet, inches_to_centimeters, centimeters_to_inches
- [ ] Weight (2): pounds_to_kilograms, kilograms_to_pounds
- [ ] Volume (2): gallons_to_liters, liters_to_gallons
- [ ] Speed (2): mph_to_kph, kph_to_mph
- [ ] Time (6): hours_to_seconds, minutes_to_seconds, days_to_hours, weeks_to_days, years_to_days, seconds_to_milliseconds
- [ ] Data (8): kb_to_bytes, mb_to_bytes, gb_to_bytes, tb_to_bytes, bytes_to_kb, bytes_to_mb, bytes_to_gb, bytes_to_tb
- [ ] Energy (4): joules_to_calories, calories_to_joules, kwh_to_joules, joules_to_kwh
- [ ] Pressure (4): psi_to_pascal, pascal_to_psi, bar_to_pascal, pascal_to_bar

**Pattern:**
```swift
struct CelsiusToFahrenheitOperation: MathOperation {
    static func execute(args: [Any]) throws -> OperationResult {
        let celsius = try parseDouble(args[0], argumentName: "celsius")
        return .number(celsius * 9/5 + 32)
    }
}
```

**Complexity:** Very low - simple formulas

---

### Priority 2: Advanced Math (1 week)

#### 2.6 Number Theory (15 operations)
**File:** `NumberTheory/NumberTheoryOperations.swift`

**Implementation:**
- [ ] is_prime (primality test)
- [ ] prime_factors (factorization)
- [ ] next_prime (find next prime)
- [ ] prime_count (count primes up to n)
- [ ] euler_phi (Euler's totient)
- [ ] divisors (all divisors)
- [ ] perfect_number (check if perfect)
- [ ] catalan (Catalan numbers)
- [ ] bell_number (Bell numbers)
- [ ] stirling (Stirling numbers)
- [ ] partition (integer partition)
- [ ] mobius (Möbius function)
- [ ] totient (alias for euler_phi)

**Complexity:** Medium - requires algorithms

**Algorithms needed:**
- Sieve of Eratosthenes (prime checking)
- Trial division (factorization)
- Recursive formulas (Catalan, Bell)

---

#### 2.7 Matrix Operations (12 operations)
**File:** `Matrix/MatrixOperations.swift`

**Implementation Steps:**

1. Create Matrix wrapper:
```swift
import Accelerate

class Matrix {
    let rows: Int
    let columns: Int
    var data: [Double]

    init(rows: Int, columns: Int, data: [Double]) {
        self.rows = rows
        self.columns = columns
        self.data = data
    }
}
```

2. Use Accelerate framework for performance:
```swift
import Accelerate

struct DeterminantOperation: MathOperation {
    static func execute(args: [Any]) throws -> OperationResult {
        let matrix = try parseMatrix(args[0])
        // Use LAPACK routines from Accelerate
        let det = calculateDeterminant(matrix)
        return .number(det)
    }
}
```

**Operations:**
- [ ] det (determinant)
- [ ] transpose
- [ ] eigenvalues, eigenvectors
- [ ] trace
- [ ] rank
- [ ] inverse
- [ ] matrix_multiply
- [ ] identity, zeros, ones (constructors)
- [ ] diagonal

**Complexity:** High - linear algebra algorithms

**Framework:** Use `Accelerate.framework` for BLAS/LAPACK

---

#### 2.8 Calculus (12 operations)
**File:** `Calculus/CalculusOperations.swift`

**Approach:** Numerical methods (symbolic math is complex)

**Implementation:**
- [ ] derivative (numerical differentiation)
- [ ] derivative2 (second derivative)
- [ ] partial (partial derivatives)
- [ ] gradient (vector of partials)
- [ ] divergence (vector calculus)
- [ ] laplacian (second-order differential)
- [ ] integrate (numerical integration - trapezoidal or Simpson's)
- [ ] integrate_symbolic (simplified - pattern matching)
- [ ] limit (numerical limit)
- [ ] taylor (Taylor series expansion)
- [ ] series (general series)
- [ ] solve_ode (Euler's method or RK4)

**Numerical Methods:**
```swift
// Numerical derivative using central difference
func derivative(f: (Double) -> Double, at x: Double, h: Double = 1e-5) -> Double {
    return (f(x + h) - f(x - h)) / (2 * h)
}
```

**Complexity:** High - numerical analysis

---

### Priority 3: Programming Features (1 week)

#### 2.9 Variable Operations (6 operations)
**File:** `Variables/VariableOperations.swift`

**Implementation:**
- [ ] set (already works in parser, but add as operation)
- [ ] persist (mark variable as persistent)
- [ ] get (get variable value)
- [ ] vars (list all variables)
- [ ] unset (delete variable)
- [ ] clear_vars (clear all)

**Integration:** These call `VariableStore` methods

```swift
struct SetOperation: MathOperation {
    static func execute(args: [Any]) throws -> OperationResult {
        let name = args[0] as? String ?? ""
        let value = try parseDouble(args[1], argumentName: "value")
        VariableStore.shared.set(name: name, value: .number(value))
        return .void
    }
}
```

**Complexity:** Low - wrapper operations

---

#### 2.10 Control Flow (13 operations)
**File:** `ControlFlow/ControlFlowOperations.swift`

**Comparison operators:**
- [ ] eq, neq, gt, gte, lt, lte

**Logical operators:**
- [ ] and, or, not

**Conditional:**
- [ ] if (ternary: `if condition then_value else_value`)

**Type checking:**
- [ ] is_number, is_string, is_bool

**Example:**
```swift
struct IfOperation: MathOperation {
    static var arguments = ["condition", "then_value", "else_value"]

    static func execute(args: [Any]) throws -> OperationResult {
        let condition = try parseBool(args[0], argumentName: "condition")
        return condition ? parse(args[1]) : parse(args[2])
    }
}
```

**Complexity:** Medium - type handling

---

#### 2.11 User Functions (3 operations)
**File:** `UserFunctions/FunctionOperations.swift`

**Implementation:**
- [ ] def (define function - already works, but formalize)
- [ ] funcs (list all functions)
- [ ] undef (delete function)

**Integration:** Wrapper for `FunctionRegistry`

```swift
struct DefOperation: MathOperation {
    static func execute(args: [Any]) throws -> OperationResult {
        let name = args[0] as? String ?? ""
        let params = extractParams(args[1...])
        let body = args.last as? String ?? ""
        FunctionRegistry.shared.define(name: name, parameters: params, body: body)
        return .void
    }
}
```

**Complexity:** Low - already implemented in registry

---

#### 2.12 Scripts (2 operations)
**File:** `Scripts/ScriptOperations.swift`

**Implementation:**
- [ ] run (execute .mathcli script file)
- [ ] eval (evaluate expression string)

**Script execution:**
```swift
struct RunOperation: MathOperation {
    static func execute(args: [Any]) throws -> OperationResult {
        let filepath = args[0] as? String ?? ""
        let script = try String(contentsOfFile: filepath)
        let lines = script.components(separatedBy: .newlines)

        var lastResult: OperationResult = .void
        for line in lines {
            if !line.isEmpty && !line.hasPrefix("#") {
                lastResult = try OperationExecutor().execute(command: line)
            }
        }
        return lastResult
    }
}
```

**Complexity:** Medium - file I/O integration

---

### Priority 4: Data Features (2 weeks)

#### 2.13 Data Analysis (12 operations)
**File:** `DataAnalysis/DataAnalysisOperations.swift`

**Prerequisites:**
1. Complete `DataFrame` implementation:
```swift
struct DataFrame {
    var columns: [String]
    var data: [[Any]]

    func select(columns: [String]) -> DataFrame { ... }
    func filter(predicate: (Row) -> Bool) -> DataFrame { ... }
    func groupBy(column: String) -> GroupedDataFrame { ... }
    // etc.
}
```

2. CSV parsing:
```swift
func parseCSV(filepath: String) -> DataFrame {
    // Use Foundation's CSV parsing or custom implementation
}
```

**Operations:**
- [ ] load_data (CSV/JSON import)
- [ ] describe_data (summary statistics)
- [ ] correlation_matrix (correlation analysis)
- [ ] groupby (group operations)
- [ ] detect_outliers (outlier detection)
- [ ] missing_values (find nulls)
- [ ] pivot_table (pivot/reshape)
- [ ] rolling_mean (moving average)
- [ ] time_series_analysis (trend analysis)
- [ ] data_info (metadata)
- [ ] save_data (export)
- [ ] unique_values (distinct values)

**Complexity:** Very High - requires full DataFrame implementation

**Recommendation:** Start with simple operations, expand DataFrame gradually

---

#### 2.14 Data Transformation (11 operations)
**File:** `DataTransform/DataTransformOperations.swift`

**Prerequisites:** Complete DataFrame implementation

**Operations:**
- [ ] filter_data (row filtering)
- [ ] normalize_data (min-max or z-score)
- [ ] sort_data (sort by column)
- [ ] aggregate_data (aggregations)
- [ ] fill_nulls (imputation)
- [ ] drop_nulls (remove missing)
- [ ] merge_data (join DataFrames)
- [ ] sample_data (random sample)
- [ ] add_column (add computed column)
- [ ] drop_column (remove column)
- [ ] rename_column (rename)

**Complexity:** Very High - depends on DataFrame

---

### Priority 5: Visualization (1 week)

#### 2.15 Plotting (8 operations)
**File:** `Plotting/PlottingOperations.swift`

**Prerequisites:**
1. Import Swift Charts:
```swift
import Charts
```

2. Create chart view factory:
```swift
struct ChartFactory {
    static func createLineChart(data: [Double]) -> some View {
        Chart {
            ForEach(Array(data.enumerated()), id: \.offset) { index, value in
                LineMark(
                    x: .value("Index", index),
                    y: .value("Value", value)
                )
            }
        }
    }
}
```

**Operations:**
- [ ] plot_hist (histogram)
- [ ] plot_box (box plot)
- [ ] plot_scatter (scatter plot)
- [ ] plot_heatmap (heatmap)
- [ ] plot (generic plot)
- [ ] plot_line (line chart)
- [ ] plot_bar (bar chart)
- [ ] plot_data (DataFrame plot)

**Implementation approach:**
1. Generate chart configuration
2. Store chart ID
3. Display in separate view or modal
4. Allow export as image

**Complexity:** Medium-High - SwiftUI Charts integration

---

### Priority 6: Export/Integration (3 days)

#### 2.16 Export Operations (6 operations)
**File:** `Export/ExportOperations.swift`

**Implementation:**
- [ ] export_session (save variables + functions + history)
- [ ] import_session (load session)
- [ ] export_vars (export variables only)
- [ ] import_vars (import variables)
- [ ] export_funcs (export functions)
- [ ] import_funcs (import functions)

**Format support:**
- JSON (primary)
- Markdown (human-readable)
- PDF (formatted report)

**Example:**
```swift
struct ExportSessionOperation: MathOperation {
    static func execute(args: [Any]) throws -> OperationResult {
        let filepath = args[0] as? String ?? ""
        let format = args.count > 1 ? args[1] as? String : "json"

        let session = SessionData(
            variables: VariableStore.shared.exportVariables(),
            functions: FunctionRegistry.shared.exportFunctions(),
            timestamp: Date()
        )

        try session.save(to: filepath, format: format)
        return .void
    }
}
```

**Complexity:** Medium - file I/O and serialization

---

## Phase 3: iCloud Sync (1-2 weeks)

### 3.1 CloudKit Setup
1. Enable CloudKit capability
2. Create container schema
3. Define record types

### 3.2 Sync Service Implementation
**File:** `Services/CloudSyncService.swift`

**Features:**
- Bi-directional sync
- Conflict resolution
- Background sync
- Manual sync trigger

**Implementation:**
```swift
class CloudSyncService {
    func syncVariables() async throws { ... }
    func syncFunctions() async throws { ... }
    func syncHistory() async throws { ... }
    func resolveConflicts() { ... }
}
```

### 3.3 UI Integration
- Sync status indicator
- Manual sync button
- Conflict resolution UI

---

## Phase 4: Polish & Optimization (2 weeks)

### 4.1 Testing
- [ ] Unit tests for all 266 operations
- [ ] Integration tests
- [ ] UI tests
- [ ] Performance tests

### 4.2 Performance Optimization
- [ ] Profile with Instruments
- [ ] Optimize matrix operations
- [ ] Cache calculations
- [ ] Lazy loading for history

### 4.3 Accessibility
- [ ] VoiceOver support
- [ ] Dynamic Type
- [ ] High contrast themes
- [ ] Voice Control

### 4.4 Documentation
- [ ] Operation reference
- [ ] User guide
- [ ] API documentation
- [ ] Video tutorials

---

## Phase 5: Advanced Features (2-3 weeks)

### 5.1 Widgets
- Last result widget
- Quick calculation widget
- Variable monitor

### 5.2 Shortcuts Integration
- App Intents
- Siri support
- Shortcuts actions

### 5.3 Mac App (Catalyst)
- Enable Mac target
- Mac-specific UI
- Menu bar integration
- Keyboard shortcuts

---

## Development Timeline

| Phase | Duration | Effort | Priority |
|-------|----------|--------|----------|
| **Phase 1: Foundation** | ✅ Complete | 4 hours | Critical |
| **Phase 2.1: Essential Math** | 1 week | 30-40 hours | High |
| **Phase 2.2: Advanced Math** | 1 week | 30-40 hours | High |
| **Phase 2.3: Programming** | 1 week | 20-30 hours | Medium |
| **Phase 2.4: Data** | 2 weeks | 50-60 hours | Medium |
| **Phase 2.5: Visualization** | 1 week | 20-30 hours | Medium |
| **Phase 2.6: Export** | 3 days | 15-20 hours | Medium |
| **Phase 3: iCloud** | 1-2 weeks | 30-40 hours | High |
| **Phase 4: Polish** | 2 weeks | 40-50 hours | High |
| **Phase 5: Advanced** | 2-3 weeks | 40-60 hours | Low |
| **TOTAL** | **3-4 months** | **275-370 hours** | |

---

## Recommended Development Order

### Week 1-2: Core Operations
1. ✅ Foundation (done)
2. Constants (easy win)
3. Unit Conversions (easy, many operations)
4. Geometry (straightforward formulas)
5. Combinatorics (medium complexity)

### Week 3-4: Advanced Math
1. Complex Numbers
2. Number Theory
3. Matrix Operations (use Accelerate)
4. Calculus (numerical methods)

### Week 5: Programming Features
1. Variable operations
2. Control flow
3. User functions
4. Scripts

### Week 6-7: Data Features
1. DataFrame implementation
2. Data analysis operations
3. Data transformation

### Week 8: Visualization
1. Swift Charts integration
2. All plot types
3. Chart export

### Week 9-10: iCloud & Polish
1. CloudKit setup
2. Sync implementation
3. Testing
4. Bug fixes

### Week 11-12: Advanced Features
1. Widgets
2. Shortcuts
3. Mac app (optional)

---

## Testing Strategy

### Unit Tests
Create test file for each operation category:
```swift
// Tests/UnitTests/BasicArithmeticTests.swift
class BasicArithmeticTests: XCTestCase {
    func testAdd() throws {
        let result = try AddOperation.execute(args: [5, 10])
        XCTAssertEqual(result, .number(15))
    }
}
```

### Coverage Goals
- **Operations**: 100% (critical)
- **Core Engine**: 95%
- **UI ViewModels**: 80%
- **Overall**: >85%

---

## Success Metrics

### Phase 2 Complete
- [ ] All 266 operations implemented
- [ ] All operations have unit tests
- [ ] Test coverage >85%
- [ ] No critical bugs

### Phase 3 Complete
- [ ] iCloud sync functional
- [ ] Conflict resolution working
- [ ] Cross-device tested

### Phase 4 Complete
- [ ] App Store ready
- [ ] Performance optimized
- [ ] Accessibility compliant
- [ ] Documentation complete

---

## Resources Needed

### Frameworks
- Foundation (built-in)
- SwiftUI (built-in)
- SwiftData (built-in)
- Accelerate (for matrix ops)
- Charts (for plotting)
- CloudKit (for sync)

### External Tools
- Xcode 15+
- SF Symbols app
- Instruments (profiling)
- TestFlight (beta testing)

### Knowledge Areas
- Swift 5.9 syntax
- SwiftUI best practices
- Numerical algorithms
- Linear algebra (for matrix ops)
- CloudKit API
- App Store guidelines

---

## Next Immediate Steps

1. **Choose starting point**:
   - Recommended: Constants (easy, 7 operations)
   - Alternative: Unit Conversions (repetitive, 38 operations)

2. **Create first new category**:
   ```bash
   touch MathCLI-iOS/Sources/Core/Operations/Constants/ConstantOperations.swift
   ```

3. **Implement all operations in category**

4. **Register in OperationRegistry**

5. **Create unit tests**

6. **Build and test**

7. **Repeat for next category**

---

## Tips for Success

1. **Start simple**: Constants and conversions are good warm-ups
2. **Follow the pattern**: Use existing operations as templates
3. **Test incrementally**: Test each operation as you write it
4. **Commit often**: Use Git to track progress
5. **Document as you go**: Add code comments
6. **Ask for help**: Review Swift documentation when stuck
7. **Take breaks**: This is a marathon, not a sprint

---

## Conclusion

You now have a complete roadmap to transform this foundation into a full-featured iOS app with 266+ operations. The hardest part (architecture and foundation) is done. The remaining work is largely repetitive implementation following established patterns.

**Estimated total development time**: 3-4 months part-time, or 6-8 weeks full-time.

**Most challenging components**:
1. Matrix operations (requires Accelerate framework knowledge)
2. DataFrame implementation (data structure complexity)
3. Calculus operations (numerical methods)
4. iCloud sync (CloudKit complexity)

**Easiest components**:
1. Constants (just return values)
2. Unit conversions (simple formulas)
3. Geometry (basic math)
4. Variable/function operations (wrappers)

Good luck with the implementation! 🚀
