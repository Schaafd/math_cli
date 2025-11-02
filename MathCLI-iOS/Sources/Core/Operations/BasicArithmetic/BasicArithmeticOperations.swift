//
//  BasicArithmeticOperations.swift
//  MathCLI
//
//  Basic arithmetic operations (14 operations)
//

import Foundation

// MARK: - Add Operation

struct AddOperation: MathOperation {
    static var name: String = "add"
    static var arguments: [String] = ["a", "b"]
    static var help: String = "Add two numbers: add a b"
    static var category: OperationCategory = .basicArithmetic

    static func execute(args: [Any]) throws -> OperationResult {
        guard args.count == 2 else {
            throw OperationError.invalidArgumentCount(expected: 2, got: args.count)
        }

        let a = try parseDouble(args[0], argumentName: "a")
        let b = try parseDouble(args[1], argumentName: "b")

        return .number(a + b)
    }
}

// MARK: - Subtract Operation

struct SubtractOperation: MathOperation {
    static var name: String = "subtract"
    static var arguments: [String] = ["a", "b"]
    static var help: String = "Subtract b from a: subtract a b"
    static var category: OperationCategory = .basicArithmetic

    static func execute(args: [Any]) throws -> OperationResult {
        guard args.count == 2 else {
            throw OperationError.invalidArgumentCount(expected: 2, got: args.count)
        }

        let a = try parseDouble(args[0], argumentName: "a")
        let b = try parseDouble(args[1], argumentName: "b")

        return .number(a - b)
    }
}

// MARK: - Multiply Operation

struct MultiplyOperation: MathOperation {
    static var name: String = "multiply"
    static var arguments: [String] = ["a", "b"]
    static var help: String = "Multiply two numbers: multiply a b"
    static var category: OperationCategory = .basicArithmetic

    static func execute(args: [Any]) throws -> OperationResult {
        guard args.count == 2 else {
            throw OperationError.invalidArgumentCount(expected: 2, got: args.count)
        }

        let a = try parseDouble(args[0], argumentName: "a")
        let b = try parseDouble(args[1], argumentName: "b")

        return .number(a * b)
    }
}

// MARK: - Divide Operation

struct DivideOperation: MathOperation {
    static var name: String = "divide"
    static var arguments: [String] = ["a", "b"]
    static var help: String = "Divide a by b: divide a b"
    static var category: OperationCategory = .basicArithmetic

    static func execute(args: [Any]) throws -> OperationResult {
        guard args.count == 2 else {
            throw OperationError.invalidArgumentCount(expected: 2, got: args.count)
        }

        let a = try parseDouble(args[0], argumentName: "a")
        let b = try parseDouble(args[1], argumentName: "b")

        guard b != 0 else {
            throw OperationError.divisionByZero
        }

        return .number(a / b)
    }
}

// MARK: - Power Operation

struct PowerOperation: MathOperation {
    static var name: String = "power"
    static var arguments: [String] = ["base", "exponent"]
    static var help: String = "Raise base to exponent: power base exponent"
    static var category: OperationCategory = .basicArithmetic

    static func execute(args: [Any]) throws -> OperationResult {
        guard args.count == 2 else {
            throw OperationError.invalidArgumentCount(expected: 2, got: args.count)
        }

        let base = try parseDouble(args[0], argumentName: "base")
        let exponent = try parseDouble(args[1], argumentName: "exponent")

        return .number(pow(base, exponent))
    }
}

// MARK: - Square Root Operation

struct SqrtOperation: MathOperation {
    static var name: String = "sqrt"
    static var arguments: [String] = ["x"]
    static var help: String = "Calculate square root: sqrt x"
    static var category: OperationCategory = .basicArithmetic

    static func execute(args: [Any]) throws -> OperationResult {
        guard args.count == 1 else {
            throw OperationError.invalidArgumentCount(expected: 1, got: args.count)
        }

        let x = try parseDouble(args[0], argumentName: "x")

        guard x >= 0 else {
            throw OperationError.negativeSquareRoot
        }

        return .number(sqrt(x))
    }
}

// MARK: - Factorial Operation

struct FactorialOperation: MathOperation {
    static var name: String = "factorial"
    static var arguments: [String] = ["n"]
    static var help: String = "Calculate factorial: factorial n"
    static var category: OperationCategory = .basicArithmetic

    static func execute(args: [Any]) throws -> OperationResult {
        guard args.count == 1 else {
            throw OperationError.invalidArgumentCount(expected: 1, got: args.count)
        }

        let n = try parseInt(args[0], argumentName: "n")

        guard n >= 0 else {
            throw OperationError.invalidValue("Factorial requires non-negative integer")
        }

        guard n <= 20 else {
            throw OperationError.invalidValue("Factorial input too large (max 20)")
        }

        func fact(_ n: Int) -> Int {
            return n <= 1 ? 1 : n * fact(n - 1)
        }

        return .integer(fact(n))
    }
}

// MARK: - Logarithm Operation

struct LogOperation: MathOperation {
    static var name: String = "log"
    static var arguments: [String] = ["x", "base"]
    static var help: String = "Calculate logarithm: log x [base] (default base=10)"
    static var category: OperationCategory = .basicArithmetic

    static func execute(args: [Any]) throws -> OperationResult {
        guard args.count >= 1 && args.count <= 2 else {
            throw OperationError.invalidArgumentCount(expected: 2, got: args.count)
        }

        let x = try parseDouble(args[0], argumentName: "x")
        let base = args.count == 2 ? try parseDouble(args[1], argumentName: "base") : 10.0

        guard x > 0 else {
            throw OperationError.invalidValue("Logarithm requires positive number")
        }

        guard base > 0 && base != 1 else {
            throw OperationError.invalidValue("Logarithm base must be positive and not equal to 1")
        }

        if base == 10 {
            return .number(log10(x))
        } else if base == 2 {
            return .number(log2(x))
        } else if base == .e {
            return .number(log(x))
        } else {
            return .number(log(x) / log(base))
        }
    }
}

// MARK: - Sine Operation

struct SinOperation: MathOperation {
    static var name: String = "sin"
    static var arguments: [String] = ["x"]
    static var help: String = "Calculate sine (input in radians): sin x"
    static var category: OperationCategory = .basicArithmetic

    static func execute(args: [Any]) throws -> OperationResult {
        guard args.count == 1 else {
            throw OperationError.invalidArgumentCount(expected: 1, got: args.count)
        }

        let x = try parseDouble(args[0], argumentName: "x")
        return .number(sin(x))
    }
}

// MARK: - Cosine Operation

struct CosOperation: MathOperation {
    static var name: String = "cos"
    static var arguments: [String] = ["x"]
    static var help: String = "Calculate cosine (input in radians): cos x"
    static var category: OperationCategory = .basicArithmetic

    static func execute(args: [Any]) throws -> OperationResult {
        guard args.count == 1 else {
            throw OperationError.invalidArgumentCount(expected: 1, got: args.count)
        }

        let x = try parseDouble(args[0], argumentName: "x")
        return .number(cos(x))
    }
}

// MARK: - Tangent Operation

struct TanOperation: MathOperation {
    static var name: String = "tan"
    static var arguments: [String] = ["x"]
    static var help: String = "Calculate tangent (input in radians): tan x"
    static var category: OperationCategory = .basicArithmetic

    static func execute(args: [Any]) throws -> OperationResult {
        guard args.count == 1 else {
            throw OperationError.invalidArgumentCount(expected: 1, got: args.count)
        }

        let x = try parseDouble(args[0], argumentName: "x")
        return .number(tan(x))
    }
}

// MARK: - To Radians Operation

struct ToRadiansOperation: MathOperation {
    static var name: String = "to_radians"
    static var arguments: [String] = ["degrees"]
    static var help: String = "Convert degrees to radians: to_radians degrees"
    static var category: OperationCategory = .basicArithmetic

    static func execute(args: [Any]) throws -> OperationResult {
        guard args.count == 1 else {
            throw OperationError.invalidArgumentCount(expected: 1, got: args.count)
        }

        let degrees = try parseDouble(args[0], argumentName: "degrees")
        return .number(degrees * .pi / 180.0)
    }
}

// MARK: - To Degrees Operation

struct ToDegreesOperation: MathOperation {
    static var name: String = "to_degrees"
    static var arguments: [String] = ["radians"]
    static var help: String = "Convert radians to degrees: to_degrees radians"
    static var category: OperationCategory = .basicArithmetic

    static func execute(args: [Any]) throws -> OperationResult {
        guard args.count == 1 else {
            throw OperationError.invalidArgumentCount(expected: 1, got: args.count)
        }

        let radians = try parseDouble(args[0], argumentName: "radians")
        return .number(radians * 180.0 / .pi)
    }
}

// MARK: - Absolute Value Operation

struct AbsOperation: MathOperation {
    static var name: String = "abs"
    static var arguments: [String] = ["x"]
    static var help: String = "Calculate absolute value: abs x"
    static var category: OperationCategory = .basicArithmetic

    static func execute(args: [Any]) throws -> OperationResult {
        guard args.count == 1 else {
            throw OperationError.invalidArgumentCount(expected: 1, got: args.count)
        }

        let x = try parseDouble(args[0], argumentName: "x")
        return .number(abs(x))
    }
}

// MARK: - Helper Functions

private func parseDouble(_ value: Any, argumentName: String) throws -> Double {
    if let doubleValue = value as? Double {
        return doubleValue
    } else if let intValue = value as? Int {
        return Double(intValue)
    } else if let stringValue = value as? String {
        guard let doubleValue = Double(stringValue) else {
            throw OperationError.invalidArgumentType(
                argument: argumentName,
                expected: "number",
                got: stringValue
            )
        }
        return doubleValue
    } else {
        throw OperationError.invalidArgumentType(
            argument: argumentName,
            expected: "number",
            got: String(describing: value)
        )
    }
}

private func parseInt(_ value: Any, argumentName: String) throws -> Int {
    if let intValue = value as? Int {
        return intValue
    } else if let doubleValue = value as? Double {
        return Int(doubleValue)
    } else if let stringValue = value as? String {
        guard let intValue = Int(stringValue) else {
            throw OperationError.invalidArgumentType(
                argument: argumentName,
                expected: "integer",
                got: stringValue
            )
        }
        return intValue
    } else {
        throw OperationError.invalidArgumentType(
            argument: argumentName,
            expected: "integer",
            got: String(describing: value)
        )
    }
}

// Make helper functions available globally for other operation files
extension MathOperation {
    static func parseDouble(_ value: Any, argumentName: String) throws -> Double {
        if let doubleValue = value as? Double {
            return doubleValue
        } else if let intValue = value as? Int {
            return Double(intValue)
        } else if let stringValue = value as? String {
            guard let doubleValue = Double(stringValue) else {
                throw OperationError.invalidArgumentType(
                    argument: argumentName,
                    expected: "number",
                    got: stringValue
                )
            }
            return doubleValue
        } else {
            throw OperationError.invalidArgumentType(
                argument: argumentName,
                expected: "number",
                got: String(describing: value)
            )
        }
    }

    static func parseInt(_ value: Any, argumentName: String) throws -> Int {
        if let intValue = value as? Int {
            return intValue
        } else if let doubleValue = value as? Double {
            return Int(doubleValue)
        } else if let stringValue = value as? String {
            guard let intValue = Int(stringValue) else {
                throw OperationError.invalidArgumentType(
                    argument: argumentName,
                    expected: "integer",
                    got: stringValue
                )
            }
            return intValue
        } else {
            throw OperationError.invalidArgumentType(
                argument: argumentName,
                expected: "integer",
                got: String(describing: value)
            )
        }
    }

    static func parseDoubleArray(_ value: Any, argumentName: String) throws -> [Double] {
        if let array = value as? [Double] {
            return array
        } else if let stringValue = value as? String {
            let components = stringValue.components(separatedBy: ",")
            return try components.map { component in
                guard let doubleValue = Double(component.trimmingCharacters(in: .whitespaces)) else {
                    throw OperationError.invalidArgumentType(
                        argument: argumentName,
                        expected: "array of numbers",
                        got: stringValue
                    )
                }
                return doubleValue
            }
        } else {
            throw OperationError.invalidArgumentType(
                argument: argumentName,
                expected: "array",
                got: String(describing: value)
            )
        }
    }
}
