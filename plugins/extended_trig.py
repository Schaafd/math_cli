"""
Extended Trigonometric Functions Plugin

Provides inverse trigonometric and hyperbolic functions.
"""

import math
from core.base_operations import MathOperation

class ArcSineOperation(MathOperation):
    name = "asin"
    args = ["x"]
    help = "Calculate the arcsine (inverse sine) of x, returns result in radians"

    @classmethod
    def execute(cls, x):
        if x < -1 or x > 1:
            raise ValueError("Input must be between -1 and 1 for arcsine")
        return math.asin(x)

class ArcCosineOperation(MathOperation):
    name = "acos"
    args = ["x"]
    help = "Calculate the arccosine (inverse cosine) of x, returns result in radians"

    @classmethod
    def execute(cls, x):
        if x < -1 or x > 1:
            raise ValueError("Input must be between -1 and 1 for arccosine")
        return math.acos(x)

class ArcTangentOperation(MathOperation):
    name = "atan"
    args = ["x"]
    help = "Calculate the arctangent (inverse tangent) of x, returns result in radians"

    @classmethod
    def execute(cls, x):
        return math.atan(x)

class ArcTangent2Operation(MathOperation):
    name = "atan2"
    args = ["y", "x"]
    help = "Calculate the arctangent of y/x using the signs to determine quadrant"

    @classmethod
    def execute(cls, y, x):
        return math.atan2(y, x)

class HyperbolicSineOperation(MathOperation):
    name = "sinh"
    args = ["x"]
    help = "Calculate the hyperbolic sine of x"

    @classmethod
    def execute(cls, x):
        return math.sinh(x)

class HyperbolicCosineOperation(MathOperation):
    name = "cosh"
    args = ["x"]
    help = "Calculate the hyperbolic cosine of x"

    @classmethod
    def execute(cls, x):
        return math.cosh(x)

class HyperbolicTangentOperation(MathOperation):
    name = "tanh"
    args = ["x"]
    help = "Calculate the hyperbolic tangent of x"

    @classmethod
    def execute(cls, x):
        return math.tanh(x)

class InverseHyperbolicSineOperation(MathOperation):
    name = "asinh"
    args = ["x"]
    help = "Calculate the inverse hyperbolic sine of x"

    @classmethod
    def execute(cls, x):
        return math.asinh(x)

class InverseHyperbolicCosineOperation(MathOperation):
    name = "acosh"
    args = ["x"]
    help = "Calculate the inverse hyperbolic cosine of x"

    @classmethod
    def execute(cls, x):
        if x < 1:
            raise ValueError("Input must be >= 1 for inverse hyperbolic cosine")
        return math.acosh(x)

class InverseHyperbolicTangentOperation(MathOperation):
    name = "atanh"
    args = ["x"]
    help = "Calculate the inverse hyperbolic tangent of x"

    @classmethod
    def execute(cls, x):
        if x <= -1 or x >= 1:
            raise ValueError("Input must be between -1 and 1 (exclusive) for inverse hyperbolic tangent")
        return math.atanh(x)
