//
//  CalculusOperations.swift
//  MathCLI
//
//  Calculus operations using numerical methods (12 operations)
//

import Foundation

// Note: These are simplified numerical implementations
// Full symbolic calculus would require a computer algebra system

// MARK: - Derivative (Numerical)

struct DerivativeOperation: MathOperation {
    static var name = "derivative"
    static var arguments = ["function_expr", "x", "h"]
    static var help = "Numerical derivative: derivative expr x [h] (uses central difference)"
    static var category = OperationCategory.calculus

    static func execute(args: [Any]) throws -> OperationResult {
        // This is a placeholder - full implementation would need expression parsing
        // For now, accept a simple power function coefficient and exponent
        let coefficient = try parseDouble(args[0], argumentName: "coefficient")
        let exponent = try parseDouble(args[1], argumentName: "exponent")
        let x = args.count > 2 ? try parseDouble(args[2], argumentName: "x") : 0.0

        // d/dx(ax^n) = n*a*x^(n-1)
        if exponent == 0 {
            return .number(0)
        }

        let result = exponent * coefficient * pow(x, exponent - 1)
        return .number(result)
    }
}

// MARK: - Second Derivative

struct Derivative2Operation: MathOperation {
    static var name = "derivative2"
    static var arguments = ["coefficient", "exponent", "x"]
    static var help = "Second derivative of ax^n: derivative2 a n x"
    static var category = OperationCategory.calculus

    static func execute(args: [Any]) throws -> OperationResult {
        let coefficient = try parseDouble(args[0], argumentName: "coefficient")
        let exponent = try parseDouble(args[1], argumentName: "exponent")
        let x = args.count > 2 ? try parseDouble(args[2], argumentName: "x") : 0.0

        // d²/dx²(ax^n) = n(n-1)*a*x^(n-2)
        if exponent <= 1 {
            return .number(0)
        }

        let result = exponent * (exponent - 1) * coefficient * pow(x, exponent - 2)
        return .number(result)
    }
}

// MARK: - Partial Derivative

struct PartialOperation: MathOperation {
    static var name = "partial"
    static var arguments = ["expr", "var"]
    static var help = "Partial derivative (simplified): partial expr var"
    static var category = OperationCategory.calculus

    static func execute(args: [Any]) throws -> OperationResult {
        // Simplified - same as regular derivative for now
        return try DerivativeOperation.execute(args: args)
    }
}

// MARK: - Gradient

struct GradientOperation: MathOperation {
    static var name = "gradient"
    static var arguments = ["values..."]
    static var help = "Numerical gradient of array: gradient val1 val2 val3 ..."
    static var category = OperationCategory.calculus
    static var isVariadic = true

    static func execute(args: [Any]) throws -> OperationResult {
        var values: [Double] = []
        for arg in args {
            values.append(try parseDouble(arg, argumentName: "value"))
        }

        guard values.count >= 2 else {
            throw OperationError.invalidValue("Gradient requires at least 2 values")
        }

        var gradient: [Double] = []

        for i in 0..<values.count {
            if i == 0 {
                // Forward difference
                gradient.append(values[1] - values[0])
            } else if i == values.count - 1 {
                // Backward difference
                gradient.append(values[i] - values[i - 1])
            } else {
                // Central difference
                gradient.append((values[i + 1] - values[i - 1]) / 2.0)
            }
        }

        return .array(gradient)
    }
}

// MARK: - Divergence

struct DivergenceOperation: MathOperation {
    static var name = "divergence"
    static var arguments = ["x_values", "y_values"]
    static var help = "Divergence (simplified 2D): divergence x_vals y_vals"
    static var category = OperationCategory.calculus

    static func execute(args: [Any]) throws -> OperationResult {
        // Simplified divergence calculation
        let xValues = try parseDoubleArray(args[0], argumentName: "x_values")
        let yValues = try parseDoubleArray(args[1], argumentName: "y_values")

        guard xValues.count == yValues.count else {
            throw OperationError.invalidValue("Arrays must have same length")
        }

        // Sum of gradients
        let xGrad = try GradientOperation.execute(args: xValues.map { $0 as Any })
        let yGrad = try GradientOperation.execute(args: yValues.map { $0 as Any })

        if case .array(let xG) = xGrad, case .array(let yG) = yGrad {
            let div = zip(xG, yG).map { $0 + $1 }
            return .array(div)
        }

        return .number(0)
    }
}

// MARK: - Laplacian

struct LaplacianOperation: MathOperation {
    static var name = "laplacian"
    static var arguments = ["values..."]
    static var help = "Laplacian (second derivative): laplacian val1 val2 val3 ..."
    static var category = OperationCategory.calculus
    static var isVariadic = true

    static func execute(args: [Any]) throws -> OperationResult {
        var values: [Double] = []
        for arg in args {
            values.append(try parseDouble(arg, argumentName: "value"))
        }

        guard values.count >= 3 else {
            throw OperationError.invalidValue("Laplacian requires at least 3 values")
        }

        var laplacian: [Double] = []

        for i in 1..<(values.count - 1) {
            // Second derivative approximation
            let secondDeriv = values[i + 1] - 2 * values[i] + values[i - 1]
            laplacian.append(secondDeriv)
        }

        return .array(laplacian)
    }
}

// MARK: - Integration (Numerical)

struct IntegrateOperation: MathOperation {
    static var name = "integrate"
    static var arguments = ["coefficient", "exponent", "a", "b"]
    static var help = "Integrate ax^n from a to b: integrate a n lower upper"
    static var category = OperationCategory.calculus

    static func execute(args: [Any]) throws -> OperationResult {
        let coefficient = try parseDouble(args[0], argumentName: "coefficient")
        let exponent = try parseDouble(args[1], argumentName: "exponent")
        let a = try parseDouble(args[2], argumentName: "lower_bound")
        let b = try parseDouble(args[3], argumentName: "upper_bound")

        // ∫ax^n dx = a*x^(n+1)/(n+1) + C
        guard exponent != -1 else {
            throw OperationError.invalidValue("Use log for x^-1 integration")
        }

        let newExp = exponent + 1
        let antiderivative = { (x: Double) -> Double in
            coefficient * pow(x, newExp) / newExp
        }

        let result = antiderivative(b) - antiderivative(a)
        return .number(result)
    }
}

// MARK: - Integrate Symbolic

struct IntegrateSymbolicOperation: MathOperation {
    static var name = "integrate_symbolic"
    static var arguments = ["coefficient", "exponent"]
    static var help = "Symbolic integral of ax^n: integrate_symbolic a n"
    static var category = OperationCategory.calculus

    static func execute(args: [Any]) throws -> OperationResult {
        let coefficient = try parseDouble(args[0], argumentName: "coefficient")
        let exponent = try parseDouble(args[1], argumentName: "exponent")

        guard exponent != -1 else {
            return .string("\(coefficient)*log(x) + C")
        }

        let newCoeff = coefficient / (exponent + 1)
        let newExp = exponent + 1

        return .string("\(newCoeff)*x^\(newExp) + C")
    }
}

// MARK: - Limit

struct LimitOperation: MathOperation {
    static var name = "limit"
    static var arguments = ["coefficient", "exponent", "point"]
    static var help = "Limit of ax^n as x approaches point: limit a n point"
    static var category = OperationCategory.calculus

    static func execute(args: [Any]) throws -> OperationResult {
        let coefficient = try parseDouble(args[0], argumentName: "coefficient")
        let exponent = try parseDouble(args[1], argumentName: "exponent")
        let point = try parseDouble(args[2], argumentName: "point")

        // For polynomial, limit is just evaluation
        let result = coefficient * pow(point, exponent)

        return .number(result)
    }
}

// MARK: - Taylor Series

struct TaylorOperation: MathOperation {
    static var name = "taylor"
    static var arguments = ["function", "center", "terms"]
    static var help = "Taylor series (simplified for e^x, sin, cos): taylor func center terms"
    static var category = OperationCategory.calculus

    static func execute(args: [Any]) throws -> OperationResult {
        let funcName = args[0] as? String ?? "exp"
        let center = try parseDouble(args[1], argumentName: "center")
        let terms = try parseInt(args[2], argumentName: "terms")

        guard terms > 0 && terms <= 20 else {
            throw OperationError.invalidValue("Terms must be between 1 and 20")
        }

        var result: Double = 0

        switch funcName.lowercased() {
        case "exp", "e":
            // e^x = Σ x^n/n!
            for n in 0..<terms {
                var factorial: Double = 1
                for i in 1...n {
                    factorial *= Double(i)
                }
                result += pow(center, Double(n)) / factorial
            }

        case "sin":
            // sin(x) = Σ (-1)^n * x^(2n+1) / (2n+1)!
            for n in 0..<terms {
                let power = 2 * n + 1
                var factorial: Double = 1
                for i in 1...power {
                    factorial *= Double(i)
                }
                let sign = n % 2 == 0 ? 1.0 : -1.0
                result += sign * pow(center, Double(power)) / factorial
            }

        case "cos":
            // cos(x) = Σ (-1)^n * x^(2n) / (2n)!
            for n in 0..<terms {
                let power = 2 * n
                var factorial: Double = 1
                for i in 1...power {
                    factorial *= Double(i)
                }
                let sign = n % 2 == 0 ? 1.0 : -1.0
                result += sign * pow(center, Double(power)) / factorial
            }

        default:
            throw OperationError.invalidValue("Unsupported function: \(funcName)")
        }

        return .number(result)
    }
}

// MARK: - Series

struct SeriesOperation: MathOperation {
    static var name = "series"
    static var arguments = ["start", "end", "step"]
    static var help = "Generate arithmetic series: series start end step"
    static var category = OperationCategory.calculus

    static func execute(args: [Any]) throws -> OperationResult {
        let start = try parseDouble(args[0], argumentName: "start")
        let end = try parseDouble(args[1], argumentName: "end")
        let step = try parseDouble(args[2], argumentName: "step")

        guard step != 0 else {
            throw OperationError.divisionByZero
        }

        var series: [Double] = []
        var current = start

        if step > 0 {
            while current <= end {
                series.append(current)
                current += step
                if series.count > 10000 {
                    throw OperationError.invalidValue("Series too large (max 10000 elements)")
                }
            }
        } else {
            while current >= end {
                series.append(current)
                current += step
                if series.count > 10000 {
                    throw OperationError.invalidValue("Series too large (max 10000 elements)")
                }
            }
        }

        return .array(series)
    }
}

// MARK: - Solve ODE (Euler's Method)

struct SolveOdeOperation: MathOperation {
    static var name = "solve_ode"
    static var arguments = ["slope", "y0", "x0", "x_end", "steps"]
    static var help = "Solve ODE using Euler's method (dy/dx = slope): solve_ode slope y0 x0 x_end steps"
    static var category = OperationCategory.calculus

    static func execute(args: [Any]) throws -> OperationResult {
        let slope = try parseDouble(args[0], argumentName: "slope") // Constant slope for simplicity
        let y0 = try parseDouble(args[1], argumentName: "y0")
        let x0 = try parseDouble(args[2], argumentName: "x0")
        let xEnd = try parseDouble(args[3], argumentName: "x_end")
        let steps = try parseInt(args[4], argumentName: "steps")

        guard steps > 0 && steps <= 1000 else {
            throw OperationError.invalidValue("Steps must be between 1 and 1000")
        }

        let h = (xEnd - x0) / Double(steps)
        var y = y0
        var solution: [Double] = [y0]

        for _ in 0..<steps {
            y += h * slope
            solution.append(y)
        }

        return .array(solution)
    }
}
