//
//  ConstantOperations.swift
//  MathCLI
//
//  Mathematical and physical constants (7 operations)
//

import Foundation

// MARK: - Pi

struct PiOperation: MathOperation {
    static var name: String = "pi"
    static var arguments: [String] = []
    static var help: String = "Return value of π (pi): pi"
    static var category: OperationCategory = .constants

    static func execute(args: [Any]) throws -> OperationResult {
        return .number(Double.pi)
    }
}

// MARK: - Euler's Number

struct EOperation: MathOperation {
    static var name: String = "e"
    static var arguments: [String] = []
    static var help: String = "Return value of e (Euler's number): e"
    static var category: OperationCategory = .constants

    static func execute(args: [Any]) throws -> OperationResult {
        return .number(M_E)
    }
}

// MARK: - Golden Ratio

struct GoldenRatioOperation: MathOperation {
    static var name: String = "golden_ratio"
    static var arguments: [String] = []
    static var help: String = "Return value of φ (golden ratio): golden_ratio"
    static var category: OperationCategory = .constants

    static func execute(args: [Any]) throws -> OperationResult {
        // φ = (1 + √5) / 2
        return .number((1.0 + sqrt(5.0)) / 2.0)
    }
}

// MARK: - Speed of Light

struct SpeedOfLightOperation: MathOperation {
    static var name: String = "speed_of_light"
    static var arguments: [String] = []
    static var help: String = "Return speed of light in m/s: speed_of_light"
    static var category: OperationCategory = .constants

    static func execute(args: [Any]) throws -> OperationResult {
        // Speed of light in vacuum (m/s)
        return .number(299_792_458.0)
    }
}

// MARK: - Planck Constant

struct PlanckOperation: MathOperation {
    static var name: String = "planck"
    static var arguments: [String] = []
    static var help: String = "Return Planck constant in J⋅s: planck"
    static var category: OperationCategory = .constants

    static func execute(args: [Any]) throws -> OperationResult {
        // Planck constant (J⋅s)
        return .number(6.62607015e-34)
    }
}

// MARK: - Avogadro's Number

struct AvogadroOperation: MathOperation {
    static var name: String = "avogadro"
    static var arguments: [String] = []
    static var help: String = "Return Avogadro's number (mol⁻¹): avogadro"
    static var category: OperationCategory = .constants

    static func execute(args: [Any]) throws -> OperationResult {
        // Avogadro constant (mol⁻¹)
        return .number(6.02214076e23)
    }
}

// MARK: - Boltzmann Constant

struct BoltzmannOperation: MathOperation {
    static var name: String = "boltzmann"
    static var arguments: [String] = []
    static var help: String = "Return Boltzmann constant in J/K: boltzmann"
    static var category: OperationCategory = .constants

    static func execute(args: [Any]) throws -> OperationResult {
        // Boltzmann constant (J/K)
        return .number(1.380649e-23)
    }
}
