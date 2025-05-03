import math
from core.base_operations import MathOperation

class AddOperation(MathOperation):
    name = "add"
    args = ["a", "b"]
    help = "Add two numbers"

    @classmethod
    def execute(cls, a, b):
        return a + b

class SubtractOperation(MathOperation):
    name = "subtract"
    args = ["a", "b"]
    help = "Subtract b from a"

    @classmethod
    def execute(cls, a, b):
        return a - b

class MultiplyOperation(MathOperation):
    name = "multiply"
    args = ["a", "b"]
    help = "Multiply two numbers"

    @classmethod
    def execute(cls, a, b):
        return a * b

class DivideOperation(MathOperation):
    name = "divide"
    args = ["a", "b"]
    help = "Divide a by b"

    @classmethod
    def execute(cls, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

class PowerOperation(MathOperation):
    name = "power"
    args = ["base", "exponent"]
    help = "Raise base to the power of exponent"

    @classmethod
    def execute(cls, base, exponent):
        return math.pow(base, exponent)

class SquareRootOperation(MathOperation):
    name = "sqrt"
    args = ["n"]
    help = "Calculate the square root of n"

    @classmethod
    def execute(cls, n):
        if n < 0:
            raise ValueError("Cannot calculate square root of a negative number")
        return math.sqrt(n)

class FactorialOperation(MathOperation):
    name = "factorial"
    args = ["n"]
    help = "Calculate the factorial of n"

    @classmethod
    def execute(cls, n):
        if n < 0:
            raise ValueError("Cannot calculate factorial of a negative number")
        if not isinstance(n, int):
            raise ValueError("Factorial requires an integer")
        return math.factorial(n)

class LogarithmOperation(MathOperation):
    name = "log"
    args = ["n", "base"]
    help = "Calculate the logarithm of n with the given base"

    @classmethod
    def execute(cls, n, base=math.e):
        if n <= 0:
            raise ValueError("Cannot calculate logarithm of a non-positive number")
        if base <= 0 or base == 1:
            raise ValueError("Invalid logarithm base")
        return math.log(n, base)

class SineOperation(MathOperation):
    name = "sin"
    args = ["angle"]
    help = "Calculate the sine of an angle in radians"

    @classmethod
    def execute(cls, angle):
        return math.sin(angle)

class CosineOperation(MathOperation):
    name = "cos"
    args = ["angle"]
    help = "Calculate the cosine of an angle in radians"

    @classmethod
    def execute(cls, angle):
        return math.cos(angle)

class TangentOperation(MathOperation):
    name = "tan"
    args = ["angle"]
    help = "Calculate the tangent of an angle in radians"

    @classmethod
    def execute(cls, angle):
        return math.tan(angle)

class DegreesToRadiansOperation(MathOperation):
    name = "to_radians"
    args = ["degrees"]
    help = "Convert degrees to radians"

    @classmethod
    def execute(cls, degrees):
        return math.radians(degrees)

class RadiansToDegreesOperation(MathOperation):
    name = "to_degrees"
    args = ["radians"]
    help = "Convert radians to degrees"

    @classmethod
    def execute(cls, radians):
        return math.degrees(radians)

class AbsoluteOperation(MathOperation):
    name = "abs"
    args = ["n"]
    help = "Calculate the absolute value of n"

    @classmethod
    def execute(cls, n):
        return abs(n)
