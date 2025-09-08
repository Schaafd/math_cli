import math
from core.base_operations import MathOperation
from utils.validation import validate_number, validate_integer, validate_positive_number, validate_non_negative_number, validate_angle

class AddOperation(MathOperation):
    name = "add"
    args = ["a", "b"]
    help = "Add two numbers"

    @classmethod
    def execute(cls, a, b):
        """
        Return the sum of two numbers.
        
        Both operands are validated with validate_number (accepting int or float); the validated numeric values are added and the numeric result is returned.
        
        Parameters:
            a: First addend (int or float-like)
            b: Second addend (int or float-like)
        
        Returns:
            The numeric sum of `a` and `b` (int or float).
        """
        a = validate_number(a, "a")
        b = validate_number(b, "b")
        return a + b

class SubtractOperation(MathOperation):
    name = "subtract"
    args = ["a", "b"]
    help = "Subtract b from a"

    @classmethod
    def execute(cls, a, b):
        """
        Return the result of subtracting b from a.
        
        Parameters:
            a (int | float): Minuend.
            b (int | float): Subtrahend.
        
        Returns:
            int | float: The numeric difference a - b.
        """
        a = validate_number(a, "a")
        b = validate_number(b, "b")
        return a - b

class MultiplyOperation(MathOperation):
    name = "multiply"
    args = ["a", "b"]
    help = "Multiply two numbers"

    @classmethod
    def execute(cls, a, b):
        """
        Multiply two numbers after validating both operands.
        
        Parameters:
            a: First multiplicand; will be validated as a numeric value.
            b: Second multiplicand; will be validated as a numeric value.
        
        Returns:
            The product of `a` and `b`.
        """
        a = validate_number(a, "a")
        b = validate_number(b, "b")
        return a * b

class DivideOperation(MathOperation):
    name = "divide"
    args = ["a", "b"]
    help = "Divide a by b"

    @classmethod
    def execute(cls, a, b):
        """
        Divide `a` by `b`, validating both operands and rejecting a zero (or near-zero) divisor.
        
        Parameters:
            a: Dividend; will be validated as a number.
            b: Divisor; will be validated as a number and must not be zero or effectively zero.
        
        Returns:
            The quotient a / b.
        
        Raises:
            ValueError: If `b` is zero or is within 1e-10 of zero.
        """
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
        """
        Raise `base` to the power of `exponent`.
        
        Validates both arguments as numbers before computing the result and returns the power as a float.
        
        Parameters:
            base: The base value.
            exponent: The exponent value.
        
        Returns:
            float: The result of base raised to exponent.
        """
        base = validate_number(base, "base")
        exponent = validate_number(exponent, "exponent")
        return math.pow(base, exponent)

class SquareRootOperation(MathOperation):
    name = "sqrt"
    args = ["n"]
    help = "Calculate the square root of n"

    @classmethod
    def execute(cls, n):
        """
        Return the square root of a non-negative number.
        
        Parameters:
            n (int|float): A non-negative number. Validation enforces n >= 0.
        
        Returns:
            float: The square root of n.
        """
        n = validate_non_negative_number(n, "n")
        return math.sqrt(n)

class FactorialOperation(MathOperation):
    name = "factorial"
    args = ["n"]
    help = "Calculate the factorial of n"

    @classmethod
    def execute(cls, n):
        """
        Calculate the factorial of a non-negative integer.
        
        Validates that `n` is an integer and returns n! (n factorial). Raises a ValueError if `n` is negative.
        
        Parameters:
            n (int): Non-negative integer whose factorial to compute.
        
        Returns:
            int: Factorial of `n`.
        
        Raises:
            ValueError: If `n` is negative.
        """
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
        """
        Return the logarithm of n using the specified base.
        
        n and base must be positive; base must not be 1. Returns math.log(n, base) as a float.
        
        Raises:
            ValueError: If base is (effectively) 1.
        """
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
        """
        Return the sine of an angle in radians.
        
        Parameters:
            angle (float): Angle in radians; validated for correct numeric type/range before computation.
        
        Returns:
            float: Sine of the provided angle.
        """
        angle = validate_angle(angle, "angle")
        return math.sin(angle)

class CosineOperation(MathOperation):
    name = "cos"
    args = ["angle"]
    help = "Calculate the cosine of an angle in radians"

    @classmethod
    def execute(cls, angle):
        """
        Return the cosine of an angle in radians.
        
        Parameters:
            angle (float): Angle in radians.
        
        Returns:
            float: Cosine of the given angle.
        """
        angle = validate_angle(angle, "angle")
        return math.cos(angle)

class TangentOperation(MathOperation):
    name = "tan"
    args = ["angle"]
    help = "Calculate the tangent of an angle in radians"

    @classmethod
    def execute(cls, angle):
        """
        Return the tangent of the given angle.
        
        Angle must be provided in radians; the value is validated before computation. Returns the tangent as a float.
        """
        angle = validate_angle(angle, "angle")
        return math.tan(angle)

class DegreesToRadiansOperation(MathOperation):
    name = "to_radians"
    args = ["degrees"]
    help = "Convert degrees to radians"

    @classmethod
    def execute(cls, degrees):
        """
        Convert an angle in degrees to radians.
        
        Parameters:
            degrees (float | int): Angle in degrees; must be a finite number (validated).
        
        Returns:
            float: Angle in radians.
        """
        degrees = validate_number(degrees, "degrees")
        return math.radians(degrees)

class RadiansToDegreesOperation(MathOperation):
    name = "to_degrees"
    args = ["radians"]
    help = "Convert radians to degrees"

    @classmethod
    def execute(cls, radians):
        """
        Convert an angle from radians to degrees.
        
        Parameters:
            radians (float): Angle in radians; must be a finite number (validated).
        
        Returns:
            float: Angle converted to degrees.
        """
        radians = validate_number(radians, "radians")
        return math.degrees(radians)

class AbsoluteOperation(MathOperation):
    name = "abs"
    args = ["n"]
    help = "Calculate the absolute value of n"

    @classmethod
    def execute(cls, n):
        """
        Return the absolute value of n.
        
        Validates that `n` is a numeric value and returns its non-negative magnitude (int or float).
        Parameters:
            n: The number whose absolute value will be returned.
        Returns:
            The absolute value of `n` (same numeric type where possible).
        """
        n = validate_number(n, "n")
        return abs(n)
