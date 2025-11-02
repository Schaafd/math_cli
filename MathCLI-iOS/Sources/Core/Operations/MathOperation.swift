//
//  MathOperation.swift
//  MathCLI
//
//  Core protocol for all mathematical operations
//

import Foundation

/// Category classification for operations
enum OperationCategory: String, CaseIterable, Codable {
    case basicArithmetic = "Basic Arithmetic"
    case trigonometry = "Trigonometry"
    case advancedMath = "Advanced Math"
    case statistics = "Statistics"
    case complexNumbers = "Complex Numbers"
    case matrix = "Matrix Operations"
    case calculus = "Calculus"
    case numberTheory = "Number Theory"
    case combinatorics = "Combinatorics"
    case geometry = "Geometry"
    case constants = "Constants"
    case conversions = "Unit Conversions"
    case variables = "Variables"
    case controlFlow = "Control Flow"
    case userFunctions = "User Functions"
    case scripts = "Scripts"
    case dataAnalysis = "Data Analysis"
    case dataTransform = "Data Transformation"
    case plotting = "Plotting"
    case export = "Export/Integration"
}

/// Result type for operation execution
enum OperationResult: Codable {
    case number(Double)
    case integer(Int)
    case string(String)
    case boolean(Bool)
    case array([Double])
    case matrix([[Double]])
    case complex(real: Double, imaginary: Double)
    case dictionary([String: Double])
    case dataFrame(DataFrame)
    case void

    var description: String {
        switch self {
        case .number(let value):
            return formatNumber(value)
        case .integer(let value):
            return "\(value)"
        case .string(let value):
            return "\"\(value)\""
        case .boolean(let value):
            return value ? "true" : "false"
        case .array(let values):
            return "[\(values.map { formatNumber($0) }.joined(separator: ", "))]"
        case .matrix(let rows):
            let formattedRows = rows.map { row in
                "[\(row.map { formatNumber($0) }.joined(separator: ", "))]"
            }
            return "[\n  \(formattedRows.joined(separator: ",\n  "))\n]"
        case .complex(let real, let imaginary):
            let sign = imaginary >= 0 ? "+" : ""
            return "\(formatNumber(real)) \(sign) \(formatNumber(imaginary))i"
        case .dictionary(let dict):
            let pairs = dict.map { "\"\($0.key)\": \(formatNumber($0.value))" }
            return "{\(pairs.joined(separator: ", "))}"
        case .dataFrame(let df):
            return df.description
        case .void:
            return ""
        }
    }

    private func formatNumber(_ value: Double) -> String {
        if value.truncatingRemainder(dividingBy: 1) == 0 && abs(value) < Double(Int.max) {
            return String(format: "%.0f", value)
        }
        return String(format: "%.6f", value).trimmingCharacters(in: CharacterSet(charactersIn: "0")).trimmingCharacters(in: CharacterSet(charactersIn: "."))
    }
}

/// Error types for operation execution
enum OperationError: LocalizedError {
    case invalidArgumentCount(expected: Int, got: Int)
    case invalidArgumentType(argument: String, expected: String, got: String)
    case invalidValue(String)
    case divisionByZero
    case negativeSquareRoot
    case matrixDimensionMismatch
    case singularMatrix
    case operationNotFound(String)
    case variableNotFound(String)
    case functionNotFound(String)
    case parsingError(String)
    case executionError(String)
    case fileNotFound(String)
    case importError(String)

    var errorDescription: String? {
        switch self {
        case .invalidArgumentCount(let expected, let got):
            return "Invalid argument count: expected \(expected), got \(got)"
        case .invalidArgumentType(let argument, let expected, let got):
            return "Invalid type for '\(argument)': expected \(expected), got \(got)"
        case .invalidValue(let message):
            return "Invalid value: \(message)"
        case .divisionByZero:
            return "Division by zero"
        case .negativeSquareRoot:
            return "Cannot take square root of negative number (use complex operations)"
        case .matrixDimensionMismatch:
            return "Matrix dimension mismatch"
        case .singularMatrix:
            return "Matrix is singular (not invertible)"
        case .operationNotFound(let name):
            return "Operation '\(name)' not found. Use 'help' to see available operations."
        case .variableNotFound(let name):
            return "Variable '\(name)' not found. Use 'vars' to see available variables."
        case .functionNotFound(let name):
            return "Function '\(name)' not found. Use 'funcs' to see available functions."
        case .parsingError(let message):
            return "Parsing error: \(message)"
        case .executionError(let message):
            return "Execution error: \(message)"
        case .fileNotFound(let path):
            return "File not found: \(path)"
        case .importError(let message):
            return "Import error: \(message)"
        }
    }
}

/// Protocol that all mathematical operations must conform to
protocol MathOperation {
    /// Unique identifier for the operation
    static var name: String { get }

    /// List of parameter names
    static var arguments: [String] { get }

    /// Help text describing the operation
    static var help: String { get }

    /// Category classification
    static var category: OperationCategory { get }

    /// Whether the operation accepts variable number of arguments
    static var isVariadic: Bool { get }

    /// Execute the operation with given arguments
    /// - Parameter args: Array of arguments (can be Any type - Double, String, Bool, Array, etc.)
    /// - Returns: Result of the operation
    /// - Throws: OperationError if execution fails
    static func execute(args: [Any]) throws -> OperationResult
}

// Default implementation for non-variadic operations
extension MathOperation {
    static var isVariadic: Bool { false }
}

/// Simplified DataFrame structure for data operations
struct DataFrame: Codable, CustomStringConvertible {
    var columns: [String]
    var data: [[Any]]

    var description: String {
        guard !columns.isEmpty && !data.isEmpty else {
            return "Empty DataFrame"
        }

        var result = "DataFrame (\(data.count) rows × \(columns.count) columns)\n"
        result += columns.joined(separator: " | ") + "\n"
        result += String(repeating: "-", count: columns.count * 15) + "\n"

        for row in data.prefix(10) {
            let rowStr = row.map { "\($0)" }.joined(separator: " | ")
            result += rowStr + "\n"
        }

        if data.count > 10 {
            result += "... \(data.count - 10) more rows"
        }

        return result
    }

    enum CodingKeys: String, CodingKey {
        case columns, data
    }

    init(columns: [String], data: [[Any]]) {
        self.columns = columns
        self.data = data
    }

    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        columns = try container.decode([String].self, forKey: .columns)
        // Simplified decoding - in real implementation would need proper Any decoding
        data = []
    }

    func encode(to encoder: Encoder) throws {
        var container = encoder.container(keyedBy: CodingKeys.self)
        try container.encode(columns, forKey: .columns)
        // Simplified encoding - in real implementation would need proper Any encoding
    }
}
