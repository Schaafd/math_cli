//
//  ControlFlowOperations.swift
//  MathCLI
//
//  Control flow operations (13 operations)
//

import Foundation

// Helper to parse boolean
private func parseBool(_ value: Any) throws -> Bool {
    if let boolValue = value as? Bool {
        return boolValue
    } else if let stringValue = value as? String {
        let lower = stringValue.lowercased()
        if lower == "true" { return true }
        if lower == "false" { return false }
        throw OperationError.invalidArgumentType(
            argument: "value",
            expected: "boolean",
            got: stringValue
        )
    } else if let numValue = value as? Double {
        return numValue != 0
    } else if let intValue = value as? Int {
        return intValue != 0
    }
    throw OperationError.invalidArgumentType(
        argument: "value",
        expected: "boolean",
        got: String(describing: value)
    )
}

// MARK: - Comparison Operations

struct EqOperation: MathOperation {
    static var name = "eq"
    static var arguments = ["a", "b"]
    static var help = "Check if a equals b: eq a b"
    static var category = OperationCategory.controlFlow

    static func execute(args: [Any]) throws -> OperationResult {
        let a = try parseDouble(args[0], argumentName: "a")
        let b = try parseDouble(args[1], argumentName: "b")
        return .boolean(abs(a - b) < 1e-10) // Floating point comparison
    }
}

struct NeqOperation: MathOperation {
    static var name = "neq"
    static var arguments = ["a", "b"]
    static var help = "Check if a not equals b: neq a b"
    static var category = OperationCategory.controlFlow

    static func execute(args: [Any]) throws -> OperationResult {
        let a = try parseDouble(args[0], argumentName: "a")
        let b = try parseDouble(args[1], argumentName: "b")
        return .boolean(abs(a - b) >= 1e-10)
    }
}

struct GtOperation: MathOperation {
    static var name = "gt"
    static var arguments = ["a", "b"]
    static var help = "Check if a greater than b: gt a b"
    static var category = OperationCategory.controlFlow

    static func execute(args: [Any]) throws -> OperationResult {
        let a = try parseDouble(args[0], argumentName: "a")
        let b = try parseDouble(args[1], argumentName: "b")
        return .boolean(a > b)
    }
}

struct GteOperation: MathOperation {
    static var name = "gte"
    static var arguments = ["a", "b"]
    static var help = "Check if a greater than or equal to b: gte a b"
    static var category = OperationCategory.controlFlow

    static func execute(args: [Any]) throws -> OperationResult {
        let a = try parseDouble(args[0], argumentName: "a")
        let b = try parseDouble(args[1], argumentName: "b")
        return .boolean(a >= b)
    }
}

struct LtOperation: MathOperation {
    static var name = "lt"
    static var arguments = ["a", "b"]
    static var help = "Check if a less than b: lt a b"
    static var category = OperationCategory.controlFlow

    static func execute(args: [Any]) throws -> OperationResult {
        let a = try parseDouble(args[0], argumentName: "a")
        let b = try parseDouble(args[1], argumentName: "b")
        return .boolean(a < b)
    }
}

struct LteOperation: MathOperation {
    static var name = "lte"
    static var arguments = ["a", "b"]
    static var help = "Check if a less than or equal to b: lte a b"
    static var category = OperationCategory.controlFlow

    static func execute(args: [Any]) throws -> OperationResult {
        let a = try parseDouble(args[0], argumentName: "a")
        let b = try parseDouble(args[1], argumentName: "b")
        return .boolean(a <= b)
    }
}

// MARK: - Logical Operations

struct AndOperation: MathOperation {
    static var name = "and"
    static var arguments = ["a", "b"]
    static var help = "Logical AND: and a b"
    static var category = OperationCategory.controlFlow

    static func execute(args: [Any]) throws -> OperationResult {
        let a = try parseBool(args[0])
        let b = try parseBool(args[1])
        return .boolean(a && b)
    }
}

struct OrOperation: MathOperation {
    static var name = "or"
    static var arguments = ["a", "b"]
    static var help = "Logical OR: or a b"
    static var category = OperationCategory.controlFlow

    static func execute(args: [Any]) throws -> OperationResult {
        let a = try parseBool(args[0])
        let b = try parseBool(args[1])
        return .boolean(a || b)
    }
}

struct NotOperation: MathOperation {
    static var name = "not"
    static var arguments = ["value"]
    static var help = "Logical NOT: not value"
    static var category = OperationCategory.controlFlow

    static func execute(args: [Any]) throws -> OperationResult {
        let value = try parseBool(args[0])
        return .boolean(!value)
    }
}

// MARK: - Conditional

struct IfOperation: MathOperation {
    static var name = "if"
    static var arguments = ["condition", "then_value", "else_value"]
    static var help = "Conditional (ternary): if condition then_value else_value"
    static var category = OperationCategory.controlFlow

    static func execute(args: [Any]) throws -> OperationResult {
        guard args.count == 3 else {
            throw OperationError.invalidArgumentCount(expected: 3, got: args.count)
        }

        let condition = try parseBool(args[0])

        if condition {
            // Try to parse then_value as number
            if let numValue = try? parseDouble(args[1], argumentName: "then_value") {
                return .number(numValue)
            } else if let strValue = args[1] as? String {
                return .string(strValue)
            } else {
                return .string(String(describing: args[1]))
            }
        } else {
            // Try to parse else_value as number
            if let numValue = try? parseDouble(args[2], argumentName: "else_value") {
                return .number(numValue)
            } else if let strValue = args[2] as? String {
                return .string(strValue)
            } else {
                return .string(String(describing: args[2]))
            }
        }
    }
}

// MARK: - Type Checking

struct IsNumberOperation: MathOperation {
    static var name = "is_number"
    static var arguments = ["value"]
    static var help = "Check if value is a number: is_number value"
    static var category = OperationCategory.controlFlow

    static func execute(args: [Any]) throws -> OperationResult {
        let value = args[0]

        if value is Double || value is Int || value is Float {
            return .boolean(true)
        }

        if let stringValue = value as? String {
            return .boolean(Double(stringValue) != nil)
        }

        return .boolean(false)
    }
}

struct IsStringOperation: MathOperation {
    static var name = "is_string"
    static var arguments = ["value"]
    static var help = "Check if value is a string: is_string value"
    static var category = OperationCategory.controlFlow

    static func execute(args: [Any]) throws -> OperationResult {
        return .boolean(args[0] is String)
    }
}

struct IsBoolOperation: MathOperation {
    static var name = "is_bool"
    static var arguments = ["value"]
    static var help = "Check if value is a boolean: is_bool value"
    static var category = OperationCategory.controlFlow

    static func execute(args: [Any]) throws -> OperationResult {
        if let stringValue = args[0] as? String {
            let lower = stringValue.lowercased()
            return .boolean(lower == "true" || lower == "false")
        }
        return .boolean(args[0] is Bool)
    }
}
