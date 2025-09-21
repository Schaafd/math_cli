"""
Advanced Mathematical Functions Plugin

Provides advanced mathematical operations like ceiling, floor, rounding,
GCD, LCM, modulo, and exponential functions.
"""

import math
from core.base_operations import MathOperation

class CeilingOperation(MathOperation):
    name = "ceil"
    args = ["x"]
    help = "Return the ceiling of x (smallest integer >= x)"

    @classmethod
    def execute(cls, x):
        return math.ceil(x)

class FloorOperation(MathOperation):
    name = "floor"
    args = ["x"]
    help = "Return the floor of x (largest integer <= x)"

    @classmethod
    def execute(cls, x):
        return math.floor(x)

class RoundOperation(MathOperation):
    name = "round"
    args = ["x", "digits"]
    help = "Round x to the given number of decimal places"

    @classmethod
    def execute(cls, x, digits=0):
        return round(x, int(digits))

class GreatestCommonDivisorOperation(MathOperation):
    name = "gcd"
    args = ["a", "b"]
    help = "Calculate the greatest common divisor of two integers"

    @classmethod
    def execute(cls, a, b):
        try:
            a, b = int(a), int(b)
        except (ValueError, TypeError):
            raise ValueError("GCD requires integer inputs")
        return math.gcd(a, b)

class LeastCommonMultipleOperation(MathOperation):
    name = "lcm"
    args = ["a", "b"]
    help = "Calculate the least common multiple of two integers"

    @classmethod
    def execute(cls, a, b):
        try:
            a, b = int(a), int(b)
        except (ValueError, TypeError):
            raise ValueError("LCM requires integer inputs")
        return abs(a * b) // math.gcd(a, b) if a != 0 and b != 0 else 0

class ModuloOperation(MathOperation):
    name = "mod"
    args = ["a", "b"]
    help = "Calculate a modulo b (remainder of a divided by b)"

    @classmethod
    def execute(cls, a, b):
        if b == 0:
            raise ValueError("Cannot calculate modulo with zero divisor")
        return a % b

class ExponentialOperation(MathOperation):
    name = "exp"
    args = ["x"]
    help = "Calculate e raised to the power of x"

    @classmethod
    def execute(cls, x):
        return math.exp(x)

class RemainderOperation(MathOperation):
    name = "remainder"
    args = ["a", "b"]
    help = "Calculate the IEEE remainder of a divided by b"

    @classmethod
    def execute(cls, a, b):
        if b == 0:
            raise ValueError("Cannot calculate remainder with zero divisor")
        return math.remainder(a, b)

class TruncateOperation(MathOperation):
    name = "trunc"
    args = ["x"]
    help = "Truncate x to an integer (remove fractional part)"

    @classmethod
    def execute(cls, x):
        return math.trunc(x)
