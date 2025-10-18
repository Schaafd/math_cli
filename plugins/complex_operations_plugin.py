"""Complex number operations plugin for Math CLI."""

from core.base_operations import MathOperation
import cmath
import math


class ComplexNumberOperation(MathOperation):
    """Create a complex number from real and imaginary parts."""

    name = "complex"
    args = ["real", "imaginary"]
    help = "Create a complex number from real and imaginary parts (e.g., complex 3 4 -> 3+4j)"
    category = "complex"

    @classmethod
    def execute(cls, real: float, imaginary: float) -> complex:
        """Create a complex number.

        Args:
            real: Real part
            imaginary: Imaginary part

        Returns:
            Complex number
        """
        return complex(real, imaginary)


class ComplexAddOperation(MathOperation):
    """Add two complex numbers."""

    name = "cadd"
    args = ["z1_real", "z1_imag", "z2_real", "z2_imag"]
    help = "Add two complex numbers: cadd r1 i1 r2 i2"
    category = "complex"

    @classmethod
    def execute(cls, z1_real: float, z1_imag: float, z2_real: float, z2_imag: float) -> complex:
        """Add two complex numbers.

        Args:
            z1_real: Real part of first number
            z1_imag: Imaginary part of first number
            z2_real: Real part of second number
            z2_imag: Imaginary part of second number

        Returns:
            Sum of the complex numbers
        """
        z1 = complex(z1_real, z1_imag)
        z2 = complex(z2_real, z2_imag)
        return z1 + z2


class ComplexSubtractOperation(MathOperation):
    """Subtract two complex numbers."""

    name = "csub"
    args = ["z1_real", "z1_imag", "z2_real", "z2_imag"]
    help = "Subtract two complex numbers: csub r1 i1 r2 i2"
    category = "complex"

    @classmethod
    def execute(cls, z1_real: float, z1_imag: float, z2_real: float, z2_imag: float) -> complex:
        """Subtract two complex numbers.

        Args:
            z1_real: Real part of first number
            z1_imag: Imaginary part of first number
            z2_real: Real part of second number
            z2_imag: Imaginary part of second number

        Returns:
            Difference of the complex numbers
        """
        z1 = complex(z1_real, z1_imag)
        z2 = complex(z2_real, z2_imag)
        return z1 - z2


class ComplexMultiplyOperation(MathOperation):
    """Multiply two complex numbers."""

    name = "cmul"
    args = ["z1_real", "z1_imag", "z2_real", "z2_imag"]
    help = "Multiply two complex numbers: cmul r1 i1 r2 i2"
    category = "complex"

    @classmethod
    def execute(cls, z1_real: float, z1_imag: float, z2_real: float, z2_imag: float) -> complex:
        """Multiply two complex numbers.

        Args:
            z1_real: Real part of first number
            z1_imag: Imaginary part of first number
            z2_real: Real part of second number
            z2_imag: Imaginary part of second number

        Returns:
            Product of the complex numbers
        """
        z1 = complex(z1_real, z1_imag)
        z2 = complex(z2_real, z2_imag)
        return z1 * z2


class ComplexDivideOperation(MathOperation):
    """Divide two complex numbers."""

    name = "cdiv"
    args = ["z1_real", "z1_imag", "z2_real", "z2_imag"]
    help = "Divide two complex numbers: cdiv r1 i1 r2 i2"
    category = "complex"

    @classmethod
    def execute(cls, z1_real: float, z1_imag: float, z2_real: float, z2_imag: float) -> complex:
        """Divide two complex numbers.

        Args:
            z1_real: Real part of numerator
            z1_imag: Imaginary part of numerator
            z2_real: Real part of denominator
            z2_imag: Imaginary part of denominator

        Returns:
            Quotient of the complex numbers

        Raises:
            ValueError: If denominator is zero
        """
        z1 = complex(z1_real, z1_imag)
        z2 = complex(z2_real, z2_imag)

        if z2 == 0:
            raise ValueError("Cannot divide by zero")

        return z1 / z2


class ComplexMagnitudeOperation(MathOperation):
    """Calculate the magnitude (absolute value) of a complex number."""

    name = "magnitude"
    args = ["real", "imaginary"]
    help = "Calculate magnitude of complex number: magnitude r i -> |r+ij|"
    category = "complex"

    @classmethod
    def execute(cls, real: float, imaginary: float) -> float:
        """Calculate magnitude of a complex number.

        Args:
            real: Real part
            imaginary: Imaginary part

        Returns:
            Magnitude (absolute value)
        """
        z = complex(real, imaginary)
        return abs(z)


class ComplexPhaseOperation(MathOperation):
    """Calculate the phase (argument) of a complex number."""

    name = "phase"
    args = ["real", "imaginary"]
    help = "Calculate phase/argument of complex number in radians: phase r i"
    category = "complex"

    @classmethod
    def execute(cls, real: float, imaginary: float) -> float:
        """Calculate phase of a complex number.

        Args:
            real: Real part
            imaginary: Imaginary part

        Returns:
            Phase angle in radians (-π to π)
        """
        z = complex(real, imaginary)
        return cmath.phase(z)


class ComplexConjugateOperation(MathOperation):
    """Calculate the complex conjugate."""

    name = "conjugate"
    args = ["real", "imaginary"]
    help = "Calculate complex conjugate: conjugate r i -> r-ij"
    category = "complex"

    @classmethod
    def execute(cls, real: float, imaginary: float) -> complex:
        """Calculate complex conjugate.

        Args:
            real: Real part
            imaginary: Imaginary part

        Returns:
            Complex conjugate
        """
        z = complex(real, imaginary)
        return z.conjugate()


class ComplexPolarOperation(MathOperation):
    """Convert complex number to polar form."""

    name = "polar"
    args = ["real", "imaginary"]
    help = "Convert to polar form: polar r i -> (magnitude, phase)"
    category = "complex"

    @classmethod
    def execute(cls, real: float, imaginary: float) -> tuple:
        """Convert to polar form.

        Args:
            real: Real part
            imaginary: Imaginary part

        Returns:
            Tuple of (magnitude, phase_in_radians)
        """
        z = complex(real, imaginary)
        return cmath.polar(z)


class ComplexFromPolarOperation(MathOperation):
    """Create complex number from polar coordinates."""

    name = "from_polar"
    args = ["magnitude", "phase"]
    help = "Create complex number from polar form: from_polar mag phase"
    category = "complex"

    @classmethod
    def execute(cls, magnitude: float, phase: float) -> complex:
        """Create complex number from polar coordinates.

        Args:
            magnitude: Magnitude (r)
            phase: Phase angle in radians (θ)

        Returns:
            Complex number
        """
        return cmath.rect(magnitude, phase)


class ComplexRealPartOperation(MathOperation):
    """Extract real part of a complex number."""

    name = "real_part"
    args = ["real", "imaginary"]
    help = "Extract real part: real_part r i -> r"
    category = "complex"

    @classmethod
    def execute(cls, real: float, imaginary: float) -> float:
        """Extract real part.

        Args:
            real: Real part
            imaginary: Imaginary part

        Returns:
            Real part
        """
        z = complex(real, imaginary)
        return z.real


class ComplexImaginaryPartOperation(MathOperation):
    """Extract imaginary part of a complex number."""

    name = "imag_part"
    args = ["real", "imaginary"]
    help = "Extract imaginary part: imag_part r i -> i"
    category = "complex"

    @classmethod
    def execute(cls, real: float, imaginary: float) -> float:
        """Extract imaginary part.

        Args:
            real: Real part
            imaginary: Imaginary part

        Returns:
            Imaginary part
        """
        z = complex(real, imaginary)
        return z.imag


class ComplexExpOperation(MathOperation):
    """Calculate e^z for complex number."""

    name = "cexp"
    args = ["real", "imaginary"]
    help = "Calculate e^z for complex z: cexp r i"
    category = "complex"

    @classmethod
    def execute(cls, real: float, imaginary: float) -> complex:
        """Calculate e^z.

        Args:
            real: Real part
            imaginary: Imaginary part

        Returns:
            e^(real+imaginary*j)
        """
        z = complex(real, imaginary)
        return cmath.exp(z)


class ComplexLogOperation(MathOperation):
    """Calculate natural logarithm of complex number."""

    name = "clog"
    args = ["real", "imaginary"]
    help = "Calculate ln(z) for complex z: clog r i"
    category = "complex"

    @classmethod
    def execute(cls, real: float, imaginary: float) -> complex:
        """Calculate natural logarithm.

        Args:
            real: Real part
            imaginary: Imaginary part

        Returns:
            ln(real+imaginary*j)

        Raises:
            ValueError: If z is zero
        """
        z = complex(real, imaginary)
        if z == 0:
            raise ValueError("Cannot take logarithm of zero")
        return cmath.log(z)


class ComplexSqrtOperation(MathOperation):
    """Calculate square root of complex number."""

    name = "csqrt"
    args = ["real", "imaginary"]
    help = "Calculate sqrt(z) for complex z: csqrt r i"
    category = "complex"

    @classmethod
    def execute(cls, real: float, imaginary: float) -> complex:
        """Calculate square root.

        Args:
            real: Real part
            imaginary: Imaginary part

        Returns:
            sqrt(real+imaginary*j)
        """
        z = complex(real, imaginary)
        return cmath.sqrt(z)


class ComplexPowerOperation(MathOperation):
    """Raise complex number to a power."""

    name = "cpow"
    args = ["z_real", "z_imag", "n_real", "n_imag"]
    help = "Calculate z1^z2 for complex numbers: cpow z1r z1i z2r z2i"
    category = "complex"

    @classmethod
    def execute(cls, z_real: float, z_imag: float, n_real: float, n_imag: float) -> complex:
        """Calculate z1^z2.

        Args:
            z_real: Real part of base
            z_imag: Imaginary part of base
            n_real: Real part of exponent
            n_imag: Imaginary part of exponent

        Returns:
            z1^z2
        """
        z = complex(z_real, z_imag)
        n = complex(n_real, n_imag)
        return z ** n


class ComplexSinOperation(MathOperation):
    """Calculate sine of complex number."""

    name = "csin"
    args = ["real", "imaginary"]
    help = "Calculate sin(z) for complex z: csin r i"
    category = "complex"

    @classmethod
    def execute(cls, real: float, imaginary: float) -> complex:
        """Calculate sine.

        Args:
            real: Real part
            imaginary: Imaginary part

        Returns:
            sin(real+imaginary*j)
        """
        z = complex(real, imaginary)
        return cmath.sin(z)


class ComplexCosOperation(MathOperation):
    """Calculate cosine of complex number."""

    name = "ccos"
    args = ["real", "imaginary"]
    help = "Calculate cos(z) for complex z: ccos r i"
    category = "complex"

    @classmethod
    def execute(cls, real: float, imaginary: float) -> complex:
        """Calculate cosine.

        Args:
            real: Real part
            imaginary: Imaginary part

        Returns:
            cos(real+imaginary*j)
        """
        z = complex(real, imaginary)
        return cmath.cos(z)


# All operations are automatically discovered by the plugin manager
