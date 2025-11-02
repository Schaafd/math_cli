//
//  AdvancedMathOperations.swift
//  MathCLI
//
//  Advanced math operations (8 operations)
//

import Foundation

// MARK: - Ceil

struct CeilOperation: MathOperation {
    static var name: String = "ceil"
    static var arguments: [String] = ["x"]
    static var help: String = "Round up to nearest integer: ceil x"
    static var category: OperationCategory = .advancedMath

    static func execute(args: [Any]) throws -> OperationResult {
        let x = try parseDouble(args[0], argumentName: "x")
        return .number(ceil(x))
    }
}

// MARK: - Floor

struct FloorOperation: MathOperation {
    static var name: String = "floor"
    static var arguments: [String] = ["x"]
    static var help: String = "Round down to nearest integer: floor x"
    static var category: OperationCategory = .advancedMath

    static func execute(args: [Any]) throws -> OperationResult {
        let x = try parseDouble(args[0], argumentName: "x")
        return .number(floor(x))
    }
}

// MARK: - Round

struct RoundOperation: MathOperation {
    static var name: String = "round"
    static var arguments: [String] = ["x", "decimals"]
    static var help: String = "Round to n decimal places: round x [decimals]"
    static var category: OperationCategory = .advancedMath

    static func execute(args: [Any]) throws -> OperationResult {
        let x = try parseDouble(args[0], argumentName: "x")
        let decimals = args.count > 1 ? try parseInt(args[1], argumentName: "decimals") : 0

        let multiplier = pow(10.0, Double(decimals))
        return .number(Darwin.round(x * multiplier) / multiplier)
    }
}

// MARK: - Truncate

struct TruncOperation: MathOperation {
    static var name: String = "trunc"
    static var arguments: [String] = ["x"]
    static var help: String = "Truncate to integer (remove decimal part): trunc x"
    static var category: OperationCategory = .advancedMath

    static func execute(args: [Any]) throws -> OperationResult {
        let x = try parseDouble(args[0], argumentName: "x")
        return .number(trunc(x))
    }
}

// MARK: - GCD (Greatest Common Divisor)

struct GcdOperation: MathOperation {
    static var name: String = "gcd"
    static var arguments: [String] = ["a", "b"]
    static var help: String = "Calculate greatest common divisor: gcd a b"
    static var category: OperationCategory = .advancedMath

    static func execute(args: [Any]) throws -> OperationResult {
        let a = try parseInt(args[0], argumentName: "a")
        let b = try parseInt(args[1], argumentName: "b")

        func gcdFunc(_ a: Int, _ b: Int) -> Int {
            return b == 0 ? abs(a) : gcdFunc(b, a % b)
        }

        return .integer(gcdFunc(a, b))
    }
}

// MARK: - LCM (Least Common Multiple)

struct LcmOperation: MathOperation {
    static var name: String = "lcm"
    static var arguments: [String] = ["a", "b"]
    static var help: String = "Calculate least common multiple: lcm a b"
    static var category: OperationCategory = .advancedMath

    static func execute(args: [Any]) throws -> OperationResult {
        let a = try parseInt(args[0], argumentName: "a")
        let b = try parseInt(args[1], argumentName: "b")

        func gcdFunc(_ a: Int, _ b: Int) -> Int {
            return b == 0 ? abs(a) : gcdFunc(b, a % b)
        }

        guard a != 0 && b != 0 else {
            return .integer(0)
        }

        return .integer(abs(a * b) / gcdFunc(a, b))
    }
}

// MARK: - Modulo

struct ModOperation: MathOperation {
    static var name: String = "mod"
    static var arguments: [String] = ["a", "b"]
    static var help: String = "Calculate modulo (remainder): mod a b"
    static var category: OperationCategory = .advancedMath

    static func execute(args: [Any]) throws -> OperationResult {
        let a = try parseDouble(args[0], argumentName: "a")
        let b = try parseDouble(args[1], argumentName: "b")

        guard b != 0 else {
            throw OperationError.divisionByZero
        }

        return .number(a.truncatingRemainder(dividingBy: b))
    }
}

// MARK: - Exponential

struct ExpOperation: MathOperation {
    static var name: String = "exp"
    static var arguments: [String] = ["x"]
    static var help: String = "Calculate e^x (exponential): exp x"
    static var category: OperationCategory = .advancedMath

    static func execute(args: [Any]) throws -> OperationResult {
        let x = try parseDouble(args[0], argumentName: "x")
        return .number(exp(x))
    }
}
