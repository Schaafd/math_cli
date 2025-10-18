"""Number theory and combinatorics plugin for Math CLI."""

from core.base_operations import MathOperation
import math
from functools import reduce
import sympy


class IsPrimeOperation(MathOperation):
    """Test if a number is prime."""

    name = "is_prime"
    args = ["n"]
    help = "Test if prime: is_prime 17 -> true"
    category = "number_theory"

    @classmethod
    def execute(cls, n: int) -> bool:
        """Test if number is prime.

        Args:
            n: Number to test

        Returns:
            True if prime, False otherwise
        """
        n = int(n)
        if n < 2:
            return False
        return sympy.isprime(n)


class PrimeFactorsOperation(MathOperation):
    """Find prime factorization of a number."""

    name = "prime_factors"
    args = ["n"]
    help = "Prime factorization: prime_factors 84"
    category = "number_theory"

    @classmethod
    def execute(cls, n: int) -> dict:
        """Find prime factorization.

        Args:
            n: Number to factor

        Returns:
            Dictionary of {prime: power}
        """
        n = int(n)
        if n < 2:
            raise ValueError("Number must be >= 2")

        factors = sympy.factorint(n)
        return factors


class GCDOperation(MathOperation):
    """Calculate greatest common divisor."""

    name = "gcd"
    args = ["*numbers"]
    help = "Greatest common divisor: gcd 48 18 24"
    category = "number_theory"

    @classmethod
    def execute(cls, *numbers) -> int:
        """Calculate GCD.

        Args:
            *numbers: Numbers to find GCD of

        Returns:
            Greatest common divisor
        """
        if len(numbers) == 0:
            raise ValueError("Need at least one number")

        numbers = [int(n) for n in numbers]
        result = reduce(math.gcd, numbers)
        return result


class LCMOperation(MathOperation):
    """Calculate least common multiple."""

    name = "lcm"
    args = ["*numbers"]
    help = "Least common multiple: lcm 12 18 24"
    category = "number_theory"

    @classmethod
    def execute(cls, *numbers) -> int:
        """Calculate LCM.

        Args:
            *numbers: Numbers to find LCM of

        Returns:
            Least common multiple
        """
        if len(numbers) == 0:
            raise ValueError("Need at least one number")

        numbers = [int(n) for n in numbers]

        def lcm_two(a, b):
            return abs(a * b) // math.gcd(a, b)

        result = reduce(lcm_two, numbers)
        return result


class ModPowerOperation(MathOperation):
    """Calculate modular exponentiation (a^b mod m)."""

    name = "mod_power"
    args = ["base", "exponent", "modulus"]
    help = "Modular power: mod_power 3 4 5 -> 3^4 mod 5"
    category = "number_theory"

    @classmethod
    def execute(cls, base: int, exponent: int, modulus: int) -> int:
        """Calculate modular exponentiation.

        Args:
            base: Base number
            exponent: Exponent
            modulus: Modulus

        Returns:
            base^exponent mod modulus
        """
        base = int(base)
        exponent = int(exponent)
        modulus = int(modulus)

        if modulus <= 0:
            raise ValueError("Modulus must be positive")

        return pow(base, exponent, modulus)


class ModInverseOperation(MathOperation):
    """Calculate modular multiplicative inverse."""

    name = "mod_inverse"
    args = ["a", "m"]
    help = "Modular inverse: mod_inverse 3 11"
    category = "number_theory"

    @classmethod
    def execute(cls, a: int, m: int) -> int:
        """Calculate modular inverse.

        Args:
            a: Number
            m: Modulus

        Returns:
            x such that (a * x) mod m = 1

        Raises:
            ValueError: If inverse doesn't exist
        """
        a = int(a)
        m = int(m)

        try:
            return int(sympy.mod_inverse(a, m))
        except ValueError:
            raise ValueError(f"Modular inverse of {a} mod {m} does not exist")


class PermutationsOperation(MathOperation):
    """Calculate permutations P(n, r) = n!/(n-r)!"""

    name = "permutations"
    args = ["n", "r"]
    help = "Permutations: permutations 5 3 -> 60"
    category = "number_theory"

    @classmethod
    def execute(cls, n: int, r: int) -> int:
        """Calculate permutations.

        Args:
            n: Total items
            r: Items to arrange

        Returns:
            Number of permutations
        """
        n = int(n)
        r = int(r)

        if n < 0 or r < 0:
            raise ValueError("n and r must be non-negative")
        if r > n:
            raise ValueError("r cannot be greater than n")

        return math.perm(n, r)


class CombinationsOperation(MathOperation):
    """Calculate combinations C(n, r) = n!/(r!(n-r)!)"""

    name = "combinations"
    args = ["n", "r"]
    help = "Combinations: combinations 5 3 -> 10"
    category = "number_theory"

    @classmethod
    def execute(cls, n: int, r: int) -> int:
        """Calculate combinations.

        Args:
            n: Total items
            r: Items to choose

        Returns:
            Number of combinations
        """
        n = int(n)
        r = int(r)

        if n < 0 or r < 0:
            raise ValueError("n and r must be non-negative")
        if r > n:
            raise ValueError("r cannot be greater than n")

        return math.comb(n, r)


class FactorialOperation(MathOperation):
    """Calculate factorial n!"""

    name = "factorial"
    args = ["n"]
    help = "Factorial: factorial 5 -> 120"
    category = "number_theory"

    @classmethod
    def execute(cls, n: int) -> int:
        """Calculate factorial.

        Args:
            n: Non-negative integer

        Returns:
            n!
        """
        n = int(n)
        if n < 0:
            raise ValueError("Factorial not defined for negative numbers")
        if n > 170:
            raise ValueError("Factorial too large (max 170)")

        return math.factorial(n)


class FibonacciOperation(MathOperation):
    """Calculate nth Fibonacci number."""

    name = "fibonacci"
    args = ["n"]
    help = "Fibonacci number: fibonacci 10 -> 55"
    category = "number_theory"

    @classmethod
    def execute(cls, n: int) -> int:
        """Calculate nth Fibonacci number.

        Args:
            n: Index (0-indexed)

        Returns:
            nth Fibonacci number
        """
        n = int(n)
        if n < 0:
            raise ValueError("Index must be non-negative")

        return int(sympy.fibonacci(n))


class BinomialCoefficientOperation(MathOperation):
    """Calculate binomial coefficient (n choose k)."""

    name = "binomial"
    args = ["n", "k"]
    help = "Binomial coefficient: binomial 5 2 -> 10"
    category = "number_theory"

    @classmethod
    def execute(cls, n: int, k: int) -> int:
        """Calculate binomial coefficient.

        Args:
            n: Upper index
            k: Lower index

        Returns:
            Binomial coefficient C(n, k)
        """
        n = int(n)
        k = int(k)

        return math.comb(n, k)


class IsCoprime:
    """Test if two numbers are coprime (GCD = 1)."""

    name = "is_coprime"
    args = ["a", "b"]
    help = "Test if coprime: is_coprime 8 15 -> true"
    category = "number_theory"

    @classmethod
    def execute(cls, a: int, b: int) -> bool:
        """Test if numbers are coprime.

        Args:
            a: First number
            b: Second number

        Returns:
            True if coprime
        """
        a = int(a)
        b = int(b)

        return math.gcd(a, b) == 1


class EulerTotientOperation(MathOperation):
    """Calculate Euler's totient function φ(n)."""

    name = "euler_phi"
    args = ["n"]
    help = "Euler totient: euler_phi 12 -> 4"
    category = "number_theory"

    @classmethod
    def execute(cls, n: int) -> int:
        """Calculate Euler's totient.

        Args:
            n: Positive integer

        Returns:
            φ(n) - count of numbers ≤ n that are coprime to n
        """
        n = int(n)
        if n < 1:
            raise ValueError("n must be positive")

        return int(sympy.totient(n))


class NextPrimeOperation(MathOperation):
    """Find the next prime number after n."""

    name = "next_prime"
    args = ["n"]
    help = "Next prime: next_prime 10 -> 11"
    category = "number_theory"

    @classmethod
    def execute(cls, n: int) -> int:
        """Find next prime.

        Args:
            n: Starting number

        Returns:
            Next prime after n
        """
        n = int(n)
        return int(sympy.nextprime(n))


class NthPrimeOperation(MathOperation):
    """Find the nth prime number."""

    name = "nth_prime"
    args = ["n"]
    help = "Nth prime: nth_prime 10 -> 29"
    category = "number_theory"

    @classmethod
    def execute(cls, n: int) -> int:
        """Find nth prime.

        Args:
            n: Index (1-indexed)

        Returns:
            nth prime number
        """
        n = int(n)
        if n < 1:
            raise ValueError("Index must be positive")

        return int(sympy.prime(n))


class PrimeCountOperation(MathOperation):
    """Count primes less than or equal to n."""

    name = "prime_count"
    args = ["n"]
    help = "Count primes: prime_count 100 -> 25"
    category = "number_theory"

    @classmethod
    def execute(cls, n: int) -> int:
        """Count primes up to n.

        Args:
            n: Upper limit

        Returns:
            Number of primes <= n
        """
        n = int(n)
        if n < 2:
            return 0

        return int(sympy.primepi(n))


# All operations are automatically discovered by the plugin manager
