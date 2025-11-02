//
//  StatisticsOperations.swift
//  MathCLI
//
//  Statistics operations (15 operations - all variadic)
//

import Foundation

// MARK: - Mean (Average)

struct MeanOperation: MathOperation {
    static var name: String = "mean"
    static var arguments: [String] = ["values..."]
    static var help: String = "Calculate arithmetic mean: mean value1 value2 ..."
    static var category: OperationCategory = .statistics
    static var isVariadic: Bool = true

    static func execute(args: [Any]) throws -> OperationResult {
        let values = try parseVariadicDoubles(args)
        guard !values.isEmpty else {
            throw OperationError.invalidValue("Mean requires at least one value")
        }
        return .number(values.reduce(0, +) / Double(values.count))
    }
}

// MARK: - Median

struct MedianOperation: MathOperation {
    static var name: String = "median"
    static var arguments: [String] = ["values..."]
    static var help: String = "Calculate median: median value1 value2 ..."
    static var category: OperationCategory = .statistics
    static var isVariadic: Bool = true

    static func execute(args: [Any]) throws -> OperationResult {
        var values = try parseVariadicDoubles(args)
        guard !values.isEmpty else {
            throw OperationError.invalidValue("Median requires at least one value")
        }

        values.sort()
        let count = values.count

        if count % 2 == 0 {
            return .number((values[count / 2 - 1] + values[count / 2]) / 2.0)
        } else {
            return .number(values[count / 2])
        }
    }
}

// MARK: - Mode

struct ModeOperation: MathOperation {
    static var name: String = "mode"
    static var arguments: [String] = ["values..."]
    static var help: String = "Find most frequent value: mode value1 value2 ..."
    static var category: OperationCategory = .statistics
    static var isVariadic: Bool = true

    static func execute(args: [Any]) throws -> OperationResult {
        let values = try parseVariadicDoubles(args)
        guard !values.isEmpty else {
            throw OperationError.invalidValue("Mode requires at least one value")
        }

        var frequencies: [Double: Int] = [:]
        for value in values {
            frequencies[value, default: 0] += 1
        }

        let maxFrequency = frequencies.values.max() ?? 0
        let modes = frequencies.filter { $0.value == maxFrequency }.keys

        return .number(modes.first ?? 0)
    }
}

// MARK: - Geometric Mean

struct GeometricMeanOperation: MathOperation {
    static var name: String = "geometric_mean"
    static var arguments: [String] = ["values..."]
    static var help: String = "Calculate geometric mean: geometric_mean value1 value2 ..."
    static var category: OperationCategory = .statistics
    static var isVariadic: Bool = true

    static func execute(args: [Any]) throws -> OperationResult {
        let values = try parseVariadicDoubles(args)
        guard !values.isEmpty else {
            throw OperationError.invalidValue("Geometric mean requires at least one value")
        }

        let product = values.reduce(1.0, *)
        return .number(pow(abs(product), 1.0 / Double(values.count)))
    }
}

// MARK: - Harmonic Mean

struct HarmonicMeanOperation: MathOperation {
    static var name: String = "harmonic_mean"
    static var arguments: [String] = ["values..."]
    static var help: String = "Calculate harmonic mean: harmonic_mean value1 value2 ..."
    static var category: OperationCategory = .statistics
    static var isVariadic: Bool = true

    static func execute(args: [Any]) throws -> OperationResult {
        let values = try parseVariadicDoubles(args)
        guard !values.isEmpty else {
            throw OperationError.invalidValue("Harmonic mean requires at least one value")
        }

        let reciprocalSum = values.reduce(0.0) { $0 + (1.0 / $1) }
        return .number(Double(values.count) / reciprocalSum)
    }
}

// MARK: - Variance

struct VarianceOperation: MathOperation {
    static var name: String = "variance"
    static var arguments: [String] = ["values..."]
    static var help: String = "Calculate sample variance: variance value1 value2 ..."
    static var category: OperationCategory = .statistics
    static var isVariadic: Bool = true

    static func execute(args: [Any]) throws -> OperationResult {
        let values = try parseVariadicDoubles(args)
        guard values.count >= 2 else {
            throw OperationError.invalidValue("Variance requires at least two values")
        }

        let mean = values.reduce(0, +) / Double(values.count)
        let squaredDiffs = values.map { pow($0 - mean, 2) }
        return .number(squaredDiffs.reduce(0, +) / Double(values.count - 1))
    }
}

// MARK: - Population Variance

struct PopVarianceOperation: MathOperation {
    static var name: String = "pop_variance"
    static var arguments: [String] = ["values..."]
    static var help: String = "Calculate population variance: pop_variance value1 value2 ..."
    static var category: OperationCategory = .statistics
    static var isVariadic: Bool = true

    static func execute(args: [Any]) throws -> OperationResult {
        let values = try parseVariadicDoubles(args)
        guard !values.isEmpty else {
            throw OperationError.invalidValue("Population variance requires at least one value")
        }

        let mean = values.reduce(0, +) / Double(values.count)
        let squaredDiffs = values.map { pow($0 - mean, 2) }
        return .number(squaredDiffs.reduce(0, +) / Double(values.count))
    }
}

// MARK: - Standard Deviation

struct StdDevOperation: MathOperation {
    static var name: String = "std_dev"
    static var arguments: [String] = ["values..."]
    static var help: String = "Calculate sample standard deviation: std_dev value1 value2 ..."
    static var category: OperationCategory = .statistics
    static var isVariadic: Bool = true

    static func execute(args: [Any]) throws -> OperationResult {
        let varianceResult = try VarianceOperation.execute(args: args)
        if case .number(let variance) = varianceResult {
            return .number(sqrt(variance))
        }
        throw OperationError.executionError("Failed to calculate standard deviation")
    }
}

// MARK: - Population Standard Deviation

struct PopStdDevOperation: MathOperation {
    static var name: String = "pop_std_dev"
    static var arguments: [String] = ["values..."]
    static var help: String = "Calculate population standard deviation: pop_std_dev value1 value2 ..."
    static var category: OperationCategory = .statistics
    static var isVariadic: Bool = true

    static func execute(args: [Any]) throws -> OperationResult {
        let varianceResult = try PopVarianceOperation.execute(args: args)
        if case .number(let variance) = varianceResult {
            return .number(sqrt(variance))
        }
        throw OperationError.executionError("Failed to calculate population standard deviation")
    }
}

// MARK: - Range

struct RangeOperation: MathOperation {
    static var name: String = "range"
    static var arguments: [String] = ["values..."]
    static var help: String = "Calculate range (max - min): range value1 value2 ..."
    static var category: OperationCategory = .statistics
    static var isVariadic: Bool = true

    static func execute(args: [Any]) throws -> OperationResult {
        let values = try parseVariadicDoubles(args)
        guard !values.isEmpty else {
            throw OperationError.invalidValue("Range requires at least one value")
        }

        let min = values.min() ?? 0
        let max = values.max() ?? 0
        return .number(max - min)
    }
}

// MARK: - Min

struct MinOperation: MathOperation {
    static var name: String = "min"
    static var arguments: [String] = ["values..."]
    static var help: String = "Find minimum value: min value1 value2 ..."
    static var category: OperationCategory = .statistics
    static var isVariadic: Bool = true

    static func execute(args: [Any]) throws -> OperationResult {
        let values = try parseVariadicDoubles(args)
        guard !values.isEmpty else {
            throw OperationError.invalidValue("Min requires at least one value")
        }

        return .number(values.min() ?? 0)
    }
}

// MARK: - Max

struct MaxOperation: MathOperation {
    static var name: String = "min"
    static var arguments: [String] = ["values..."]
    static var help: String = "Find maximum value: max value1 value2 ..."
    static var category: OperationCategory = .statistics
    static var isVariadic: Bool = true

    static func execute(args: [Any]) throws -> OperationResult {
        let values = try parseVariadicDoubles(args)
        guard !values.isEmpty else {
            throw OperationError.invalidValue("Max requires at least one value")
        }

        return .number(values.max() ?? 0)
    }
}

// MARK: - Sum

struct SumOperation: MathOperation {
    static var name: String = "sum"
    static var arguments: [String] = ["values..."]
    static var help: String = "Calculate sum of values: sum value1 value2 ..."
    static var category: OperationCategory = .statistics
    static var isVariadic: Bool = true

    static func execute(args: [Any]) throws -> OperationResult {
        let values = try parseVariadicDoubles(args)
        return .number(values.reduce(0, +))
    }
}

// MARK: - Product

struct ProductOperation: MathOperation {
    static var name: String = "product"
    static var arguments: [String] = ["values..."]
    static var help: String = "Calculate product of values: product value1 value2 ..."
    static var category: OperationCategory = .statistics
    static var isVariadic: Bool = true

    static func execute(args: [Any]) throws -> OperationResult {
        let values = try parseVariadicDoubles(args)
        return .number(values.reduce(1, *))
    }
}

// MARK: - Count

struct CountOperation: MathOperation {
    static var name: String = "count"
    static var arguments: [String] = ["values..."]
    static var help: String = "Count number of values: count value1 value2 ..."
    static var category: OperationCategory = .statistics
    static var isVariadic: Bool = true

    static func execute(args: [Any]) throws -> OperationResult {
        return .integer(args.count)
    }
}

// MARK: - Helper Function

private func parseVariadicDoubles(_ args: [Any]) throws -> [Double] {
    var values: [Double] = []

    for (index, arg) in args.enumerated() {
        let value = try MathOperation.parseDouble(arg, argumentName: "value\(index + 1)")
        values.append(value)
    }

    return values
}
