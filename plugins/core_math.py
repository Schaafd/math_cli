import math
from core.base_operations import MathOperation
from utils.validation import validate_number, validate_integer, validate_positive_number, validate_non_negative_number, validate_angle

class AddOperation(MathOperation):
    name = "add"
    args = ["a", "b"]
    help = "Add two numbers"

    @classmethod
    def execute(cls, a, b):
        a = validate_number(a, "a")
        b = validate_number(b, "b")
        return a + b

class SubtractOperation(MathOperation):
    name = "subtract"
    args = ["a", "b"]
    help = "Subtract b from a"

    @classmethod
    def execute(cls, a, b):
        a = validate_number(a, "a")
        b = validate_number(b, "b")
        return a - b

class MultiplyOperation(MathOperation):
    name = "multiply"
    args = ["a", "b"]
    help = "Multiply two numbers"

    @classmethod
    def execute(cls, a, b):
        a = validate_number(a, "a")
        b = validate_number(b, "b")
        return a * b

class DivideOperation(MathOperation):
    name = "divide"
    args = ["a", "b"]
    help = "Divide a by b"

    @classmethod
    def execute(cls, a, b):
        a = validate_number(a, "a")
        b = validate_number(b, "b")
        if math.isclose(b, 0, abs_tol=1e-10):
            raise ValueError("Cannot divide by zero")
        return a / b

class PowerOperation(MathOperation):
    name = "power"
    args = ["base", "exponent"]
    help = "Raise base to the power of exponent"

    @classmethod
    def execute(cls, base, exponent):
        base = validate_number(base, "base")
        exponent = validate_number(exponent, "exponent")
        return math.pow(base, exponent)

class SquareRootOperation(MathOperation):
    name = "sqrt"
    args = ["n"]
    help = "Calculate the square root of n"

    @classmethod
    def execute(cls, n):
        n = validate_non_negative_number(n, "n")
        return math.sqrt(n)

class FactorialOperation(MathOperation):
    name = "factorial"
    args = ["n"]
    help = "Calculate the factorial of n"

    @classmethod
    def execute(cls, n):
        n = validate_integer(n, "n")
        if n < 0:
            raise ValueError("Cannot calculate factorial of a negative number")
        return math.factorial(n)

class LogarithmOperation(MathOperation):
    name = "log"
    args = ["n", "base"]
    help = "Calculate the logarithm of n with the given base"

    @classmethod
    def execute(cls, n, base=math.e):
        n = validate_positive_number(n, "n")
        base = validate_positive_number(base, "base")
        if math.isclose(base, 1, abs_tol=1e-10):
            raise ValueError("Invalid logarithm base: base cannot be 1")
        return math.log(n, base)

class SineOperation(MathOperation):
    name = "sin"
    args = ["angle"]
    help = "Calculate the sine of an angle in radians"

    @classmethod
    def execute(cls, angle):
        angle = validate_angle(angle, "angle")
        return math.sin(angle)

class CosineOperation(MathOperation):
    name = "cos"
    args = ["angle"]
    help = "Calculate the cosine of an angle in radians"

    @classmethod
    def execute(cls, angle):
        angle = validate_angle(angle, "angle")
        return math.cos(angle)

class TangentOperation(MathOperation):
    name = "tan"
    args = ["angle"]
    help = "Calculate the tangent of an angle in radians"

    @classmethod
    def execute(cls, angle):
        angle = validate_angle(angle, "angle")
        return math.tan(angle)

class DegreesToRadiansOperation(MathOperation):
    name = "to_radians"
    args = ["degrees"]
    help = "Convert degrees to radians"

    @classmethod
    def execute(cls, degrees):
        degrees = validate_number(degrees, "degrees")
        return math.radians(degrees)

class RadiansToDegreesOperation(MathOperation):
    name = "to_degrees"
    args = ["radians"]
    help = "Convert radians to degrees"

    @classmethod
    def execute(cls, radians):
        radians = validate_number(radians, "radians")
        return math.degrees(radians)

class AbsoluteOperation(MathOperation):
    name = "abs"
    args = ["n"]
    help = "Calculate the absolute value of n"

    @classmethod
    def execute(cls, n):
        n = validate_number(n, "n")
        return abs(n)
