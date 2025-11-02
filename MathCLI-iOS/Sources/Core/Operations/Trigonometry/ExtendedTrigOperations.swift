//
//  ExtendedTrigOperations.swift
//  MathCLI
//
//  Extended trigonometry operations (10 operations)
//

import Foundation

// MARK: - Arc Sine

struct AsinOperation: MathOperation {
    static var name: String = "asin"
    static var arguments: [String] = ["x"]
    static var help: String = "Calculate arcsine (returns radians): asin x"
    static var category: OperationCategory = .trigonometry

    static func execute(args: [Any]) throws -> OperationResult {
        let x = try parseDouble(args[0], argumentName: "x")
        guard x >= -1 && x <= 1 else {
            throw OperationError.invalidValue("asin domain is [-1, 1]")
        }
        return .number(asin(x))
    }
}

// MARK: - Arc Cosine

struct AcosOperation: MathOperation {
    static var name: String = "acos"
    static var arguments: [String] = ["x"]
    static var help: String = "Calculate arccosine (returns radians): acos x"
    static var category: OperationCategory = .trigonometry

    static func execute(args: [Any]) throws -> OperationResult {
        let x = try parseDouble(args[0], argumentName: "x")
        guard x >= -1 && x <= 1 else {
            throw OperationError.invalidValue("acos domain is [-1, 1]")
        }
        return .number(acos(x))
    }
}

// MARK: - Arc Tangent

struct AtanOperation: MathOperation {
    static var name: String = "atan"
    static var arguments: [String] = ["x"]
    static var help: String = "Calculate arctangent (returns radians): atan x"
    static var category: OperationCategory = .trigonometry

    static func execute(args: [Any]) throws -> OperationResult {
        let x = try parseDouble(args[0], argumentName: "x")
        return .number(atan(x))
    }
}

// MARK: - Arc Tangent 2

struct Atan2Operation: MathOperation {
    static var name: String = "atan2"
    static var arguments: [String] = ["y", "x"]
    static var help: String = "Calculate two-argument arctangent: atan2 y x"
    static var category: OperationCategory = .trigonometry

    static func execute(args: [Any]) throws -> OperationResult {
        let y = try parseDouble(args[0], argumentName: "y")
        let x = try parseDouble(args[1], argumentName: "x")
        return .number(atan2(y, x))
    }
}

// MARK: - Hyperbolic Sine

struct SinhOperation: MathOperation {
    static var name: String = "sinh"
    static var arguments: [String] = ["x"]
    static var help: String = "Calculate hyperbolic sine: sinh x"
    static var category: OperationCategory = .trigonometry

    static func execute(args: [Any]) throws -> OperationResult {
        let x = try parseDouble(args[0], argumentName: "x")
        return .number(sinh(x))
    }
}

// MARK: - Hyperbolic Cosine

struct CoshOperation: MathOperation {
    static var name: String = "cosh"
    static var arguments: [String] = ["x"]
    static var help: String = "Calculate hyperbolic cosine: cosh x"
    static var category: OperationCategory = .trigonometry

    static func execute(args: [Any]) throws -> OperationResult {
        let x = try parseDouble(args[0], argumentName: "x")
        return .number(cosh(x))
    }
}

// MARK: - Hyperbolic Tangent

struct TanhOperation: MathOperation {
    static var name: String = "tanh"
    static var arguments: [String] = ["x"]
    static var help: String = "Calculate hyperbolic tangent: tanh x"
    static var category: OperationCategory = .trigonometry

    static func execute(args: [Any]) throws -> OperationResult {
        let x = try parseDouble(args[0], argumentName: "x")
        return .number(tanh(x))
    }
}

// MARK: - Inverse Hyperbolic Sine

struct AsinhOperation: MathOperation {
    static var name: String = "asinh"
    static var arguments: [String] = ["x"]
    static var help: String = "Calculate inverse hyperbolic sine: asinh x"
    static var category: OperationCategory = .trigonometry

    static func execute(args: [Any]) throws -> OperationResult {
        let x = try parseDouble(args[0], argumentName: "x")
        return .number(asinh(x))
    }
}

// MARK: - Inverse Hyperbolic Cosine

struct AcoshOperation: MathOperation {
    static var name: String = "acosh"
    static var arguments: [String] = ["x"]
    static var help: String = "Calculate inverse hyperbolic cosine: acosh x"
    static var category: OperationCategory = .trigonometry

    static func execute(args: [Any]) throws -> OperationResult {
        let x = try parseDouble(args[0], argumentName: "x")
        guard x >= 1 else {
            throw OperationError.invalidValue("acosh domain is [1, ∞)")
        }
        return .number(acosh(x))
    }
}

// MARK: - Inverse Hyperbolic Tangent

struct AtanhOperation: MathOperation {
    static var name: String = "atanh"
    static var arguments: [String] = ["x"]
    static var help: String = "Calculate inverse hyperbolic tangent: atanh x"
    static var category: OperationCategory = .trigonometry

    static func execute(args: [Any]) throws -> OperationResult {
        let x = try parseDouble(args[0], argumentName: "x")
        guard x > -1 && x < 1 else {
            throw OperationError.invalidValue("atanh domain is (-1, 1)")
        }
        return .number(atanh(x))
    }
}
