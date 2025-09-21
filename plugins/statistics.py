"""
Statistical Functions Plugin

Provides statistical operations like mean, median, mode, variance,
standard deviation, and min/max operations.
"""

import math
from collections import Counter
from core.base_operations import MathOperation

class MeanOperation(MathOperation):
    name = "mean"
    args = ["numbers"]
    help = "Calculate the arithmetic mean (average) of a list of numbers"
    variadic = True

    @classmethod
    def execute(cls, *numbers):
        if len(numbers) == 0:
            raise ValueError("Cannot calculate mean of empty list")
        return sum(numbers) / len(numbers)

class MedianOperation(MathOperation):
    name = "median"
    args = ["numbers"]
    help = "Calculate the median of a list of numbers"
    variadic = True

    @classmethod
    def execute(cls, *numbers):
        if len(numbers) == 0:
            raise ValueError("Cannot calculate median of empty list")
        sorted_numbers = sorted(numbers)
        n = len(sorted_numbers)
        if n % 2 == 0:
            return (sorted_numbers[n//2 - 1] + sorted_numbers[n//2]) / 2
        else:
            return sorted_numbers[n//2]

class ModeOperation(MathOperation):
    name = "mode"
    args = ["numbers"]
    help = "Calculate the mode (most frequent value) of a list of numbers"
    variadic = True

    @classmethod
    def execute(cls, *numbers):
        if len(numbers) == 0:
            raise ValueError("Cannot calculate mode of empty list")
        counter = Counter(numbers)
        max_count = max(counter.values())
        modes = [num for num, count in counter.items() if count == max_count]
        return modes[0] if len(modes) == 1 else modes

class VarianceOperation(MathOperation):
    name = "variance"
    args = ["numbers"]
    help = "Calculate the sample variance of a list of numbers"
    variadic = True

    @classmethod
    def execute(cls, *numbers):
        if len(numbers) < 2:
            raise ValueError("Variance requires at least 2 numbers")
        mean = sum(numbers) / len(numbers)
        squared_diffs = [(x - mean) ** 2 for x in numbers]
        return sum(squared_diffs) / (len(numbers) - 1)

class PopulationVarianceOperation(MathOperation):
    name = "pop_variance"
    args = ["numbers"]
    help = "Calculate the population variance of a list of numbers"
    variadic = True

    @classmethod
    def execute(cls, *numbers):
        if len(numbers) == 0:
            raise ValueError("Cannot calculate population variance of empty list")
        mean = sum(numbers) / len(numbers)
        squared_diffs = [(x - mean) ** 2 for x in numbers]
        return sum(squared_diffs) / len(numbers)

class StandardDeviationOperation(MathOperation):
    name = "std_dev"
    args = ["numbers"]
    help = "Calculate the sample standard deviation of a list of numbers"
    variadic = True

    @classmethod
    def execute(cls, *numbers):
        if len(numbers) < 2:
            raise ValueError("Standard deviation requires at least 2 numbers")
        variance = VarianceOperation.execute(*numbers)
        return math.sqrt(variance)

class PopulationStandardDeviationOperation(MathOperation):
    name = "pop_std_dev"
    args = ["numbers"]
    help = "Calculate the population standard deviation of a list of numbers"
    variadic = True

    @classmethod
    def execute(cls, *numbers):
        if len(numbers) == 0:
            raise ValueError("Cannot calculate population standard deviation of empty list")
        variance = PopulationVarianceOperation.execute(*numbers)
        return math.sqrt(variance)

class MinimumOperation(MathOperation):
    name = "min"
    args = ["numbers"]
    help = "Find the minimum value in a list of numbers"
    variadic = True

    @classmethod
    def execute(cls, *numbers):
        if len(numbers) == 0:
            raise ValueError("Cannot find minimum of empty list")
        return min(numbers)

class MaximumOperation(MathOperation):
    name = "max"
    args = ["numbers"]
    help = "Find the maximum value in a list of numbers"
    variadic = True

    @classmethod
    def execute(cls, *numbers):
        if len(numbers) == 0:
            raise ValueError("Cannot find maximum of empty list")
        return max(numbers)

class RangeOperation(MathOperation):
    name = "range"
    args = ["numbers"]
    help = "Calculate the range (max - min) of a list of numbers"
    variadic = True

    @classmethod
    def execute(cls, *numbers):
        if len(numbers) == 0:
            raise ValueError("Cannot calculate range of empty list")
        return max(numbers) - min(numbers)

class SumOperation(MathOperation):
    name = "sum"
    args = ["numbers"]
    help = "Calculate the sum of a list of numbers"
    variadic = True

    @classmethod
    def execute(cls, *numbers):
        if len(numbers) == 0:
            raise ValueError("Cannot calculate sum of empty list")
        return sum(numbers)

class ProductOperation(MathOperation):
    name = "product"
    args = ["numbers"]
    help = "Calculate the product of a list of numbers"
    variadic = True

    @classmethod
    def execute(cls, *numbers):
        if len(numbers) == 0:
            raise ValueError("Cannot calculate product of empty list")
        result = 1
        for num in numbers:
            result *= num
        return result

class GeometricMeanOperation(MathOperation):
    name = "geometric_mean"
    args = ["numbers"]
    help = "Calculate the geometric mean of a list of positive numbers"
    variadic = True

    @classmethod
    def execute(cls, *numbers):
        if len(numbers) == 0:
            raise ValueError("Cannot calculate geometric mean of empty list")

        # Check for non-positive numbers
        for num in numbers:
            if num <= 0:
                raise ValueError("Geometric mean requires all positive numbers")

        # Calculate product and take nth root
        product = 1
        for num in numbers:
            product *= num
        return product ** (1.0 / len(numbers))

class HarmonicMeanOperation(MathOperation):
    name = "harmonic_mean"
    args = ["numbers"]
    help = "Calculate the harmonic mean of a list of positive numbers"
    variadic = True

    @classmethod
    def execute(cls, *numbers):
        if len(numbers) == 0:
            raise ValueError("Cannot calculate harmonic mean of empty list")

        # Check for zero or negative numbers
        for num in numbers:
            if num <= 0:
                raise ValueError("Harmonic mean requires all positive numbers")

        # Calculate harmonic mean: n / (1/x1 + 1/x2 + ... + 1/xn)
        reciprocal_sum = sum(1.0 / num for num in numbers)
        return len(numbers) / reciprocal_sum

class CountOperation(MathOperation):
    name = "count"
    args = ["numbers"]
    help = "Count the number of values provided"
    variadic = True

    @classmethod
    def execute(cls, *numbers):
        return len(numbers)
