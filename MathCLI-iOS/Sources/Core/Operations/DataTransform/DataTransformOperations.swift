//
//  DataTransformOperations.swift
//  MathCLI
//
//  Data transformation operations - simplified array-based (11 operations)
//

import Foundation

// MARK: - Filter Data

struct FilterDataOperation: MathOperation {
    static var name = "filter_data"
    static var arguments = ["threshold", "values..."]
    static var help = "Filter values greater than threshold: filter_data threshold val1 val2 ..."
    static var category = OperationCategory.dataTransform
    static var isVariadic = true

    static func execute(args: [Any]) throws -> OperationResult {
        guard args.count >= 2 else {
            throw OperationError.invalidArgumentCount(expected: 2, got: args.count)
        }

        let threshold = try parseDouble(args[0], argumentName: "threshold")
        var values: [Double] = []

        for i in 1..<args.count {
            values.append(try parseDouble(args[i], argumentName: "value"))
        }

        let filtered = values.filter { $0 > threshold }
        return .array(filtered)
    }
}

// MARK: - Normalize Data

struct NormalizeDataOperation: MathOperation {
    static var name = "normalize_data"
    static var arguments = ["values..."]
    static var help = "Normalize to [0,1] range: normalize_data val1 val2 val3 ..."
    static var category = OperationCategory.dataTransform
    static var isVariadic = true

    static func execute(args: [Any]) throws -> OperationResult {
        var values: [Double] = []
        for arg in args {
            values.append(try parseDouble(arg, argumentName: "value"))
        }

        guard !values.isEmpty else {
            throw OperationError.invalidValue("No data provided")
        }

        let min = values.min()!
        let max = values.max()!

        guard max != min else {
            return .array(Array(repeating: 0.5, count: values.count))
        }

        let normalized = values.map { ($0 - min) / (max - min) }
        return .array(normalized)
    }
}

// MARK: - Sort Data

struct SortDataOperation: MathOperation {
    static var name = "sort_data"
    static var arguments = ["ascending", "values..."]
    static var help = "Sort data: sort_data ascending val1 val2 val3 ..."
    static var category = OperationCategory.dataTransform
    static var isVariadic = true

    static func execute(args: [Any]) throws -> OperationResult {
        guard args.count >= 2 else {
            throw OperationError.invalidArgumentCount(expected: 2, got: args.count)
        }

        let ascendingStr = args[0] as? String ?? "true"
        let ascending = ascendingStr.lowercased() == "true"

        var values: [Double] = []
        for i in 1..<args.count {
            values.append(try parseDouble(args[i], argumentName: "value"))
        }

        let sorted = ascending ? values.sorted() : values.sorted(by: >)
        return .array(sorted)
    }
}

// MARK: - Aggregate Data

struct AggregateDataOperation: MathOperation {
    static var name = "aggregate_data"
    static var arguments = ["function", "values..."]
    static var help = "Aggregate data (sum/mean/max/min): aggregate_data func val1 val2 ..."
    static var category = OperationCategory.dataTransform
    static var isVariadic = true

    static func execute(args: [Any]) throws -> OperationResult {
        guard args.count >= 2 else {
            throw OperationError.invalidArgumentCount(expected: 2, got: args.count)
        }

        let function = (args[0] as? String ?? "sum").lowercased()
        var values: [Double] = []

        for i in 1..<args.count {
            values.append(try parseDouble(args[i], argumentName: "value"))
        }

        guard !values.isEmpty else {
            throw OperationError.invalidValue("No data provided")
        }

        switch function {
        case "sum":
            return .number(values.reduce(0, +))
        case "mean", "avg", "average":
            return .number(values.reduce(0, +) / Double(values.count))
        case "max":
            return .number(values.max()!)
        case "min":
            return .number(values.min()!)
        case "count":
            return .integer(values.count)
        default:
            throw OperationError.invalidValue("Unknown function: \(function)")
        }
    }
}

// MARK: - Fill Nulls

struct FillNullsOperation: MathOperation {
    static var name = "fill_nulls"
    static var arguments = ["fill_value", "values..."]
    static var help = "Replace zeros with value: fill_nulls fill_value val1 val2 ..."
    static var category = OperationCategory.dataTransform
    static var isVariadic = true

    static func execute(args: [Any]) throws -> OperationResult {
        guard args.count >= 2 else {
            throw OperationError.invalidArgumentCount(expected: 2, got: args.count)
        }

        let fillValue = try parseDouble(args[0], argumentName: "fill_value")
        var values: [Double] = []

        for i in 1..<args.count {
            let val = try parseDouble(args[i], argumentName: "value")
            values.append(val == 0 ? fillValue : val)
        }

        return .array(values)
    }
}

// MARK: - Drop Nulls

struct DropNullsOperation: MathOperation {
    static var name = "drop_nulls"
    static var arguments = ["values..."]
    static var help = "Remove zero values: drop_nulls val1 val2 val3 ..."
    static var category = OperationCategory.dataTransform
    static var isVariadic = true

    static func execute(args: [Any]) throws -> OperationResult {
        var values: [Double] = []
        for arg in args {
            let val = try parseDouble(arg, argumentName: "value")
            if val != 0 {
                values.append(val)
            }
        }

        return .array(values)
    }
}

// MARK: - Merge Data

struct MergeDataOperation: MathOperation {
    static var name = "merge_data"
    static var arguments = ["array1...", "array2..."]
    static var help = "Merge two arrays: merge_data (pass all values)"
    static var category = OperationCategory.dataTransform
    static var isVariadic = true

    static func execute(args: [Any]) throws -> OperationResult {
        var values: [Double] = []
        for arg in args {
            values.append(try parseDouble(arg, argumentName: "value"))
        }

        return .array(values)
    }
}

// MARK: - Sample Data

struct SampleDataOperation: MathOperation {
    static var name = "sample_data"
    static var arguments = ["n", "values..."]
    static var help = "Random sample of n values: sample_data n val1 val2 val3 ..."
    static var category = OperationCategory.dataTransform
    static var isVariadic = true

    static func execute(args: [Any]) throws -> OperationResult {
        guard args.count >= 2 else {
            throw OperationError.invalidArgumentCount(expected: 2, got: args.count)
        }

        let n = try parseInt(args[0], argumentName: "n")
        var values: [Double] = []

        for i in 1..<args.count {
            values.append(try parseDouble(args[i], argumentName: "value"))
        }

        guard n > 0 && n <= values.count else {
            throw OperationError.invalidValue("Sample size must be between 1 and \(values.count)")
        }

        let sampled = values.shuffled().prefix(n)
        return .array(Array(sampled))
    }
}

// MARK: - Add Column (Simplified)

struct AddColumnOperation: MathOperation {
    static var name = "add_column"
    static var arguments = ["value", "values..."]
    static var help = "Add constant to all values: add_column constant val1 val2 ..."
    static var category = OperationCategory.dataTransform
    static var isVariadic = true

    static func execute(args: [Any]) throws -> OperationResult {
        guard args.count >= 2 else {
            throw OperationError.invalidArgumentCount(expected: 2, got: args.count)
        }

        let constant = try parseDouble(args[0], argumentName: "constant")
        var values: [Double] = []

        for i in 1..<args.count {
            let val = try parseDouble(args[i], argumentName: "value")
            values.append(val + constant)
        }

        return .array(values)
    }
}

// MARK: - Drop Column (Simplified)

struct DropColumnOperation: MathOperation {
    static var name = "drop_column"
    static var arguments = ["index", "values..."]
    static var help = "Drop value at index: drop_column index val1 val2 val3 ..."
    static var category = OperationCategory.dataTransform
    static var isVariadic = true

    static func execute(args: [Any]) throws -> OperationResult {
        guard args.count >= 2 else {
            throw OperationError.invalidArgumentCount(expected: 2, got: args.count)
        }

        let index = try parseInt(args[0], argumentName: "index")
        var values: [Double] = []

        for i in 1..<args.count {
            values.append(try parseDouble(args[i], argumentName: "value"))
        }

        guard index >= 0 && index < values.count else {
            throw OperationError.invalidValue("Index out of range")
        }

        values.remove(at: index)
        return .array(values)
    }
}

// MARK: - Rename Column (Simplified)

struct RenameColumnOperation: MathOperation {
    static var name = "rename_column"
    static var arguments = ["old_name", "new_name"]
    static var help = "Rename column (placeholder): rename_column old_name new_name"
    static var category = OperationCategory.dataTransform

    static func execute(args: [Any]) throws -> OperationResult {
        guard args.count == 2 else {
            throw OperationError.invalidArgumentCount(expected: 2, got: args.count)
        }

        let oldName = args[0] as? String ?? String(describing: args[0])
        let newName = args[1] as? String ?? String(describing: args[1])

        return .string("Renamed '\(oldName)' to '\(newName)'")
    }
}
