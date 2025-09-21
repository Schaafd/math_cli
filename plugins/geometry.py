"""
Geometric Functions Plugin

Provides geometric calculations including distance, areas, and
basic geometric operations.
"""

import math
from core.base_operations import MathOperation

class DistanceOperation(MathOperation):
    name = "distance"
    args = ["x1", "y1", "x2", "y2"]
    help = "Calculate the Euclidean distance between two points (x1,y1) and (x2,y2)"

    @classmethod
    def execute(cls, x1, y1, x2, y2):
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

class Distance3DOperation(MathOperation):
    name = "distance3d"
    args = ["x1", "y1", "z1", "x2", "y2", "z2"]
    help = "Calculate the 3D Euclidean distance between two points"

    @classmethod
    def execute(cls, x1, y1, z1, x2, y2, z2):
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)

class CircleAreaOperation(MathOperation):
    name = "area_circle"
    args = ["radius"]
    help = "Calculate the area of a circle given its radius"

    @classmethod
    def execute(cls, radius):
        if radius < 0:
            raise ValueError("Radius must be non-negative")
        return math.pi * radius ** 2

class CircleCircumferenceOperation(MathOperation):
    name = "circumference"
    args = ["radius"]
    help = "Calculate the circumference of a circle given its radius"

    @classmethod
    def execute(cls, radius):
        if radius < 0:
            raise ValueError("Radius must be non-negative")
        return 2 * math.pi * radius

class TriangleAreaOperation(MathOperation):
    name = "area_triangle"
    args = ["base", "height"]
    help = "Calculate the area of a triangle given base and height"

    @classmethod
    def execute(cls, base, height):
        if base < 0 or height < 0:
            raise ValueError("Base and height must be non-negative")
        return 0.5 * base * height

class TriangleAreaHeronsOperation(MathOperation):
    name = "area_triangle_heron"
    args = ["a", "b", "c"]
    help = "Calculate triangle area using Heron's formula given three sides"

    @classmethod
    def execute(cls, a, b, c):
        if a <= 0 or b <= 0 or c <= 0:
            raise ValueError("All sides must be positive")
        if a + b <= c or a + c <= b or b + c <= a:
            raise ValueError("Invalid triangle: sum of any two sides must be greater than the third")

        s = (a + b + c) / 2  # semi-perimeter
        return math.sqrt(s * (s - a) * (s - b) * (s - c))

class RectangleAreaOperation(MathOperation):
    name = "area_rectangle"
    args = ["length", "width"]
    help = "Calculate the area of a rectangle"

    @classmethod
    def execute(cls, length, width):
        if length < 0 or width < 0:
            raise ValueError("Length and width must be non-negative")
        return length * width

class RectanglePerimeterOperation(MathOperation):
    name = "perimeter_rectangle"
    args = ["length", "width"]
    help = "Calculate the perimeter of a rectangle"

    @classmethod
    def execute(cls, length, width):
        if length < 0 or width < 0:
            raise ValueError("Length and width must be non-negative")
        return 2 * (length + width)

class SquareAreaOperation(MathOperation):
    name = "area_square"
    args = ["side"]
    help = "Calculate the area of a square"

    @classmethod
    def execute(cls, side):
        if side < 0:
            raise ValueError("Side length must be non-negative")
        return side ** 2

class SphereVolumeOperation(MathOperation):
    name = "volume_sphere"
    args = ["radius"]
    help = "Calculate the volume of a sphere"

    @classmethod
    def execute(cls, radius):
        if radius < 0:
            raise ValueError("Radius must be non-negative")
        return (4/3) * math.pi * radius ** 3

class SphereSurfaceAreaOperation(MathOperation):
    name = "surface_area_sphere"
    args = ["radius"]
    help = "Calculate the surface area of a sphere"

    @classmethod
    def execute(cls, radius):
        if radius < 0:
            raise ValueError("Radius must be non-negative")
        return 4 * math.pi * radius ** 2

class CylinderVolumeOperation(MathOperation):
    name = "volume_cylinder"
    args = ["radius", "height"]
    help = "Calculate the volume of a cylinder"

    @classmethod
    def execute(cls, radius, height):
        if radius < 0 or height < 0:
            raise ValueError("Radius and height must be non-negative")
        return math.pi * radius ** 2 * height

class PythagoreanOperation(MathOperation):
    name = "pythagorean"
    args = ["a", "b"]
    help = "Calculate the hypotenuse of a right triangle using Pythagorean theorem"

    @classmethod
    def execute(cls, a, b):
        if a < 0 or b < 0:
            raise ValueError("Both sides must be non-negative")
        return math.sqrt(a ** 2 + b ** 2)

class PythagoreanSideOperation(MathOperation):
    name = "pythagorean_side"
    args = ["hypotenuse", "side"]
    help = "Calculate the unknown side of a right triangle given hypotenuse and one side"

    @classmethod
    def execute(cls, hypotenuse, side):
        if hypotenuse <= 0 or side <= 0:
            raise ValueError("Hypotenuse and side must be positive")
        if side >= hypotenuse:
            raise ValueError("Side must be less than hypotenuse")
        return math.sqrt(hypotenuse ** 2 - side ** 2)

class RegularPolygonAreaOperation(MathOperation):
    name = "area_regular_polygon"
    args = ["sides", "length"]
    help = "Calculate the area of a regular polygon given number of sides and side length"

    @classmethod
    def execute(cls, sides, length):
        if not isinstance(sides, int) or sides < 3:
            raise ValueError("Number of sides must be an integer >= 3")
        if length <= 0:
            raise ValueError("Side length must be positive")

        sides = int(sides)
        return (sides * length ** 2) / (4 * math.tan(math.pi / sides))
