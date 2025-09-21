"""
Mathematical Constants Plugin

Provides access to important mathematical and physical constants.
"""

import math
from core.base_operations import MathOperation

class PiOperation(MathOperation):
    name = "pi"
    args = []
    help = "Return the mathematical constant π (pi)"

    @classmethod
    def execute(cls):
        return math.pi

class EulerOperation(MathOperation):
    name = "e"
    args = []
    help = "Return Euler's number (e)"

    @classmethod
    def execute(cls):
        return math.e

class TauOperation(MathOperation):
    name = "tau"
    args = []
    help = "Return the mathematical constant τ (tau = 2π)"

    @classmethod
    def execute(cls):
        return math.tau

class GoldenRatioOperation(MathOperation):
    name = "golden_ratio"
    args = []
    help = "Return the golden ratio φ (phi) ≈ 1.618"

    @classmethod
    def execute(cls):
        return (1 + math.sqrt(5)) / 2

class NaturalLogOf2Operation(MathOperation):
    name = "ln2"
    args = []
    help = "Return the natural logarithm of 2"

    @classmethod
    def execute(cls):
        return math.log(2)

class NaturalLogOf10Operation(MathOperation):
    name = "ln10"
    args = []
    help = "Return the natural logarithm of 10"

    @classmethod
    def execute(cls):
        return math.log(10)

class SquareRootOf2Operation(MathOperation):
    name = "sqrt2"
    args = []
    help = "Return the square root of 2"

    @classmethod
    def execute(cls):
        return math.sqrt(2)

class SquareRootOf3Operation(MathOperation):
    name = "sqrt3"
    args = []
    help = "Return the square root of 3"

    @classmethod
    def execute(cls):
        return math.sqrt(3)

class EulerMascheroniConstantOperation(MathOperation):
    name = "euler_gamma"
    args = []
    help = "Return the Euler-Mascheroni constant γ ≈ 0.5772"

    @classmethod
    def execute(cls):
        # Euler-Mascheroni constant (approximation)
        return 0.5772156649015329

class PlanckConstantOperation(MathOperation):
    name = "planck"
    args = []
    help = "Return Planck's constant in J⋅s"

    @classmethod
    def execute(cls):
        return 6.62607015e-34

class SpeedOfLightOperation(MathOperation):
    name = "speed_of_light"
    args = []
    help = "Return the speed of light in vacuum (m/s)"

    @classmethod
    def execute(cls):
        return 299792458

class GravitationalConstantOperation(MathOperation):
    name = "gravitational_constant"
    args = []
    help = "Return the gravitational constant G (m³/kg⋅s²)"

    @classmethod
    def execute(cls):
        return 6.67430e-11

class AvogadroNumberOperation(MathOperation):
    name = "avogadro"
    args = []
    help = "Return Avogadro's number (mol⁻¹)"

    @classmethod
    def execute(cls):
        return 6.02214076e23

class BoltzmannConstantOperation(MathOperation):
    name = "boltzmann"
    args = []
    help = "Return Boltzmann constant (J/K)"

    @classmethod
    def execute(cls):
        return 1.380649e-23

class ElementaryChargeOperation(MathOperation):
    name = "elementary_charge"
    args = []
    help = "Return elementary charge (C)"

    @classmethod
    def execute(cls):
        return 1.602176634e-19

class ElectronMassOperation(MathOperation):
    name = "electron_mass"
    args = []
    help = "Return electron rest mass (kg)"

    @classmethod
    def execute(cls):
        return 9.1093837015e-31

class ProtonMassOperation(MathOperation):
    name = "proton_mass"
    args = []
    help = "Return proton rest mass (kg)"

    @classmethod
    def execute(cls):
        return 1.67262192369e-27

class NeutronMassOperation(MathOperation):
    name = "neutron_mass"
    args = []
    help = "Return neutron rest mass (kg)"

    @classmethod
    def execute(cls):
        return 1.67492749804e-27
