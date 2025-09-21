"""
Combinatorics and Number Theory Plugin

Provides combinatorial calculations, number theory functions,
and sequence operations.
"""

import math
from core.base_operations import MathOperation

class CombinationsOperation(MathOperation):
    name = "combinations"
    args = ["n", "r"]
    help = "Calculate nCr (n choose r) - number of ways to choose r items from n items"

    @classmethod
    def execute(cls, n, r):
        try:
            n, r = int(n), int(r)
        except (ValueError, TypeError):
            raise ValueError("Combinations requires integer inputs")
        if n < 0 or r < 0:
            raise ValueError("Both n and r must be non-negative")
        if r > n:
            return 0
        return math.factorial(n) // (math.factorial(r) * math.factorial(n - r))

class PermutationsOperation(MathOperation):
    name = "permutations"
    args = ["n", "r"]
    help = "Calculate nPr (n permute r) - number of ways to arrange r items from n items"

    @classmethod
    def execute(cls, n, r):
        try:
            n, r = int(n), int(r)
        except (ValueError, TypeError):
            raise ValueError("Permutations requires integer inputs")
        if n < 0 or r < 0:
            raise ValueError("Both n and r must be non-negative")
        if r > n:
            return 0
        return math.factorial(n) // math.factorial(n - r)

class FibonacciOperation(MathOperation):
    name = "fibonacci"
    args = ["n"]
    help = "Calculate the nth Fibonacci number (0-indexed)"

    @classmethod
    def execute(cls, n):
        try:
            n = int(n)
        except (ValueError, TypeError):
            raise ValueError("Fibonacci requires an integer input")
        if n < 0:
            raise ValueError("Fibonacci index must be non-negative")
        if n <= 1:
            return n

        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

class IsPrimeOperation(MathOperation):
    name = "is_prime"
    args = ["n"]
    help = "Check if a number is prime (returns 1 for prime, 0 for composite)"

    @classmethod
    def execute(cls, n):
        try:
            n = int(n)
        except (ValueError, TypeError):
            raise ValueError("Prime check requires an integer input")
        if n < 2:
            return 0
        if n == 2:
            return 1
        if n % 2 == 0:
            return 0

        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return 0
        return 1

class PrimeFactorsOperation(MathOperation):
    name = "prime_factors"
    args = ["n"]
    help = "Find the prime factorization of a number (returns product of prime factors)"

    @classmethod
    def execute(cls, n):
        try:
            n = int(n)
        except (ValueError, TypeError):
            raise ValueError("Prime factorization requires an integer input")
        if n <= 1:
            raise ValueError("Prime factorization requires a number > 1")

        factors = []
        d = 2
        while d * d <= n:
            while n % d == 0:
                factors.append(d)
                n //= d
            d += 1
        if n > 1:
            factors.append(n)

        # Return the product for now (could be modified to return the list)
        result = 1
        for factor in factors:
            result *= factor
        return result

class IsEvenOperation(MathOperation):
    name = "is_even"
    args = ["n"]
    help = "Check if a number is even (returns 1 for even, 0 for odd)"

    @classmethod
    def execute(cls, n):
        try:
            n = int(n)
        except (ValueError, TypeError):
            raise ValueError("Even check requires an integer input")
        return 1 if n % 2 == 0 else 0

class IsOddOperation(MathOperation):
    name = "is_odd"
    args = ["n"]
    help = "Check if a number is odd (returns 1 for odd, 0 for even)"

    @classmethod
    def execute(cls, n):
        try:
            n = int(n)
        except (ValueError, TypeError):
            raise ValueError("Odd check requires an integer input")
        return 1 if n % 2 != 0 else 0

class DigitSumOperation(MathOperation):
    name = "digit_sum"
    args = ["n"]
    help = "Calculate the sum of digits in a number"

    @classmethod
    def execute(cls, n):
        try:
            n = abs(int(n))  # Work with absolute value
        except (ValueError, TypeError):
            raise ValueError("Digit sum requires an integer input")
        digit_sum = 0
        while n > 0:
            digit_sum += n % 10
            n //= 10
        return digit_sum

class ReverseNumberOperation(MathOperation):
    name = "reverse_number"
    args = ["n"]
    help = "Reverse the digits of a number"

    @classmethod
    def execute(cls, n):
        try:
            n = int(n)
        except (ValueError, TypeError):
            raise ValueError("Number reversal requires an integer input")
        sign = -1 if n < 0 else 1
        n = abs(n)

        reversed_n = 0
        while n > 0:
            reversed_n = reversed_n * 10 + n % 10
            n //= 10

        return sign * reversed_n

class IsPerfectSquareOperation(MathOperation):
    name = "is_perfect_square"
    args = ["n"]
    help = "Check if a number is a perfect square (returns 1 for yes, 0 for no)"

    @classmethod
    def execute(cls, n):
        try:
            n = int(n)
        except (ValueError, TypeError):
            raise ValueError("Perfect square check requires an integer input")
        if n < 0:
            return 0

        sqrt_n = int(math.sqrt(n))
        return 1 if sqrt_n * sqrt_n == n else 0
