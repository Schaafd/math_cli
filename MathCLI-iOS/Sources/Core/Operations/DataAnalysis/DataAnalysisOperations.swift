//
//  DataAnalysisOperations.swift
//  MathCLI
//
//  Data analysis operations - simplified array-based (12 operations)
//  Full DataFrame implementation can be added later
//

import Foundation

// MARK: - Load Data

struct LoadDataOperation: MathOperation {
    static var name = "load_data"
    static var arguments = ["filepath"]
    static var help = "Load data from CSV file (simplified): load_data filepath"
    static var category = OperationCategory.dataAnalysis

    static func execute(args: [Any]) throws -> OperationResult {
        let filepath = args[0] as? String ?? String(describing: args[0])

        guard let content = try? String(contentsOfFile: filepath, encoding: .utf8) else {
            throw OperationError.fileNotFound(filepath)
        }

        // Parse CSV
        let lines = content.components(separatedBy: .newlines).filter { !$0.isEmpty }
        guard let header = lines.first else {
            throw OperationError.importError("Empty file")
        }

        let columns = header.components(separatedBy: ",").map { $0.trimmingCharacters(in: .whitespaces) }

        // For now, return column names
        return .string("Loaded \(lines.count - 1) rows, \(columns.count) columns: \(columns.joined(separator: ", "))")
    }
}

// MARK: - Describe Data

struct DescribeDataOperation: MathOperation {
    static var name = "describe_data"
    static var arguments = ["values..."]
    static var help = "Statistical summary of data: describe_data val1 val2 val3 ..."
    static var category = OperationCategory.dataAnalysis
    static var isVariadic = true

    static func execute(args: [Any]) throws -> OperationResult {
        var values: [Double] = []
        for arg in args {
            values.append(try parseDouble(arg, argumentName: "value"))
        }

        guard !values.isEmpty else {
            throw OperationError.invalidValue("No data provided")
        }

        let count = values.count
        let sum = values.reduce(0, +)
        let mean = sum / Double(count)
        let sorted = values.sorted()
        let min = sorted.first!
        let max = sorted.last!

        let median = count % 2 == 0 ?
            (sorted[count / 2 - 1] + sorted[count / 2]) / 2 :
            sorted[count / 2]

        let variance = values.map { pow($0 - mean, 2) }.reduce(0, +) / Double(count)
        let stdDev = sqrt(variance)

        let summary = """
        Count: \(count)
        Mean: \(mean)
        Std Dev: \(stdDev)
        Min: \(min)
        25%: \(sorted[count / 4])
        50% (Median): \(median)
        75%: \(sorted[3 * count / 4])
        Max: \(max)
        """

        return .string(summary)
    }
}

// MARK: - Correlation Matrix

struct CorrelationMatrixOperation: MathOperation {
    static var name = "correlation_matrix"
    static var arguments = ["array1", "array2"]
    static var help = "Correlation between two arrays: correlation_matrix arr1 arr2"
    static var category = OperationCategory.dataAnalysis

    static func execute(args: [Any]) throws -> OperationResult {
        let arr1 = try parseDoubleArray(args[0], argumentName: "array1")
        let arr2 = try parseDoubleArray(args[1], argumentName: "array2")

        guard arr1.count == arr2.count else {
            throw OperationError.invalidValue("Arrays must have same length")
        }

        let n = Double(arr1.count)
        let mean1 = arr1.reduce(0, +) / n
        let mean2 = arr2.reduce(0, +) / n

        var covariance: Double = 0
        var variance1: Double = 0
        var variance2: Double = 0

        for i in 0..<arr1.count {
            let diff1 = arr1[i] - mean1
            let diff2 = arr2[i] - mean2
            covariance += diff1 * diff2
            variance1 += diff1 * diff1
            variance2 += diff2 * diff2
        }

        let correlation = covariance / sqrt(variance1 * variance2)
        return .number(correlation)
    }
}

// MARK: - Group By (Simplified)

struct GroupByOperation: MathOperation {
    static var name = "groupby"
    static var arguments = ["values...", "groups..."]
    static var help = "Group and sum values (simplified): groupby val1 val2 ... (groups via count)"
    static var category = OperationCategory.dataAnalysis
    static var isVariadic = true

    static func execute(args: [Any]) throws -> OperationResult {
        var values: [Double] = []
        for arg in args {
            values.append(try parseDouble(arg, argumentName: "value"))
        }

        // Simplified: return sum
        return .number(values.reduce(0, +))
    }
}

// MARK: - Detect Outliers

struct DetectOutliersOperation: MathOperation {
    static var name = "detect_outliers"
    static var arguments = ["values..."]
    static var help = "Detect outliers using IQR method: detect_outliers val1 val2 val3 ..."
    static var category = OperationCategory.dataAnalysis
    static var isVariadic = true

    static func execute(args: [Any]) throws -> OperationResult {
        var values: [Double] = []
        for arg in args {
            values.append(try parseDouble(arg, argumentName: "value"))
        }

        guard values.count >= 4 else {
            throw OperationError.invalidValue("Need at least 4 values")
        }

        let sorted = values.sorted()
        let q1 = sorted[sorted.count / 4]
        let q3 = sorted[3 * sorted.count / 4]
        let iqr = q3 - q1

        let lowerBound = q1 - 1.5 * iqr
        let upperBound = q3 + 1.5 * iqr

        let outliers = values.filter { $0 < lowerBound || $0 > upperBound }

        return .array(outliers)
    }
}

// MARK: - Missing Values

struct MissingValuesOperation: MathOperation {
    static var name = "missing_values"
    static var arguments = ["values..."]
    static var help = "Count missing/zero values: missing_values val1 val2 val3 ..."
    static var category = OperationCategory.dataAnalysis
    static var isVariadic = true

    static func execute(args: [Any]) throws -> OperationResult {
        let missingCount = args.filter { arg in
            if let num = try? parseDouble(arg, argumentName: "value") {
                return num == 0
            }
            return true
        }.count

        return .integer(missingCount)
    }
}

// MARK: - Pivot Table (Simplified)

struct PivotTableOperation: MathOperation {
    static var name = "pivot_table"
    static var arguments = ["values..."]
    static var help = "Pivot table (simplified sum): pivot_table val1 val2 val3 ..."
    static var category = OperationCategory.dataAnalysis
    static var isVariadic = true

    static func execute(args: [Any]) throws -> OperationResult {
        var values: [Double] = []
        for arg in args {
            values.append(try parseDouble(arg, argumentName: "value"))
        }

        return .number(values.reduce(0, +))
    }
}

// MARK: - Rolling Mean

struct RollingMeanOperation: MathOperation {
    static var name = "rolling_mean"
    static var arguments = ["window_size", "values..."]
    static var help = "Calculate rolling mean: rolling_mean window val1 val2 val3 ..."
    static var category = OperationCategory.dataAnalysis
    static var isVariadic = true

    static func execute(args: [Any]) throws -> OperationResult {
        guard args.count >= 2 else {
            throw OperationError.invalidArgumentCount(expected: 2, got: args.count)
        }

        let window = try parseInt(args[0], argumentName: "window_size")
        var values: [Double] = []

        for i in 1..<args.count {
            values.append(try parseDouble(args[i], argumentName: "value"))
        }

        guard window > 0 && window <= values.count else {
            throw OperationError.invalidValue("Invalid window size")
        }

        var rollingMeans: [Double] = []

        for i in 0...(values.count - window) {
            let windowValues = Array(values[i..<(i + window)])
            let mean = windowValues.reduce(0, +) / Double(window)
            rollingMeans.append(mean)
        }

        return .array(rollingMeans)
    }
}

// MARK: - Time Series Analysis (Simplified)

struct TimeSeriesAnalysisOperation: MathOperation {
    static var name = "time_series_analysis"
    static var arguments = ["values..."]
    static var help = "Time series trend: time_series_analysis val1 val2 val3 ..."
    static var category = OperationCategory.dataAnalysis
    static var isVariadic = true

    static func execute(args: [Any]) throws -> OperationResult {
        var values: [Double] = []
        for arg in args {
            values.append(try parseDouble(arg, argumentName: "value"))
        }

        guard values.count >= 2 else {
            throw OperationError.invalidValue("Need at least 2 values")
        }

        // Calculate linear trend
        let n = Double(values.count)
        var sumX: Double = 0
        var sumY: Double = 0
        var sumXY: Double = 0
        var sumX2: Double = 0

        for (i, y) in values.enumerated() {
            let x = Double(i)
            sumX += x
            sumY += y
            sumXY += x * y
            sumX2 += x * x
        }

        let slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX)
        let intercept = (sumY - slope * sumX) / n

        return .string("Trend: y = \(slope)x + \(intercept)")
    }
}

// MARK: - Data Info

struct DataInfoOperation: MathOperation {
    static var name = "data_info"
    static var arguments = ["values..."]
    static var help = "Data information summary: data_info val1 val2 val3 ..."
    static var category = OperationCategory.dataAnalysis
    static var isVariadic = true

    static func execute(args: [Any]) throws -> OperationResult {
        let count = args.count
        var numericCount = 0

        for arg in args {
            if let _ = try? parseDouble(arg, argumentName: "value") {
                numericCount += 1
            }
        }

        return .string("Total: \(count), Numeric: \(numericCount), Non-numeric: \(count - numericCount)")
    }
}

// MARK: - Save Data

struct SaveDataOperation: MathOperation {
    static var name = "save_data"
    static var arguments = ["filepath", "values..."]
    static var help = "Save data to CSV: save_data filepath val1 val2 val3 ..."
    static var category = OperationCategory.dataAnalysis
    static var isVariadic = true

    static func execute(args: [Any]) throws -> OperationResult {
        guard args.count >= 2 else {
            throw OperationError.invalidArgumentCount(expected: 2, got: args.count)
        }

        let filepath = args[0] as? String ?? String(describing: args[0])
        var values: [String] = []

        for i in 1..<args.count {
            values.append(String(describing: args[i]))
        }

        let csv = values.joined(separator: ",")
        try csv.write(toFile: filepath, atomically: true, encoding: .utf8)

        return .string("Data saved to \(filepath)")
    }
}

// MARK: - Unique Values

struct UniqueValuesOperation: MathOperation {
    static var name = "unique_values"
    static var arguments = ["values..."]
    static var help = "Get unique values: unique_values val1 val2 val3 ..."
    static var category = OperationCategory.dataAnalysis
    static var isVariadic = true

    static func execute(args: [Any]) throws -> OperationResult {
        var values: [Double] = []
        for arg in args {
            values.append(try parseDouble(arg, argumentName: "value"))
        }

        let unique = Array(Set(values)).sorted()
        return .array(unique)
    }
}
