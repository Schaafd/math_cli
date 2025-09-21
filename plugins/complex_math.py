"""
Complex Numbers Plugin

Provides complex number operations including arithmetic, magnitude,
phase calculations, and conversions.
"""

import math
from core.base_operations import MathOperation

class ComplexAddOperation(MathOperation):
    name = "complex_add"
    args = ["real1", "imag1", "real2", "imag2"]
    help = "Add two complex numbers: (real1 + imag1*i) + (real2 + imag2*i)"

    @classmethod
    def execute(cls, real1, imag1, real2, imag2):
        real_result = real1 + real2
        imag_result = imag1 + imag2
        return f"{real_result} + {imag_result}i" if imag_result >= 0 else f"{real_result} - {abs(imag_result)}i"

class ComplexSubtractOperation(MathOperation):
    name = "complex_subtract"
    args = ["real1", "imag1", "real2", "imag2"]
    help = "Subtract two complex numbers: (real1 + imag1*i) - (real2 + imag2*i)"

    @classmethod
    def execute(cls, real1, imag1, real2, imag2):
        real_result = real1 - real2
        imag_result = imag1 - imag2
        return f"{real_result} + {imag_result}i" if imag_result >= 0 else f"{real_result} - {abs(imag_result)}i"

class ComplexMultiplyOperation(MathOperation):
    name = "complex_multiply"
    args = ["real1", "imag1", "real2", "imag2"]
    help = "Multiply two complex numbers: (real1 + imag1*i) * (real2 + imag2*i)"

    @classmethod
    def execute(cls, real1, imag1, real2, imag2):
        # (a + bi)(c + di) = (ac - bd) + (ad + bc)i
        real_result = real1 * real2 - imag1 * imag2
        imag_result = real1 * imag2 + imag1 * real2
        return f"{real_result} + {imag_result}i" if imag_result >= 0 else f"{real_result} - {abs(imag_result)}i"

class ComplexDivideOperation(MathOperation):
    name = "complex_divide"
    args = ["real1", "imag1", "real2", "imag2"]
    help = "Divide two complex numbers: (real1 + imag1*i) / (real2 + imag2*i)"

    @classmethod
    def execute(cls, real1, imag1, real2, imag2):
        if real2 == 0 and imag2 == 0:
            raise ValueError("Cannot divide by zero complex number")

        # (a + bi) / (c + di) = [(a + bi)(c - di)] / (c² + d²)
        denominator = real2 ** 2 + imag2 ** 2
        real_result = (real1 * real2 + imag1 * imag2) / denominator
        imag_result = (imag1 * real2 - real1 * imag2) / denominator

        return f"{real_result} + {imag_result}i" if imag_result >= 0 else f"{real_result} - {abs(imag_result)}i"

class ComplexMagnitudeOperation(MathOperation):
    name = "complex_magnitude"
    args = ["real", "imag"]
    help = "Calculate the magnitude (absolute value) of a complex number"

    @classmethod
    def execute(cls, real, imag):
        return math.sqrt(real ** 2 + imag ** 2)

class ComplexPhaseOperation(MathOperation):
    name = "complex_phase"
    args = ["real", "imag"]
    help = "Calculate the phase (argument) of a complex number in radians"

    @classmethod
    def execute(cls, real, imag):
        return math.atan2(imag, real)

class ComplexConjugateOperation(MathOperation):
    name = "complex_conjugate"
    args = ["real", "imag"]
    help = "Calculate the complex conjugate of a complex number"

    @classmethod
    def execute(cls, real, imag):
        return f"{real} + {-imag}i" if -imag >= 0 else f"{real} - {abs(-imag)}i"

class PolarToRectangularOperation(MathOperation):
    name = "polar_to_rect"
    args = ["magnitude", "phase"]
    help = "Convert from polar form (magnitude, phase) to rectangular form (real + imag*i)"

    @classmethod
    def execute(cls, magnitude, phase):
        if magnitude < 0:
            raise ValueError("Magnitude must be non-negative")

        real = magnitude * math.cos(phase)
        imag = magnitude * math.sin(phase)
        return f"{real} + {imag}i" if imag >= 0 else f"{real} - {abs(imag)}i"

class RectangularToPolarOperation(MathOperation):
    name = "rect_to_polar"
    args = ["real", "imag"]
    help = "Convert from rectangular form (real + imag*i) to polar form (returns magnitude and phase)"

    @classmethod
    def execute(cls, real, imag):
        magnitude = math.sqrt(real ** 2 + imag ** 2)
        phase = math.atan2(imag, real)
        return f"Magnitude: {magnitude}, Phase: {phase} radians"

class ComplexPowerOperation(MathOperation):
    name = "complex_power"
    args = ["real", "imag", "exponent"]
    help = "Raise a complex number to a real power using De Moivre's theorem"

    @classmethod
    def execute(cls, real, imag, exponent):
        # Convert to polar form
        magnitude = math.sqrt(real ** 2 + imag ** 2)
        phase = math.atan2(imag, real)

        # Apply De Moivre's theorem: (r*e^(iθ))^n = r^n * e^(inθ)
        new_magnitude = magnitude ** exponent
        new_phase = phase * exponent

        # Convert back to rectangular form
        result_real = new_magnitude * math.cos(new_phase)
        result_imag = new_magnitude * math.sin(new_phase)

        return f"{result_real} + {result_imag}i" if result_imag >= 0 else f"{result_real} - {abs(result_imag)}i"

class ComplexExponentialOperation(MathOperation):
    name = "complex_exp"
    args = ["real", "imag"]
    help = "Calculate e^(real + imag*i) using Euler's formula"

    @classmethod
    def execute(cls, real, imag):
        # e^(a + bi) = e^a * (cos(b) + i*sin(b))
        exp_real = math.exp(real)
        result_real = exp_real * math.cos(imag)
        result_imag = exp_real * math.sin(imag)

        return f"{result_real} + {result_imag}i" if result_imag >= 0 else f"{result_real} - {abs(result_imag)}i"

class ComplexLogarithmOperation(MathOperation):
    name = "complex_log"
    args = ["real", "imag"]
    help = "Calculate the natural logarithm of a complex number"

    @classmethod
    def execute(cls, real, imag):
        if real == 0 and imag == 0:
            raise ValueError("Cannot calculate logarithm of zero")

        magnitude = math.sqrt(real ** 2 + imag ** 2)
        phase = math.atan2(imag, real)

        log_real = math.log(magnitude)
        log_imag = phase

        return f"{log_real} + {log_imag}i" if log_imag >= 0 else f"{log_real} - {abs(log_imag)}i"
