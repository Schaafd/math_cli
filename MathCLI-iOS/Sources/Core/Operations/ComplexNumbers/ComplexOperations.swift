//
//  ComplexOperations.swift
//  MathCLI
//
//  Complex number operations (18 operations)
//

import Foundation

// Helper function to parse complex numbers
private func parseComplex(_ args: [Any], startIndex: Int = 0) throws -> (real: Double, imag: Double) {
    // Expect two arguments: real and imaginary parts
    guard args.count >= startIndex + 2 else {
        throw OperationError.invalidArgumentCount(expected: startIndex + 2, got: args.count)
    }

    let real = try MathOperation.parseDouble(args[startIndex], argumentName: "real")
    let imag = try MathOperation.parseDouble(args[startIndex + 1], argumentName: "imaginary")

    return (real, imag)
}

// MARK: - Complex Addition

struct CaddOperation: MathOperation {
    static var name = "cadd"
    static var arguments = ["real1", "imag1", "real2", "imag2"]
    static var help = "Add complex numbers: cadd real1 imag1 real2 imag2"
    static var category = OperationCategory.complexNumbers

    static func execute(args: [Any]) throws -> OperationResult {
        let (r1, i1) = try parseComplex(args, startIndex: 0)
        let (r2, i2) = try parseComplex(args, startIndex: 2)

        return .complex(real: r1 + r2, imaginary: i1 + i2)
    }
}

// MARK: - Complex Subtraction

struct CsubOperation: MathOperation {
    static var name = "csub"
    static var arguments = ["real1", "imag1", "real2", "imag2"]
    static var help = "Subtract complex numbers: csub real1 imag1 real2 imag2"
    static var category = OperationCategory.complexNumbers

    static func execute(args: [Any]) throws -> OperationResult {
        let (r1, i1) = try parseComplex(args, startIndex: 0)
        let (r2, i2) = try parseComplex(args, startIndex: 2)

        return .complex(real: r1 - r2, imaginary: i1 - i2)
    }
}

// MARK: - Complex Multiplication

struct CmulOperation: MathOperation {
    static var name = "cmul"
    static var arguments = ["real1", "imag1", "real2", "imag2"]
    static var help = "Multiply complex numbers: cmul real1 imag1 real2 imag2"
    static var category = OperationCategory.complexNumbers

    static func execute(args: [Any]) throws -> OperationResult {
        let (r1, i1) = try parseComplex(args, startIndex: 0)
        let (r2, i2) = try parseComplex(args, startIndex: 2)

        // (a + bi)(c + di) = (ac - bd) + (ad + bc)i
        let real = r1 * r2 - i1 * i2
        let imag = r1 * i2 + i1 * r2

        return .complex(real: real, imaginary: imag)
    }
}

// MARK: - Complex Division

struct CdivOperation: MathOperation {
    static var name = "cdiv"
    static var arguments = ["real1", "imag1", "real2", "imag2"]
    static var help = "Divide complex numbers: cdiv real1 imag1 real2 imag2"
    static var category = OperationCategory.complexNumbers

    static func execute(args: [Any]) throws -> OperationResult {
        let (r1, i1) = try parseComplex(args, startIndex: 0)
        let (r2, i2) = try parseComplex(args, startIndex: 2)

        let denominator = r2 * r2 + i2 * i2
        guard denominator != 0 else {
            throw OperationError.divisionByZero
        }

        // (a + bi) / (c + di) = [(ac + bd) + (bc - ad)i] / (c² + d²)
        let real = (r1 * r2 + i1 * i2) / denominator
        let imag = (i1 * r2 - r1 * i2) / denominator

        return .complex(real: real, imaginary: imag)
    }
}

// MARK: - Magnitude

struct MagnitudeOperation: MathOperation {
    static var name = "magnitude"
    static var arguments = ["real", "imag"]
    static var help = "Calculate magnitude of complex number: magnitude real imag"
    static var category = OperationCategory.complexNumbers

    static func execute(args: [Any]) throws -> OperationResult {
        let (r, i) = try parseComplex(args)
        return .number(sqrt(r * r + i * i))
    }
}

// MARK: - Phase (Argument)

struct PhaseOperation: MathOperation {
    static var name = "phase"
    static var arguments = ["real", "imag"]
    static var help = "Calculate phase (argument) of complex number in radians: phase real imag"
    static var category = OperationCategory.complexNumbers

    static func execute(args: [Any]) throws -> OperationResult {
        let (r, i) = try parseComplex(args)
        return .number(atan2(i, r))
    }
}

// MARK: - Conjugate

struct ConjugateOperation: MathOperation {
    static var name = "conjugate"
    static var arguments = ["real", "imag"]
    static var help = "Calculate complex conjugate: conjugate real imag"
    static var category = OperationCategory.complexNumbers

    static func execute(args: [Any]) throws -> OperationResult {
        let (r, i) = try parseComplex(args)
        return .complex(real: r, imaginary: -i)
    }
}

// MARK: - Polar to Rectangular

struct PolarOperation: MathOperation {
    static var name = "polar"
    static var arguments = ["magnitude", "phase"]
    static var help = "Convert polar to rectangular: polar magnitude phase"
    static var category = OperationCategory.complexNumbers

    static func execute(args: [Any]) throws -> OperationResult {
        let magnitude = try parseDouble(args[0], argumentName: "magnitude")
        let phase = try parseDouble(args[1], argumentName: "phase")

        let real = magnitude * cos(phase)
        let imag = magnitude * sin(phase)

        return .complex(real: real, imaginary: imag)
    }
}

// MARK: - Rectangular to Polar

struct RectangularOperation: MathOperation {
    static var name = "rectangular"
    static var arguments = ["magnitude", "phase"]
    static var help = "Convert rectangular to polar (returns array [magnitude, phase]): rectangular real imag"
    static var category = OperationCategory.complexNumbers

    static func execute(args: [Any]) throws -> OperationResult {
        let (r, i) = try parseComplex(args)

        let magnitude = sqrt(r * r + i * i)
        let phase = atan2(i, r)

        return .array([magnitude, phase])
    }
}

// MARK: - Complex Square Root

struct CsqrtOperation: MathOperation {
    static var name = "csqrt"
    static var arguments = ["real", "imag"]
    static var help = "Calculate complex square root: csqrt real imag"
    static var category = OperationCategory.complexNumbers

    static func execute(args: [Any]) throws -> OperationResult {
        let (r, i) = try parseComplex(args)

        let magnitude = sqrt(r * r + i * i)
        let angle = atan2(i, r)

        let newMagnitude = sqrt(magnitude)
        let newAngle = angle / 2

        let resultReal = newMagnitude * cos(newAngle)
        let resultImag = newMagnitude * sin(newAngle)

        return .complex(real: resultReal, imaginary: resultImag)
    }
}

// MARK: - Complex Exponential

struct CexpOperation: MathOperation {
    static var name = "cexp"
    static var arguments = ["real", "imag"]
    static var help = "Calculate e^(real + imag*i): cexp real imag"
    static var category = OperationCategory.complexNumbers

    static func execute(args: [Any]) throws -> OperationResult {
        let (r, i) = try parseComplex(args)

        // e^(a + bi) = e^a * (cos(b) + i*sin(b))
        let expReal = exp(r)
        let resultReal = expReal * cos(i)
        let resultImag = expReal * sin(i)

        return .complex(real: resultReal, imaginary: resultImag)
    }
}

// MARK: - Complex Logarithm

struct ClogOperation: MathOperation {
    static var name = "clog"
    static var arguments = ["real", "imag"]
    static var help = "Calculate natural log of complex number: clog real imag"
    static var category = OperationCategory.complexNumbers

    static func execute(args: [Any]) throws -> OperationResult {
        let (r, i) = try parseComplex(args)

        // log(a + bi) = log(|z|) + i*arg(z)
        let magnitude = sqrt(r * r + i * i)
        let angle = atan2(i, r)

        return .complex(real: log(magnitude), imaginary: angle)
    }
}

// MARK: - Complex Sine

struct CsinOperation: MathOperation {
    static var name = "csin"
    static var arguments = ["real", "imag"]
    static var help = "Calculate sine of complex number: csin real imag"
    static var category = OperationCategory.complexNumbers

    static func execute(args: [Any]) throws -> OperationResult {
        let (r, i) = try parseComplex(args)

        // sin(a + bi) = sin(a)cosh(b) + i*cos(a)sinh(b)
        let resultReal = sin(r) * cosh(i)
        let resultImag = cos(r) * sinh(i)

        return .complex(real: resultReal, imaginary: resultImag)
    }
}

// MARK: - Complex Cosine

struct CcosOperation: MathOperation {
    static var name = "ccos"
    static var arguments = ["real", "imag"]
    static var help = "Calculate cosine of complex number: ccos real imag"
    static var category = OperationCategory.complexNumbers

    static func execute(args: [Any]) throws -> OperationResult {
        let (r, i) = try parseComplex(args)

        // cos(a + bi) = cos(a)cosh(b) - i*sin(a)sinh(b)
        let resultReal = cos(r) * cosh(i)
        let resultImag = -sin(r) * sinh(i)

        return .complex(real: resultReal, imaginary: resultImag)
    }
}

// MARK: - Complex Tangent

struct CtanOperation: MathOperation {
    static var name = "ctan"
    static var arguments = ["real", "imag"]
    static var help = "Calculate tangent of complex number: ctan real imag"
    static var category = OperationCategory.complexNumbers

    static func execute(args: [Any]) throws -> OperationResult {
        let (r, i) = try parseComplex(args)

        // tan(z) = sin(z) / cos(z)
        let sinReal = sin(r) * cosh(i)
        let sinImag = cos(r) * sinh(i)
        let cosReal = cos(r) * cosh(i)
        let cosImag = -sin(r) * sinh(i)

        let denominator = cosReal * cosReal + cosImag * cosImag
        guard denominator != 0 else {
            throw OperationError.divisionByZero
        }

        let resultReal = (sinReal * cosReal + sinImag * cosImag) / denominator
        let resultImag = (sinImag * cosReal - sinReal * cosImag) / denominator

        return .complex(real: resultReal, imaginary: resultImag)
    }
}

// MARK: - Complex Power

struct CpowerOperation: MathOperation {
    static var name = "cpower"
    static var arguments = ["real1", "imag1", "real2", "imag2"]
    static var help = "Raise complex number to complex power: cpower real1 imag1 real2 imag2"
    static var category = OperationCategory.complexNumbers

    static func execute(args: [Any]) throws -> OperationResult {
        let (r1, i1) = try parseComplex(args, startIndex: 0)
        let (r2, i2) = try parseComplex(args, startIndex: 2)

        // z1^z2 = exp(z2 * log(z1))
        let logMag = log(sqrt(r1 * r1 + i1 * i1))
        let logArg = atan2(i1, r1)

        let logReal = logMag
        let logImag = logArg

        // Multiply by exponent
        let multReal = r2 * logReal - i2 * logImag
        let multImag = r2 * logImag + i2 * logReal

        // Take exponential
        let expReal = exp(multReal)
        let resultReal = expReal * cos(multImag)
        let resultImag = expReal * sin(multImag)

        return .complex(real: resultReal, imaginary: resultImag)
    }
}

// MARK: - Cis (cos + i sin)

struct CisOperation: MathOperation {
    static var name = "cis"
    static var arguments = ["theta"]
    static var help = "Calculate cis(θ) = cos(θ) + i*sin(θ): cis theta"
    static var category = OperationCategory.complexNumbers

    static func execute(args: [Any]) throws -> OperationResult {
        let theta = try parseDouble(args[0], argumentName: "theta")
        return .complex(real: cos(theta), imaginary: sin(theta))
    }
}

// MARK: - Real Part

struct RealPartOperation: MathOperation {
    static var name = "real_part"
    static var arguments = ["real", "imag"]
    static var help = "Extract real part of complex number: real_part real imag"
    static var category = OperationCategory.complexNumbers

    static func execute(args: [Any]) throws -> OperationResult {
        let (r, _) = try parseComplex(args)
        return .number(r)
    }
}

// MARK: - Imaginary Part

struct ImagPartOperation: MathOperation {
    static var name = "imag_part"
    static var arguments = ["real", "imag"]
    static var help = "Extract imaginary part of complex number: imag_part real imag"
    static var category = OperationCategory.complexNumbers

    static func execute(args: [Any]) throws -> OperationResult {
        let (_, i) = try parseComplex(args)
        return .number(i)
    }
}
